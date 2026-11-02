import json

from scripts import eval as evaluation


def test_denials_and_wrong_facts_cannot_pass_even_when_they_contain_keywords():
    question = {
        "expected": {"name": "Maya Chen", "email": "maya@example.test"},
        "source_ids": ["source-1"],
    }
    for answer in (
        "I do not know Maya Chen or her email maya@example.test",
        json.dumps(
            {"name": "Maya Chen", "email": "wrong@example.test", "source_ids": ["source-1"]}
        ),
        json.dumps({"name": "Maya Chen", "email": "maya@example.test", "source_ids": ["invented"]}),
    ):
        assert not evaluation.grade_answer(question, answer)["answered"]
    assert evaluation.grade_answer(
        question,
        json.dumps({"name": "Maya Chen", "email": "maya@example.test", "source_ids": ["source-1"]}),
    )["answered"]
