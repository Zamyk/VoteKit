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


def approval_biased_profile_generator(
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

    p1 = random.random()
    p2 = random.random()

    n1 = (int)(number_of_ballots * 0.4)
    n2 = (int)(number_of_ballots * 0.4)
    n3 = number_of_ballots - n1 - n2

    ballots = (
        [
            ApprovalBallot(
                approvals=[candidate for candidate in candidates if random.random() < p1]
            )
            for _ in range(n1)
        ]
        + [
            ApprovalBallot(
                approvals=[candidate for candidate in candidates if random.random() < p2]
            )
            for _ in range(n2)
        ]
        + [
            ApprovalBallot(
                approvals=[candidate for candidate in candidates if random.random() < 0.5]
            )
            for _ in range(n3)
        ]
    )

    return ApprovalProfile(ballots=tuple(ballots), candidates=candidates)
