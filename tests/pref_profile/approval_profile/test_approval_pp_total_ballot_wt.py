from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_pp_total_ballot_wt():
    pp = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A", "B"}, weight=2),
            ApprovalBallot(approvals={"A", "B"}, voter_set={"Chris"}),
            ApprovalBallot(),
            ApprovalBallot(weight=0),
        ],
        candidates=["A", "B", "C", "D"],
    )
    assert pp.total_ballot_wt == 4

    pp = pp.group_ballots()
    assert pp.total_ballot_wt == 4
