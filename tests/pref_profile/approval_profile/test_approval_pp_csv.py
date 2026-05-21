import csv
import io

import pytest

from votekit.ballot import ApprovalBallot
from votekit.pref_profile.approval_profile import ApprovalProfile

filepath = "tests/pref_profile/data/approval_profile"


def test_csv_bijection_approval(tmp_path):
    profile = ApprovalProfile(
        ballots=(
            ApprovalBallot(approvals={"Alex", "Allen", "D"}, voter_set={"Chris"}),
            ApprovalBallot(approvals={"Alex", "Allen", "D"}, voter_set={"Peter", "Moon"}),
            ApprovalBallot(
                approvals={"Alex", "Allen", "C"},
            ),
            ApprovalBallot(
                approvals={"Alex", "Allen", "C"},
            ),
            ApprovalBallot(
                approvals={"Alex", "Allen", "C"},
            ),
        )
        * 5,
        candidates=["Alex", "Allen", "C", "D", "E"],
    )
    out = str(tmp_path / "test_csv_pp_approval.csv")
    profile.to_csv(out, include_voter_set=True)
    read_profile = ApprovalProfile.from_csv(out)
    assert profile == read_profile


def test_csv_filepath_error():
    with pytest.raises(ValueError, match="File path must be provided."):
        ApprovalProfile().to_csv("")


def test_csv_misformatted_header_rows_error():
    with pytest.raises(
        ValueError,
        match=("csv file is improperly formatted. Row 0 should be 'VoteKit ApprovalProfile'."),
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_header_0.csv")

    with pytest.raises(
        ValueError,
        match=("csv file is improperly formatted. Row 1 should be 'Candidates'."),
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_header_1.csv")

    with pytest.raises(
        ValueError,
        match=("csv file is improperly formatted. Row 3 should be 'Includes Voter Set'."),
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_header_3.csv")

    with pytest.raises(
        ValueError,
        match=("csv file is improperly formatted. Row 5 should be '=,=,=,=,=,=,=,=,=,='."),
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_header_5.csv")


def test_csv_misformatted_header_values_error():
    with pytest.raises(ValueError, match="Row 2 should contain tuples mapping candidates"):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_header_value_2.csv")

    with pytest.raises(
        ValueError,
        match=("csv file is improperly formatted. Row 4 should be 'True' or 'False'."),
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_header_value_4_1.csv")

    with pytest.raises(
        ValueError,
        match=("csv file is improperly formatted. Row 4 should be 'True' or 'False'."),
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_header_value_4_2.csv")


def test_csv_misformatted_ballot_header_values_error():
    with pytest.raises(ValueError, match="Row 6 should include all candidates before the first &."):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_ballot_header_candidates.csv")

    with pytest.raises(ValueError, match="Row 6 should include 'Weight' column."):
        ApprovalProfile.from_csv(
            (f"{filepath}/test_csv_pp_misformat_ballot_header_weight_missing.csv")
        )

    with pytest.raises(ValueError, match="Includes Voter Set is not set to the correct value"):
        ApprovalProfile.from_csv(
            (f"{filepath}/test_csv_pp_misformat_ballot_header_voter_set_false.csv")
        )

    with pytest.raises(ValueError, match="Includes Voter Set is not set to the correct value"):
        ApprovalProfile.from_csv(
            (f"{filepath}/test_csv_pp_misformat_ballot_header_voter_set_true.csv")
        )


def test_csv_misformatted_ballot_score_error():
    with pytest.raises(ValueError, match=("Ballot in row 7 is missing some votes")):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_ballot_vote_missing.csv")

    with pytest.raises(ValueError, match=(f"Ballot in row 7 has non-binary vote value: {'a'}. ")):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_ballot_vote_non_binary.csv")


def test_csv_misformatted_ballot_weight_error():
    with pytest.raises(
        ValueError,
        match=("Ballot in row 14 has a weight entry that is too long or short. "),
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_ballot_weight_long.csv")

    with pytest.raises(
        match=f"Ballot in row 14 has a weight entry that can't be converted to float {'a'}. "
    ):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_ballot_weight_non_float.csv")


def test_csv_misformatted_voter_set_error():
    with pytest.raises(ValueError, match=("Ballot in row 16 has a voter set but it should not.")):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_ballot_no_voter_set.csv")


def test_csv_voter_set_whitespace(tmp_path):
    expected = ApprovalProfile(
        ballots=(
            ApprovalBallot(approvals={"Alex", "Allen", "D"}, voter_set={"Chris"}),
            ApprovalBallot(approvals={"Alex", "Allen", "D"}, voter_set={"Peter", "Moon"}),
            ApprovalBallot(approvals={"Alex", "Allen", "C"}),
            ApprovalBallot(approvals={"Alex", "Allen", "C"}),
            ApprovalBallot(approvals={"Alex", "Allen", "C"}),
        )
        * 5,
        candidates=["Alex", "Allen", "C", "D", "E"],
    )
    ref = str(tmp_path / "ref.csv")
    expected.to_csv(ref, include_voter_set=True)
    assert ApprovalProfile.from_csv(
        f"{filepath}/test_csv_pp_voter_set_whitespace.csv"
    ) == ApprovalProfile.from_csv(ref)


def test_csv_to_string_round_trip(tmp_path):
    profile = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A", "B"}),
            ApprovalBallot(approvals={"B", "C"}),
        ],
        candidates=["A", "B", "C"],
    )
    csv_str = profile.to_csv()
    assert isinstance(csv_str, str)

    out = tmp_path / "round_trip.csv"
    out.write_text(csv_str, encoding="utf-8")
    read_profile = ApprovalProfile.from_csv(str(out))
    assert profile == read_profile


def test_csv_to_string_into_zipfile(tmp_path):
    import zipfile

    profile = ApprovalProfile(
        ballots=[
            ApprovalBallot(approvals={"A", "B"}),
            ApprovalBallot(approvals={"B", "C"}),
        ],
        candidates=["A", "B", "C"],
    )
    csv_str = profile.to_csv()

    assert csv_str is not None

    zip_path = tmp_path / "profiles.zip"
    with zipfile.ZipFile(str(zip_path), "w") as zf:
        zf.writestr("profile.csv", csv_str)

    with zipfile.ZipFile(str(zip_path), "r") as zf:
        extracted = tmp_path / "extracted.csv"
        extracted.write_bytes(zf.read("profile.csv"))

    read_profile = ApprovalProfile.from_csv(str(extracted))
    assert profile == read_profile


def test_csv_seven_errors():
    with pytest.raises(ValueError, match="There are errors on 7 lines"):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_7_errors.csv")


def test_csv_11_errors():
    with pytest.raises(ValueError, match="There are errors on at least ten lines"):
        ApprovalProfile.from_csv(f"{filepath}/test_csv_pp_misformat_11_errors.csv")
