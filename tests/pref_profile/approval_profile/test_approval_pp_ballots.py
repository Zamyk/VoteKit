from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_ballots_basic():
    ballots = [
        ApprovalBallot(approvals={"A", "B"}, weight=2.0),
        ApprovalBallot(approvals={"C"}, weight=1.5, voter_set={"Chris"}),
    ]
    pp = ApprovalProfile(ballots=ballots)
    returned_ballots = pp.ballots

    assert len(returned_ballots) == 2
    assert returned_ballots[0] == ballots[0]
    assert returned_ballots[1] == ballots[1]


def test_ballots_empty():
    pp = ApprovalProfile()
    assert pp.ballots == tuple()


def test_ballots_with_candidates():
    ballots = [
        ApprovalBallot(approvals={"A"}),
        ApprovalBallot(approvals={"B"}),
    ]
    pp = ApprovalProfile(ballots=ballots, candidates=["A", "B", "C"])
    returned_ballots = pp.ballots

    assert len(returned_ballots) == 2
    assert returned_ballots[0] == ballots[0]
    assert returned_ballots[1] == ballots[1]
