from src.guardrails import check_question_scope


def test_finance_question_is_in_scope():
    assert check_question_scope("What are the travel spending limits?") is True


def test_policy_question_is_in_scope():
    assert check_question_scope("What are the company travel and expense policies?") is True


def test_pto_question_is_in_scope():
    assert check_question_scope("How many PTO days do employees get?") is True


def test_marketing_roi_question_is_in_scope():
    assert check_question_scope("What was campaign ROI in Q1?") is True


def test_compliance_question_is_in_scope():
    assert check_question_scope("What compliance controls need improvement?") is True


def test_off_topic_question_is_blocked():
    assert check_question_scope("What's the weather today?") is False
