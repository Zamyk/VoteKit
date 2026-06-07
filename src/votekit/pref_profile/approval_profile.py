from __future__ import annotations

import pickle
from functools import cached_property
from os import PathLike
from pathlib import Path
from typing import Sequence, cast

import numpy as np
import pandas as pd

from votekit.ballot import ApprovalBallot
from votekit.exceptions import ProfileError
from votekit.pref_profile.utils import convert_row_to_approval_ballot


class ApprovalProfile:
    """
    ApprovalProfile class, contains ballots and candidates for a given election.
    This is a frozen class, so you need to create a new ApprovalProfile any time
    you want to edit the ballots, candidates, etc.

    Args:
        ballots (Sequence[ApprovalBallot], optional): Tuple of ``Ballot`` objects.
        Defaults to empty tuple.
        candidates (tuple[str], optional): Tuple of candidate strings. Defaults to empty tuple.
            If empty, computes this from any candidate listed on a ballot.

    Parameters:
        ballots (Sequence[ApprovalBallot]): Tuple of ``Ballot`` objects.
        candidates (tuple[str]): Tuple of candidate strings.
        candidates_cast (tuple[str]): Tuple of candidates who appear on any ballot with positive
            weight, either in the ranking or in the score dictionary.
        total_ballot_wt (float): Sum of ballot weights.
        num_ballots (int): Length of ballot list.

    Raises:
        ProfileError: a data frame and ballot list are passed to the init method.
        ProfileError: contains_rankings is set to False but a ballot contains a ranking.
        ProfileError: contains_rankings is set to True but no ballot contains a ranking.
        ProfileError: contains_scores is set to False but a ballot contains a score.
        ProfileError: contains_scores is set to True but no ballot contains a score.
        ProfileError: max_ranking_length is set but a ballot ranking excedes the length.
        ProfileError: a candidate is found on a ballot that is not listed on a provided
            candidate list.
        ProfileError: candidates must be unique.
        ProfileError: candidates must not have names matching ranking columns.

        TODO_ZAMYK
    """

    _is_frozen: bool = False

    def __init__(
        self,
        *,
        ballots: Sequence[ApprovalBallot] = tuple(),
        candidates: Sequence[str] = tuple(),
        votes: np.ndarray | None = None,
        weights: np.ndarray | None = None,
        voter_sets: np.ndarray | None = None,
    ):
        if votes is None:
            self.candidates = tuple(candidates)
            self.candidates_cast = tuple(
                sorted({candidate for ballot in ballots for candidate in (ballot.approvals or ())})
            )

            if self.candidates == tuple():
                self.candidates = self.candidates_cast

            self.votes = np.array(
                [
                    [
                        (ballot.approvals is not None and c in ballot.approvals)
                        for c in self.candidates
                    ]
                    for ballot in cast(Sequence[ApprovalBallot], ballots)
                ]
            ).reshape(len(ballots), len(self.candidates))

            self.weights = np.array([ballot.weight for ballot in ballots])
            self.voter_sets = np.array([ballot.voter_set for ballot in ballots])
        else:
            if weights is None or voter_sets is None:
                raise ProfileError(
                    "Passing votes requirse also passing weights and voter sets."
                )  # TODO_ZAMYK
            self.candidates = tuple(candidates)
            self.candidates_cast = self.candidates
            self.votes = votes.copy()
            self.weights = weights.copy()
            self.voter_sets = voter_sets.copy()

            if self.votes.shape[1] != len(candidates):
                raise ProfileError("Candidates must match votes.")

        self.total_ballot_wt = self._find_total_ballot_wt()
        self.num_ballots = self._find_num_ballots()
        self._validate_and_set_candidates()

        self.votes.flags.writeable = False
        self.weights.flags.writeable = False
        self.voter_sets.flags.writeable = False
        self._is_frozen = True

    def _find_num_ballots(self) -> int:
        """
        Compute and set the number of ballots.

        Returns:
            int: num ballots
        """
        return len(self.weights)

    def _find_total_ballot_wt(self) -> float:
        """
        Compute and set the total ballot weight.

        Returns:
            float: total ballot weight.
        """
        return np.sum(self.weights)

    def _validate_and_set_candidates(self) -> None:
        """
        Ensure that the candidate names are not equal to the ranking column names, that they are
        unique, and strips whitespace from candidates.

        Raises:
            ProfileError: Candidate names must be unique.
            ProfileError: Candidate names must be unique.
        """

        if not len(set(self.candidates)) == len(self.candidates):
            raise ProfileError("All candidates must be unique.")

        if not set(self.candidates_cast).issubset(self.candidates):
            raise ProfileError(
                "Candidates cast are not a subset of candidates list. The following "
                " candidates are in candidates_cast but not candidates: "
                f"{set(self.candidates_cast) - set(self.candidates)}."
            )

        self.candidates = tuple([c.strip() for c in self.candidates])
        self.candidates_cast = tuple([c.strip() for c in self.candidates_cast])

    @cached_property
    def ballots(self: ApprovalProfile) -> tuple[ApprovalBallot, ...]:
        """
        Compute the ballot tuple as a cached property.
        """
        computed_ballots = [
            convert_row_to_approval_ballot(b_row, tuple(self.candidates))
            for (_, b_row) in self.df.iterrows()
        ]
        return tuple(computed_ballots)

    @cached_property
    def df(self) -> pd.DataFrame:
        data = pd.DataFrame(self.votes, columns=self.candidates)
        data["Voter Set"] = self.voter_sets
        data["Weight"] = self.weights
        data.index.name = "Ballot Index"
        return data

    def group_ballots(self) -> ApprovalProfile:
        """Groups identical ballots and sums their weights."""
        df = self.df.reset_index(drop=True).copy()
        vote_cols = list(self.candidates)

        non_group_cols = ["Weight", "Voter Set"]
        cand_cols = [c for c in self.df.columns if c not in non_group_cols]
        group_df = df.groupby(cand_cols, dropna=False)
        new_df = group_df.aggregate(
            {
                "Weight": "sum",
                "Voter Set": (lambda sets: set().union(*sets)),
            }
        ).reset_index()

        votes = new_df[vote_cols].to_numpy(dtype=bool)
        weights = new_df["Weight"].to_numpy(dtype=float)
        voter_sets = new_df["Voter Set"].to_numpy(dtype=object)

        return ApprovalProfile(
            candidates=self.candidates, votes=votes, weights=weights, voter_sets=voter_sets
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ApprovalProfile):
            return False

        if set(self.candidates) != set(other.candidates):
            return False
        if set(self.candidates_cast) != set(other.candidates_cast):
            return False
        if self.total_ballot_wt != other.total_ballot_wt:
            return False

        # it seems it would be better to use set/sorting instead for better compleity? TODO_Zamyk
        pp_1 = self.group_ballots()
        pp_2 = other.group_ballots()
        for b in pp_1.ballots:
            if b not in pp_2.ballots:
                return False
        for b in pp_2.ballots:
            if b not in pp_1.ballots:
                return False
        return True

    def __add__(self, other: ApprovalProfile) -> ApprovalProfile:
        """Combines two profiles into a new one."""

        candidates = self.candidates + tuple(
            [c for c in other.candidates if c not in self.candidates]
        )

        candidate_index_1 = {candidate: i for i, candidate in enumerate(self.candidates)}
        candidate_index_2 = {candidate: i for i, candidate in enumerate(other.candidates)}

        votes_1 = np.zeros((self.votes.shape[0], len(candidates)), dtype=bool)
        votes_2 = np.zeros((other.votes.shape[0], len(candidates)), dtype=bool)

        for index, candidate in enumerate(candidates):
            if candidate in self.candidates:
                votes_1[:, index] = self.votes[:, candidate_index_1[candidate]]

            if candidate in other.candidates:
                votes_2[:, index] = other.votes[:, candidate_index_2[candidate]]

        votes = np.vstack([votes_1, votes_2])
        voter_sets = np.concatenate((self.voter_sets, other.voter_sets))
        weights = np.concatenate((self.weights, other.weights))

        return ApprovalProfile(
            candidates=candidates, votes=votes, voter_sets=voter_sets, weights=weights
        )

    def __str__(self) -> str:
        repr_str = "ApprovalProfile\n"
        repr_str += (
            f"Candidates: {self.candidates}\n"
            f"Candidates who received votes: {self.candidates_cast}\n"
            f"Total number of Ballot objects: {self.num_ballots}\n"
            f"Total weight of Ballot objects: {self.total_ballot_wt}\n"
        )

        return repr_str

    __repr__ = __str__

    def __setattr__(self, name, value):
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"Cannot modify frozen instance: tried to set '{name}'")
        super().__setattr__(name, value)

    def __delattr__(self, name):
        if getattr(self, "_is_frozen", False):
            raise AttributeError(f"Cannot delete attribute '{name}' from frozen instance")
        super().__delattr__(name)

    def to_csv(
        self, fpath: str | PathLike | Path | None = None, include_voter_set: bool = False
    ) -> str | None:
        """Saves profile to a CSV or returns CSV string."""
        raise NotImplementedError

    @classmethod
    def from_csv(cls, fpath: str | PathLike | Path) -> ApprovalProfile:
        """Creates an ApprovalProfile from a CSV file."""
        raise NotImplementedError

    def to_pickle(self, fpath: str | PathLike | Path):
        """Saves profile to a binary pickle file."""
        if fpath == "":
            raise ValueError("File path must be provided.")
        with open(str(fpath), "wb") as f:
            pickle.dump(self, f)

    @classmethod
    def from_pickle(cls, fpath: str | PathLike | Path) -> ApprovalProfile:
        """Loads an ApprovalProfile from a pickle file."""
        with open(str(fpath), "rb") as f:
            return pickle.load(f)
