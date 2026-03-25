import pytest
from model import Question


def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

# ---- NOVOS TESTES - COMMIT 2 ----

def test_create_question_with_invalid_points():
    with pytest.raises(Exception):
        Question(title='q1', points=1000)
    with pytest.raises(Exception):
        Question(title='q1', points=-1)

def test_choice_ids_are_auto_incremented():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    assert len(question.choices) == 2
    assert c1.id == 1
    assert c2.id == 2

def test_remove_choice():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    question.add_choice('b')
    question.remove_choice_by_id(c1.id)
    assert len(question.choices) == 1
    assert question.choices[0].text == 'b'

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('a')
    question.add_choice('b')
    question.remove_all_choices()
    assert len(question.choices) == 0

def test_operations_with_invalid_choice_id():
    question = Question(title='q1')
    question.add_choice('a')
    with pytest.raises(Exception):
        question.remove_choice_by_id(999)
    with pytest.raises(Exception):
        question.set_correct_choices([999])

def test_set_correct_choices():
    question = Question(title='q1')
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    question.set_correct_choices([c1.id, c2.id])
    assert question.choices[0].is_correct is True
    assert question.choices[1].is_correct is True

def test_correct_selected_choices():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', is_correct=True)
    c2 = question.add_choice('b', is_correct=False)
    
    correct_ids = question.correct_selected_choices([c1.id, c2.id])
    assert correct_ids == [c1.id]

def test_correct_selected_choices_exceeds_max_selections():
    question = Question(title='q1', max_selections=1)
    c1 = question.add_choice('a')
    c2 = question.add_choice('b')
    with pytest.raises(Exception):
        question.correct_selected_choices([c1.id, c2.id])

def test_correct_selected_choices_none_correct():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', is_correct=False)
    c2 = question.add_choice('b', is_correct=False)
    
    correct_ids = question.correct_selected_choices([c1.id, c2.id])
    assert correct_ids == []

def test_correct_selected_choices_ignores_invalid_ids():
    question = Question(title='q1', max_selections=2)
    c1 = question.add_choice('a', is_correct=True)
    
    correct_ids = question.correct_selected_choices([c1.id, 999])
    assert correct_ids == [c1.id]

# ---- NOVOS TESTES - COMMIT 3 ----

@pytest.fixture
def question_with_choices():
    question = Question(title='Sample Question', max_selections=2)
    question.add_choice('Option A', is_correct=True)
    question.add_choice('Option B', is_correct=False)
    question.add_choice('Option C', is_correct=True)
    return question

def test_fixture_correct_selected_choices_mixed(question_with_choices):
    correct_ids = question_with_choices.correct_selected_choices([1, 2])
    assert correct_ids == [1]

def test_fixture_remove_middle_choice(question_with_choices):
    question_with_choices.remove_choice_by_id(2)
    assert len(question_with_choices.choices) == 2
    assert question_with_choices.choices[0].text == 'Option A'
    assert question_with_choices.choices[1].text == 'Option C'

def test_fixture_set_correct_choices_appends_to_existing(question_with_choices):
    question_with_choices.set_correct_choices([2])
    assert question_with_choices.choices[0].is_correct is True
    assert question_with_choices.choices[1].is_correct is True
    assert question_with_choices.choices[2].is_correct is True
