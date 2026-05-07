from typing import Optional, Sequence, Union

import numpy as np

from votekit.elections import Election, ElectionState
from votekit.pref_profile.approval_profile import ApprovalProfile


class GeneralApproval(Election[ApprovalProfile]):
    def __init__(self, profile: ApprovalProfile):
        super().__init__(profile=profile)


def _hamming_score(profile: ApprovalProfile, weights: np.ndarray, committee: np.ndarray) -> float:
    distances = (profile.votes != committee).sum(axis=1)# * profile.weights
    distances = np.sort(distances)[::-1]
    return np.dot(distances, weights)


def _get_elected(
    profile: ApprovalProfile, weights: np.ndarray, tiebreak: Optional[str]
) -> np.ndarray:
    candidates = profile.candidates
    best_score = float("inf")
    best_committee = np.zeros(len(candidates))

    for mask in range((1 << (len(candidates))) - 1, -1, -1):
        committee = np.array([(mask >> i) & 1 for i in range(len(candidates))])
        score = _hamming_score(profile=profile, weights=weights, committee=committee)
        if score < best_score:
            best_score = score
            best_committee = committee

    return best_committee


def _get_weights(weights, n):
    if weights == "minisum":
        weights = ("f", 0)
    elif weights == "minimax":
        weights = ("f", n - 1)

    if isinstance(weights, tuple) and weights[0] == "f":
        i = weights[1]
        return [1.0 / (n - i)] * (n - i) + [0.0] * i

    return np.ndarray(weights)


class OrderedWeightedHamming(GeneralApproval):
    def __init__(
        self,
        profile: ApprovalProfile,
        tiebreak: Optional[str] = None,
        weights: Union[Sequence[float] | str | tuple[str, int]] = "minisum",
    ):
        self.tiebreak = tiebreak
        self.weights = _get_weights(weights, profile.votes.shape[0])
        super().__init__(profile=profile)

    def _is_finished(self):
        # single round election
        if len(self.election_states) == 2:
            return True
        return False

    def _run_step(
        self, profile: ApprovalProfile, prev_state: ElectionState, store_states=False
    ) -> ApprovalProfile:
        elected_mask = _get_elected(profile, self.weights, self.tiebreak)
        elected = {
            profile.candidates[i] for i, val in enumerate(elected_mask) if val
        }

        if store_states:
            new_state = ElectionState(
                round_number=1,  # single shot election
                elected=tuple([frozenset(elected)]),
                eliminated=tuple([frozenset(set(profile.candidates) - elected)]),
            )

            self.election_states.append(new_state)

        return profile
