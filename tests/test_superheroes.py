import responses

from superhero_api.superheroes import (
    BASE_URL,
    Gender,
    combined_hero_function,
    fetch_all_superheroes,
    filter_gender_work,
    get_tallest_hero,
    height_from_hero,
)

fake_heroes = [
    {
        "id": 1,
        "name": "Superman",
        "appearance": {"gender": "Male", "height": ["-", "200.5 cm"]},
        "work": {"occupation": "Former history professor", "base": "Oa"},
    },
    {
        "id": 2,
        "name": "Batgirl",
        "appearance": {"gender": "Female", "height": ["-", "170 cm"]},
        "work": {"occupation": "Barmen", "base": "Oa"},
    },
    # Нестандартный формат роста
    {
        "id": 3,
        "name": "Godzilla",
        "appearance": {"gender": "-", "height": ["-", 50_000]},
        "work": {"occupation": "-", "base": "Oa"},
    },
    # Поломанный пол
    {
        "id": 4,
        "name": "Woman Cat",
        "appearance": {"gender": "Cat", "height": ["-", "160 cm"]},
        "work": {"occupation": "Stewardess", "base": "Oa"},
    },
    # Незаписанная профессия
    {
        "id": 5,
        "name": "Cheburashka",
        "appearance": {"gender": "Male", "height": ["-", "0.5 meters"]},
        "work": {"occupation": "", "base": "Oa"},
    },
]

"""
Сначала проводим юнит-тесты по основным функциям,
после чего интеграционные тесты, чему нам поможет
мокирование responses и combined_hero_function 
"""

# Тесты функции height_from_hero


def test_height_cm():
    hero = {"appearance": {"height": ["-", "200 cm"]}}
    assert height_from_hero(hero) == 200.0


def test_height_meters():
    hero = {"appearance": {"height": ["-", "10 meters"]}}
    assert height_from_hero(hero) == 1000.0


def test_height_unknown():
    hero = {"appearance": {"height": ["-", "-"]}}
    assert height_from_hero(hero) == 0.0


def test_height_incorrect():
    hero = {"appearance": {"height": ["-", "abracadabra"]}}
    assert height_from_hero(hero) == 0


# Тесты функции filter_gender_work


def test_filter_male_with_work():
    # Должнен найтись Супермен и Чебурашка (т.к. у него "")
    result = filter_gender_work(fake_heroes, Gender.MALE, True)
    assert len(result) == 1
    assert result[0]["name"] == "Superman"


def test_filter_unknown_without_work():
    result = filter_gender_work(fake_heroes, Gender.UNKNOWN, 0)
    assert len(result) == 1
    assert result[0]["name"] == "Godzilla"


def test_filter_empty_list():
    result = filter_gender_work(None, Gender.MALE, True)
    assert result is None


def test_filter_incorrect_params():
    result = filter_gender_work(fake_heroes, "", True)
    assert result is None


# Тесты функции get_tallest_hero


def test_get_tallest_hero():
    result = get_tallest_hero(fake_heroes)
    assert result["name"] == "Superman"


def test_get_tallest_hero_two_equal():
    result = get_tallest_hero(
        [
            {"appearance": {"height": ["-", "100 cm"]}},
            {"appearance": {"height": ["-", "100 cm"]}},
        ]
    )
    assert result == {"appearance": {"height": ["-", "100 cm"]}}


def test_get_tallest_hero_empty_list():
    result = get_tallest_hero(None)
    assert result is None


def test_get_tallest_hero_with_incorrect_params():
    # Продублировали героя с некорректными данными
    result = get_tallest_hero([fake_heroes[2]] * 2)
    assert result is None


# МОКИРОВАНИЕ API

# Тестирование функции fetch_all_superheroes


@responses.activate
def test_fetch_all_superheroes():
    responses.add(responses.GET, f"{BASE_URL}/all.json", json=fake_heroes, status=200)
    result = fetch_all_superheroes()
    assert result[4]["name"] == "Cheburashka"
    assert result == fake_heroes


@responses.activate
def test_fetch_all_superheroes_error():
    responses.add(responses.GET, f"{BASE_URL}/all.json", status=404)
    result = fetch_all_superheroes()
    assert result is None


# Интеграционное тестирование


@responses.activate
def test_combined_hero_function_Female_True():
    responses.add(responses.GET, f"{BASE_URL}/all.json", json=fake_heroes, status=200)
    result = combined_hero_function(Gender.FEMALE, True)
    assert result["name"] == "Batgirl"


@responses.activate
def test_combined_hero_function_Male_True():
    responses.add(responses.GET, f"{BASE_URL}/all.json", json=fake_heroes, status=200)
    result = combined_hero_function(Gender.MALE, True)
    assert result["name"] == "Superman"


@responses.activate
def test_combined_hero_function_empty_list():
    responses.add(responses.GET, f"{BASE_URL}/all.json", json=[], status=200)
    result = combined_hero_function(Gender.MALE, True)
    assert result is None


@responses.activate
def test_combined_hero_function_error():
    responses.add(responses.GET, f"{BASE_URL}/all.json", json=fake_heroes, status=500)
    result = combined_hero_function("Male", 5)
    assert result is None
