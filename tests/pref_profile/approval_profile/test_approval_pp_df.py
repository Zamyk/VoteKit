import numpy as np
import pandas as pd

from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile

ballots_approval = [
    ApprovalBallot(
        weight=2,
        approvals={"A", "B"},
    ),
    ApprovalBallot(approvals={"D", "E"}, voter_set={"Chris"}),
    ApprovalBallot(),
    ApprovalBallot(weight=0),
]


def test_pp_df_approval():
    pp = ApprovalProfile(ballots=ballots_approval)
    data = {
        "A": [True, False, False, False],
        "B": [True, False, False, False],
        "D": [False, True, False, False],
        "E": [False, True, False, False],
        "Voter Set": [set(), {"Chris"}, set(), set()],
        "Weight": [2.0, 1.0, 1.0, 0.0],
    }
    true_df = pd.DataFrame(data)
    true_df.index.name = "Ballot Index"
    df = pp.df
    assert pp.df.equals(true_df)


def test_pp_df_approval_args():
    pp = ApprovalProfile(
        ballots=ballots_approval,
        candidates=["A", "B", "C", "D", "E"],
    )
    data = {
        "A": [True, False, False, False],
        "B": [True, False, False, False],
        "C": [False, False, False, False],
        "D": [False, True, False, False],
        "E": [False, True, False, False],
        "Voter Set": [set(), {"Chris"}, set(), set()],
        "Weight": [2.0, 1.0, 1.0, 0.0],
    }
    true_df = pd.DataFrame(data)
    true_df.index.name = "Ballot Index"
    assert pp.df.equals(true_df)
