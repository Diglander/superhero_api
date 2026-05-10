from enum import Enum

import requests

BASE_URL = "https://akabab.github.io/superhero-api/api"


# Перечисление возможных полов
class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    UNKNOWN = "-"


# Забрать список всех супергероев
def fetch_all_superheroes() -> list | None:
    try:
        response = requests.get(f"{BASE_URL}/all.json")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
        return None


# Новый список по фильтрам пользователя
def filter_gender_work(
    super_list: list, gender: Gender, with_work: bool
) -> list | None:
    if not super_list:
        print("В переданном списке нет героев")
        return None
    filtered_list = []
    for hero in super_list:
        hero_work = hero["work"]["occupation"]
        hero_gender = hero["appearance"]["gender"]
        try:
            if hero_gender == gender and (hero_work != "-") == with_work:
                if hero_work == "" or not isinstance(hero_work, str):
                    continue
                filtered_list.append(hero)
        except (KeyError, IndexError, TypeError):
            print(f'Ошибка в обработке героя с id: {hero.get("id", "?")}')
            continue
    if not filtered_list:
        print("Нет героев под ваши критерии")
        return None
    return filtered_list


# Функция перевода словаря героя во float по сантиметрам
def height_from_hero(hero: dict) -> float:
    try:
        hero_height = hero["appearance"]["height"][1]
    except (KeyError, IndexError, TypeError):
        # Если нет ключа 'appearance', или список пустой, или там None
        return 0.0
    if hero_height == "-" or not isinstance(hero_height, str):
        return 0
    if hero_height.endswith(" cm"):
        height = float(hero_height.replace(" cm", ""))
    elif hero_height.endswith(" meters"):
        height = 100 * float(hero_height.replace(" meters", ""))
    else:
        print(
            """Не удалось получить рост героя.\n"""
            f""" id: {hero.get('id', '?')} \n height = {hero_height}"""
        )
        return 0
    return height


# Определение высочайшего героя из переданного списка
def get_tallest_hero(super_list: list) -> dict | None:
    if not super_list:
        print("В переданном списке нет героев")
        return None
    tallest_hero = None
    max_height = 0
    for hero in super_list:
        height = height_from_hero(hero)
        if height > max_height:
            tallest_hero = hero
            max_height = height
    return tallest_hero


# Объединяющая функциИ функциЯ, выполняющая условие задания
def combined_hero_function(gender: Gender, with_work: bool) -> dict | None:
    super_list = fetch_all_superheroes()
    filtered_list = filter_gender_work(super_list, gender, with_work)
    tallest_hero = get_tallest_hero(filtered_list)
    return tallest_hero
