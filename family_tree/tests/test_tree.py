import pytest
from .context import tree


@pytest.fixture
def populated_tree():
    """return a populated tree"""
    f = {
    "amy": {
        "father": "brian",
        "mother": "shelly",
        "sons": ["george"]
      },
    "alex": {
        "father": "evan",
        "mother": "diana",
        "wife": "nancy",
        "sisters": ["nisha"],
        "brothers": ["john","joe"],
        "cousins": ["peter", "steve"],
        "aunts": ["jane"],
        "uncles": ["bob"],
        "grandfather": "jack",
        "grandmother": "helen",
        "grandsons": ["jon", "billy"],
        "grandaughters": ["trish"],
        },
    "nancy": {
        "husband": "alex",
    },
    "george": {
        "mother": "amy"
    },
     "john": {
        "father": "evan",
        "mother": "diana",
        "sisters": ["nisha"],
        "brothers": ["alex", "joe"]
        },
    }

    return tree.Tree(f)


@pytest.mark.parametrize("name, relation, result", [
    ("alex", "father", "Father=Evan"),
    ("alex", "mother", "Mother=Diana"),
    ("alex", "wife", "Wife=Nancy"),
    ("alex", "grandmother", "Grandmother=Helen"),
    ("alex", "grandfather", "Grandfather=Jack"),
    ])
def test_singular_relationship(populated_tree, name, relation, result):

    assert populated_tree.get_relationships(name, relation) == result


@pytest.mark.parametrize("name, relation, result", [
    ("alex", "brothers", "Brothers=Joe,John"),
    ("alex", "sisters", "Sisters=Nisha"),
    ("alex", "cousins", "Cousins=Peter,Steve"),
    ("alex", "aunts", "Aunts=Jane"),
    ("alex", "uncles", "Uncles=Bob"),
    ("alex", "grandsons", "Grandsons=Billy,Jon"),
    ("alex", "grandaughters", "Grandaughters=Trish"),
    ])
def test_plural_relationships(populated_tree, name, relation, result):

    assert populated_tree.get_relationships(name, relation) == result


def test_person_doesnt_exist(populated_tree):

    with pytest.raises(ValueError):
        populated_tree.get_relationships("tina", "mother")


def test_relationship_missing(populated_tree):

    with pytest.raises(KeyError):
        populated_tree.get_relationships("john", "stepson")


def test_add_spouse_wife(populated_tree):

    assert populated_tree.add_spouse(
        "john", "kelly") == str.format(tree.WELCOME, "Kelly")
    assert populated_tree.data["john"]["wife"] == "kelly"
    assert populated_tree.data["kelly"]["husband"] == "john"


def test_add_spouse_husband(populated_tree):

    assert populated_tree.add_spouse(
        "phillip", "amy") == str.format(tree.WELCOME, "Phillip")
    assert populated_tree.data["phillip"]["wife"] == "amy"
    assert populated_tree.data["amy"]["husband"] == "phillip"


def test_add_spouse_neither_person_exists(populated_tree):

    with pytest.raises(ValueError):
        populated_tree.add_spouse("unknown", "annon")


def test_add_spouse_both_people_exist(populated_tree):

    with pytest.raises(ValueError):
        populated_tree.add_spouse("alex", "amy")


def test_add_spouse_person_already_has_spouse(populated_tree):

    with pytest.raises(ValueError):
        assert populated_tree.add_spouse("alex", "nancy")


def test_add_child_add_to_both_parents(populated_tree):

    assert populated_tree.add_child(
        "robin", "alex", "sons") == str.format(tree.WELCOME, "Robin")
    assert populated_tree.data["alex"]["sons"] == ["robin"]
    assert populated_tree.data["nancy"]["sons"] == ["robin"]


def test_add_child_child_exists_return_message(populated_tree):

    with pytest.raises(ValueError):
        populated_tree.add_child("george", "amy", "sons")
