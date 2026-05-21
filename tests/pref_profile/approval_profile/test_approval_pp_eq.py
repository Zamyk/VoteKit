from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_profile_equals():
    profile1 = ApprovalProfile(
        ballots=(
            ApprovalBallot(approvals={"D", "E"}, weight=2),
            ApprovalBallot(approvals={"D", "E"}, weight=2),
        )
    )
    profile2 = ApprovalProfile(ballots=(ApprovalBallot(approvals={"D", "E"}, weight=4),))
    # This might fail if group_ballots/eq is not implemented correctly
    assert profile1 == profile2


def test_profile_not_equals_candidates():
    profile1 = ApprovalProfile(ballots=(ApprovalBallot(approvals={"D", "E"}, weight=4),))
    profile2 = ApprovalProfile(
        ballots=(ApprovalBallot(approvals={"D", "E"}, weight=4),),
        candidates=["A", "B", "C", "D", "E"],
    )

    assert profile1 != profile2


def test_profile_not_equals_cand_cast():
    profile1 = ApprovalProfile(
        ballots=(ApprovalBallot(approvals={"D", "E", "F"}, weight=4),),
        candidates=["D", "E", "F"],
    )
    profile2 = ApprovalProfile(
        ballots=(ApprovalBallot(approvals={"D", "E"}, weight=4),),
        candidates=["D", "E", "F"],
    )

    assert profile1 != profile2
