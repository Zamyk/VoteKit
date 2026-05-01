from __future__ import annotations

import pickle
from os import PathLike
from pathlib import Path
from typing import Self, Sequence, cast

import numpy as np
import pandas as pd

from votekit.ballot import ApprovalBallot, Ballot


class ApprovalProfile:
    """ """

    _is_frozen: bool = False

    def __init__(
        self,
        *,
        ballots: Sequence[Ballot] = tuple(),
        candidates: Sequence[str] = tuple(),
    ):
        self.votes = np.array(
            [
                [c in ballot.approvals for c in candidates]
                for ballot in cast(Sequence[ApprovalBallot], ballots)
            ]
        )
        self.weights = np.array(ballot.weight for ballot in ballots)
        self.candidates = list(candidates)

    @property
    def ballots(self) -> tuple[Ballot, ...]:
        """Returns the ballots contained in the profile."""
        raise NotImplementedError

    @property
    def df(self) -> pd.DataFrame:
        """Returns the data frame representing the profile."""
        raise NotImplementedError

    def group_ballots(self) -> Self:
        """Groups identical ballots and sums their weights."""
        raise NotImplementedError

    def __eq__(self, other: object) -> bool:
        """Checks if two profiles are equivalent."""
        return False

    def __str__(self) -> str:
        """Returns a human-readable summary of the profile."""
        return "ApprovalProfile"

    def __repr__(self) -> str:
        return self.__str__()

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

    def __add__(self, other: ApprovalProfile) -> ApprovalProfile:
        """Combines two profiles into a new one."""
        raise NotImplementedError
