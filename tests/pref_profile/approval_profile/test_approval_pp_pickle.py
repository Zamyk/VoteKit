from urllib.error import URLError

import pytest

from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile


def test_pkl_bijection_approval(tmp_path):
    profile_1 = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A", "B"}, weight=2),
            ApprovalBallot(approvals={"A", "C"}, voter_set={"Chris"}),
            ApprovalBallot(),
            ApprovalBallot(weight=0),
        ],
        candidates=["A", "B", "C", "D"],
    )

    out = str(tmp_path / "test_pkl_pp_approval.pkl")
    profile_1.to_pickle(out)
    read_profile = ApprovalProfile.from_pickle(out)
    assert profile_1 == read_profile


def test_pkl_error():
    with pytest.raises(ValueError, match="File path must be provided."):
        ApprovalProfile().to_pickle("")


def test_pkl_url():
    # Note: This URL will likely fail until a file is actually uploaded,
    # but we keep it for analogy.
    with pytest.raises(URLError):
        ApprovalProfile.from_pickle("https://www.fail.com")
