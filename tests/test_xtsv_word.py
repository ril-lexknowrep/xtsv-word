import pytest
from xtsv_word import WordFactory


INPUT_FIELDS = ['form', 'wsafter']
OUTPUT_FIELDS = ['output']
OUTPUT_INITS = {'output': 'foo'}


# Factory initialisation

def test_factory():
    wf = WordFactory(INPUT_FIELDS, target_fields=OUTPUT_FIELDS)
    assert wf.input_fields == INPUT_FIELDS
    assert wf.target_fields == {'output': ''}


def test_factory_no_kw():
    wf = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS)
    assert wf.target_fields == {'output': ''}


def test_factory_inits():
    wf = WordFactory(INPUT_FIELDS, target_field_inits=OUTPUT_INITS)
    assert wf.input_fields == INPUT_FIELDS
    assert wf.target_fields == OUTPUT_INITS


def test_factory_missing_targets():
    with pytest.raises(TypeError):
        wf = WordFactory(INPUT_FIELDS)


def test_factory_both_kws():
    wf = WordFactory(INPUT_FIELDS, ['bar'],
                     target_field_inits=OUTPUT_INITS)
    assert wf.target_fields == OUTPUT_INITS


def test_factory_empty_input():
    wf = WordFactory([], OUTPUT_FIELDS)
    assert wf.input_fields == []
    assert wf.target_fields == {'output': ''}


def test_factory_empty_output():
    wf = WordFactory(INPUT_FIELDS, [])
    assert wf.input_fields == INPUT_FIELDS
    assert wf.target_fields == {}


def test_factory_empty_output_inits():
    wf = WordFactory(INPUT_FIELDS, target_field_inits={})
    assert wf.input_fields == INPUT_FIELDS
    assert wf.target_fields == {}


WORD_1 = ['A', ' ']
WORD_2 = ['tükörfúrógép', '\n']

# Word fields

def test_word_init():
    wf = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS)
    word1 = wf.get_word(WORD_1)
    word2 = wf.get_word(WORD_2)

    assert list(word1.keys()) == INPUT_FIELDS + OUTPUT_FIELDS
    assert list(word1.values()) == WORD_1 + ['']

    assert list(word2.keys()) == INPUT_FIELDS + OUTPUT_FIELDS
    assert list(word2.values()) == WORD_2 + ['']


def test_word_init_two_factories():
    wf1 = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS)
    wf2 = WordFactory([], target_field_inits=OUTPUT_INITS)

    word1 = wf1.get_word(WORD_1)
    word2 = wf2.get_word([])

    assert list(word1.keys()) == INPUT_FIELDS + OUTPUT_FIELDS
    assert list(word1.values()) == WORD_1 + ['']

    assert list(word2.keys()) == list(OUTPUT_INITS.keys())
    assert list(word2.values()) == list(OUTPUT_INITS.values())


def test_target_defaults():
    wf = WordFactory([], OUTPUT_FIELDS, target_value_default='.')
    word = wf.get_word([])
    assert list(word.values()) == ['.']


def test_list():
    wf = WordFactory(INPUT_FIELDS, target_field_inits=OUTPUT_INITS)
    word = wf.get_word(WORD_2)
    assert list(word) == WORD_2 + list(OUTPUT_INITS.values())


def test_setters():
    wf = WordFactory(INPUT_FIELDS, target_field_inits=OUTPUT_INITS)
    word1 = wf.get_word(WORD_1)
    word2 = wf.get_word(WORD_2)

    assert list(word1) == ['A', ' ', 'foo']
    assert list(word2) == ['tükörfúrógép', '\n', 'foo']

    word1.form = 'B'
    word2.wsafter = '\t'
    word1.output = 'bar'
    word2.output = 'baz'

    assert list(word1) == ['B', ' ', 'bar']
    assert list(word2) == ['tükörfúrógép', '\t', 'baz']


def test_add_attribute():
    wf = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS)
    word = wf.get_word(WORD_1)
    word.foo = 'bar'
    assert list(word) == ['A', ' ', '']


def test_reprs():
    wf = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS, target_value_default='-')
    assert str(wf) == ("WordFactory(input_fields=['form', 'wsafter'], "
                       + "target_fields={'output': '-'})")
    word = wf.get_word(WORD_1)
    assert str(word) == ("Word(form='A', wsafter=' ', output='-')")


def test_word_exception1():
    wf = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS)
    with pytest.raises(ValueError):
        word = wf.get_word([])


def test_word_exception2():
    wf = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS)
    with pytest.raises(ValueError):
        word = wf.get_word(['A'])


def test_word_exception3():
    wf = WordFactory(INPUT_FIELDS, OUTPUT_FIELDS)
    with pytest.raises(ValueError):
        word = wf.get_word(['A', ' ', 'foo'])
