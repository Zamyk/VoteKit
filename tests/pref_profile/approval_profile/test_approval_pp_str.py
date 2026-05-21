from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile

ballots = [
    ApprovalBallot(approvals={"A"}, weight=2),
    ApprovalBallot(approvals={"B"}, voter_set={"Chris"}),
    ApprovalBallot(),
    ApprovalBallot(weight=0),
]

p = ApprovalProfile(ballots=ballots, candidates=["A", "B", "C", "D"])


def test_print_profile_rankings():
    print(p)

    assert p.__str__() == (
        f"ApprovalProfile\n"
        f"Candidates: {('A', 'B', 'C', 'D')}\n"
        f"Candidates who received votes: {('A', 'B')}\n"
        f"Total number of Ballot objects: 4\n"
        f"Total weight of Ballot objects: 4.0\n"
    )
