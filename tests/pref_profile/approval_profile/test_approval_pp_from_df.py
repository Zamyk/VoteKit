# import pandas as pd
# import pytest

# from votekit.ballot import ApprovalBallot
# from votekit.pref_profile import ProfileError
# from votekit.pref_profile.approval_profile import ApprovalProfile

# profile = ApprovalProfile(
#     ballots=(
#         ApprovalBallot(approvals={"A", "E"}),
#         ApprovalBallot(
#             approvals={"A", "E"},
#         ),
#         ApprovalBallot(approvals={"D"}, weight=0),
#     ),
#     candidates=("A", "B", "C", "D", "E"),
# )
# df = profile.df


# def test_from_df():
#     new_profile = ApprovalProfile(
#         df=df,
#         candidates=profile.candidates,
#     )

#     assert new_profile == profile
#     assert set(new_profile.candidates_cast) == {"A", "E"}


# def test_from_df_init_errors():
#     with pytest.raises(
#         ProfileError,
#         match="Cannot pass a dataframe and a ballot list to profile init method. Must pick one.",
#     ):
#         ApprovalProfile(df=df, ballots=(ApprovalBallot(approvals={"Chris"}),))

#     # Note: ApprovalProfile shouldn't need to check for Rank vs Score ballots in the same way
#     # if it's strictly for Approval, but we keep the analogy if requested.
#     # However, PreferenceProfile (the parent) usually handles this.


# def test_from_df_validation_errors():
#     with pytest.raises(ProfileError, match="Weight column not in dataframe:"):
#         ApprovalProfile(
#             df=pd.DataFrame(columns=["Voter Set"]),
#             candidates=["A"],
#         )

#     with pytest.raises(ProfileError, match="Voter Set column not in dataframe:"):
#         ApprovalProfile(
#             df=pd.DataFrame(columns=["Weight"]),
#             candidates=["A"],
#         )

#     with pytest.raises(ProfileError, match="Index not named 'Ballot Index':"):
#         ApprovalProfile(
#             df=pd.DataFrame(columns=["Weight", "Voter Set"]),
#             candidates=["A"],
#         )

#     with pytest.raises(ProfileError, match="Candidate column 'B' not in dataframe:"):
#         df = pd.DataFrame(columns=["Weight", "Voter Set", "A", "C"])
#         df.index.name = "Ballot Index"
#         ApprovalProfile(
#             df=df,
#             candidates=["A", "B", "C"],
#         )
# TODO_ZAMYK
