import pytest

from votekit.ballot import ApprovalBallot
from votekit.pref_profile import ProfileError
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_pp_candidate_list():
    with pytest.raises(ProfileError, match="All candidates must be unique."):
        ApprovalProfile(
            ballots=(ApprovalBallot(approvals={"Peter"}),),
            candidates=["Peter", "Peter"],
        )

    with pytest.raises(ProfileError, match="Candidate Chris found in ballot "):
        ApprovalProfile(
            ballots=(ApprovalBallot(approvals={"Chris"}),),
            candidates=["Peter"],
        )
