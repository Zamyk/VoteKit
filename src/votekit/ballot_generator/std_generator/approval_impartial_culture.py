import random
from typing import Sequence

from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def approval_ic_profile_generator(
    candidates: Sequence[str],
    number_of_ballots: int,
) -> ApprovalProfile:
    """
    Impartial Culture model where each ballot is equally likely.
    Args:
        candidates (Sequence[str]): The list of candidates in the election.
        number_of_ballots (int): The number of ballots to generate for the profile.

    Returns:
        ApprovalProfile: The generated preference profile
    """

    ballots = [
        ApprovalBallot(approvals=[candidate for candidate in candidates if random.getrandbits(1)])
        for _ in range(number_of_ballots)
    ]

    return ApprovalProfile(ballots=tuple(ballots), candidates=candidates)
