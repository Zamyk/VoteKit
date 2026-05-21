from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_pp_group_ballots_approval():
    profile = ApprovalProfile(
        ballots=(
            ApprovalBallot(approvals={"D", "E"}, weight=2, voter_set={"Chris"}),
            ApprovalBallot(approvals={"D", "E"}, weight=2, voter_set={"Moon", "Peter"}),
            ApprovalBallot(
                approvals={"D", "E"},
                weight=2,
            ),
            ApprovalBallot(),
        )
    )

    pp = profile.group_ballots()
    assert set(pp.ballots) == set(
        (
            ApprovalBallot(
                approvals={"D", "E"},
                weight=6,
                voter_set={"Chris", "Moon", "Peter"},
            ),
            ApprovalBallot(),
        )
    )
    assert set(pp.candidates) == set(profile.candidates)
    assert profile == pp
