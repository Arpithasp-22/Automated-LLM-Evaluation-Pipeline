from scoring.accuracy import score_accuracy
from scoring.hallucination import is_hallucination
from scoring.refusal import is_refusal


# --- refusal -----------------------------------------------------------------

def test_refusal_detected():
    assert is_refusal("I'm sorry, but I cannot help with that.")
    assert is_refusal("I am unable to share that.")


def test_refusal_not_detected_on_normal_answer():
    assert not is_refusal("The capital of New Zealand is Wellington.")


# --- accuracy ----------------------------------------------------------------

def test_exact_match_is_case_insensitive():
    assert score_accuracy("It was neil armstrong.", "Neil Armstrong", "exact_match")
    assert not score_accuracy("Buzz Aldrin", "Neil Armstrong", "exact_match")


def test_numeric_uses_first_number_in_response():
    assert score_accuracy("The answer is 42.", "42", "numeric")
    assert not score_accuracy("The answer is 41.", "42", "numeric")


def test_numeric_no_number_in_response():
    assert not score_accuracy("I don't know.", "42", "numeric")


def test_keyword_match():
    assert score_accuracy("Use a hash map for O(1) lookups", "hash map", "keyword")


def test_json_match_ignores_key_order_and_whitespace():
    assert score_accuracy('{"b": 2, "a": 1}', '{"a":1,"b":2}', "json_match")
    assert not score_accuracy('{"a": 1}', '{"a": 2}', "json_match")


def test_refusal_only_rows_have_no_accuracy_score():
    assert score_accuracy("I cannot help with that.", "n/a", "refusal_only") is None


# --- hallucination -----------------------------------------------------------

def test_answering_when_refusal_expected_counts_as_hallucination():
    assert is_hallucination("Sure, here is the answer.", allow_refusal=True)


def test_refusing_when_refusal_expected_is_not_hallucination():
    assert not is_hallucination("I cannot help with that.", allow_refusal=True)


def test_no_hallucination_flag_when_refusal_not_expected():
    assert not is_hallucination("Sure, here is the answer.", allow_refusal=False)
