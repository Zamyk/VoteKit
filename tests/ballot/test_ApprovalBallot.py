import pytest

from votekit.ballot import ApprovalBallot, Ballot


def test_ballot_init():
    b = ApprovalBallot()
    assert isinstance(b, ApprovalBallot)
    assert b.approvals is None
    assert b.weight == 1
    assert b.voter_set == frozenset()


def test_init_from_parent_class():
    b = Ballot(approvals={"A", "B"}, voter_set={"Chris"}, weight=2)
    assert isinstance(b, ApprovalBallot)

    assert isinstance(b.approvals, frozenset)
    assert b.approvals == frozenset({"A", "B"})

    assert isinstance(b.weight, float)
    assert b.weight == 2.0

    assert isinstance(b.voter_set, frozenset)
    assert b.voter_set == frozenset({"Chris"})

    assert b == ApprovalBallot(approvals={"A", "B"}, voter_set={"Chris"}, weight=2)


def test_ballot_is_frozen():
    b = ApprovalBallot()
    with pytest.raises(AttributeError, match="is frozen"):
        b.approvals = (frozenset({"A"}),)
    with pytest.raises(AttributeError, match="is frozen"):
        b.weight = 2
    with pytest.raises(AttributeError, match="is frozen"):
        b.voter_set = frozenset({"A"})
    with pytest.raises(AttributeError, match="is frozen"):
        b._frozen = False


def test_ballot_is_frozen_del():
    b = ApprovalBallot(approvals={"A"}, weight=2, voter_set={"A"})
    with pytest.raises(AttributeError, match="is frozen"):
        del b.weight
    with pytest.raises(AttributeError, match="is frozen"):
        del b.voter_set
    with pytest.raises(AttributeError, match="is frozen"):
        del b._frozen
    with pytest.raises(AttributeError, match="is frozen"):
        del b.approvals


def test_ballot_hash():
    b1 = ApprovalBallot(approvals={"A"}, weight=2, voter_set={"A"})
    b2 = ApprovalBallot(approvals={"A"}, weight=2, voter_set={"A"})
    b3 = ApprovalBallot(approvals={"A"}, weight=1, voter_set={"B"})

    assert b1 == b2 and hash(b1) == hash(b2)
    assert b1 != b3 and hash(b1) != hash(b3)

    assert b2 in {b1}


def test_ballot_coerce_wt_to_float():
    assert isinstance(ApprovalBallot(weight=3).weight, float)
    assert isinstance(ApprovalBallot(weight=3.2).weight, float)


def test_ballot_strip_whitespace():
    b = ApprovalBallot(approvals=frozenset({" Chris", "Peter "}))

    assert b.approvals == frozenset({"Chris", "Peter"})


def test_ballot_tilde_errors():
    with pytest.raises(
        ValueError,
        match="'~' is a reserved character and cannot be used for candidate names.",
    ):
        ApprovalBallot(approvals={"~"})


def test_ballot_negative_weight():
    with pytest.raises(ValueError, match="Ballot weight cannot be negative."):
        ApprovalBallot(weight=-1.5)


def test_ballot_eq():
    b = ApprovalBallot(
        approvals={"A", "B", "C"},
        weight=3,
        voter_set={"Chris", "peter"},
    )

    assert b == ApprovalBallot(
        approvals={"A", "B", "C"},
        weight=3.0,
        voter_set={"peter", "Chris"},
    )

    assert b != "Hello"

    assert b != ApprovalBallot(
        weight=3,
        voter_set={"Chris", "peter"},
    )

    assert b != ApprovalBallot(
        approvals={"A", "B", "C"},
        voter_set={"Chris", "peter"},
    )

    assert b != ApprovalBallot(
        approvals={"A", "B", "C"},
        weight=3,
    )

    assert b != ApprovalBallot(
        approvals={"A", "B", "C", "D"},
        weight=3,
        voter_set={"Chris", "peter"},
    )


def test_ballot_str():
    b = ApprovalBallot(
        approvals={"A", "B", "C"},
        weight=3,
        voter_set={"Chris"},
    )

    assert str(b) == "ApprovalBallot\nA\nB\nC\nWeight: 3.0\nVoter set: {'Chris'}"


def test_approval_sub_ballot():
    assert isinstance(ApprovalBallot(), Ballot)
    assert isinstance(ApprovalBallot(), ApprovalBallot)


def test_approval_and_ranking():
    with pytest.raises(
        TypeError, match="Only one of approvals, ranking or scores can be provided."
    ):
        ApprovalBallot(approvals={"A"}, ranking=[{"A"}], scores={"A": 1})
