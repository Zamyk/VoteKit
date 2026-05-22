import pytest

from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile, ProfileError


def test_init():
    empty_profile = ApprovalProfile()
    assert empty_profile.ballots == tuple()
    assert not empty_profile.candidates
    assert not empty_profile.candidates_cast
    assert not empty_profile.total_ballot_wt
    assert not empty_profile.num_ballots


def test_unique_cands_validator():
    with pytest.raises(ProfileError, match="All candidates must be unique."):
        ApprovalProfile(candidates=("A", "A", "B"))

    ApprovalProfile(candidates=("A", "B"))


def test_strip_whitespace():
    pp = ApprovalProfile(candidates=("A ", " B", " C "))
    assert pp.candidates == ("A", "B", "C")


def test_ballots_frozen():
    p = ApprovalProfile(ballots=[ApprovalBallot(approvals={"A"})])
    b_list = p.ballots

    assert b_list == (ApprovalBallot(approvals={"A"}),)

    with pytest.raises(
        AttributeError,
        match="Cannot modify frozen instance: tried to set 'ballots'",
    ):
        p.ballots = (ApprovalBallot(approvals={"B"}, weight=5),)


def test_candidates_frozen():
    profile_no_cands = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A"}),
            ApprovalBallot(approvals={"B"}),
            ApprovalBallot(approvals={"C"}),
        ]
    )
    assert set(profile_no_cands.candidates) == set(["A", "B", "C"])
    assert set(profile_no_cands.candidates_cast) == set(["A", "B", "C"])

    with pytest.raises(
        AttributeError, match="Cannot modify frozen instance: tried to set 'candidates'"
    ):
        profile_no_cands.candidates = tuple()

    with pytest.raises(
        AttributeError,
        match="Cannot modify frozen instance: tried to set 'candidates_cast'",
    ):
        profile_no_cands.candidates_cast = tuple()


def test_get_candidates_received_votes():
    profile_w_cands = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A"}),
            ApprovalBallot(approvals={"B"}),
            ApprovalBallot(approvals={"C"}),
        ],
        candidates=("A", "B", "C", "D", "E"),
    )
    vote_cands = profile_w_cands.candidates_cast
    all_cands = profile_w_cands.candidates

    assert set(all_cands) == {"A", "B", "C", "D", "E"}
    assert set(vote_cands) == {
        "A",
        "B",
        "C",
    }


test_unique_cands_validator()
