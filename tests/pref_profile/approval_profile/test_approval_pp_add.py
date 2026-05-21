from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_add_profiles():
    profile_1 = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A", "B"}, weight=2),
            ApprovalBallot(approvals={"A", "C"}, voter_set={"Chris"}),
            ApprovalBallot(),
            ApprovalBallot(weight=0),
        ],
        candidates=["A", "B", "C", "D"],
    )

    profile_2 = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"D", "E"}, weight=2),
            ApprovalBallot(approvals={"D", "E", "F"}, weight=2),
            ApprovalBallot(),
            ApprovalBallot(weight=0),
        ],
        candidates=["D", "E", "F"],
    )
    summed_profile = profile_1 + profile_2
    true_summed_profile = ApprovalProfile(
        ballots=(
            ApprovalBallot(approvals={"A", "B"}, weight=2),
            ApprovalBallot(approvals={"A", "C"}, voter_set={"Chris"}),
            ApprovalBallot(),
            ApprovalBallot(weight=0),
            ApprovalBallot(approvals={"D", "E"}, weight=2),
            ApprovalBallot(approvals={"D", "E", "F"}, weight=2),
            ApprovalBallot(),
            ApprovalBallot(weight=0),
        ),
        candidates=["A", "B", "C", "D", "E", "F"],
    )

    assert set(summed_profile.candidates) == set(["A", "B", "C", "D", "E", "F"])
    assert isinstance(summed_profile, ApprovalProfile)
    assert true_summed_profile == summed_profile


test_add_profiles()