from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_pp_num_ballots():
    pp = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A", "B"}, weight=2),
            ApprovalBallot(approvals={"A", "B"}, voter_set={"Chris"}),
            ApprovalBallot(),
            ApprovalBallot(weight=0),
        ],
        candidates=["A", "B", "C", "D"],
    )
    assert pp.num_ballots == 4

    pp = pp.group_ballots()
    assert pp.num_ballots == 2
