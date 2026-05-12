# Интеграционное тестирование с проверкой всех комбинаций
import pytest
from superhero_api.superheroes import combined_hero_function, Gender


# Перебираем все случаи
@pytest.mark.parametrize(
    'gender, with_work, tallest_hero',
    [
        (Gender.FEMALE, False, "Ardina"),
        (Gender.FEMALE, True, "Giganta"),
        (Gender.MALE, False, "Ymir"),
        (Gender.MALE, True, "Utgard-Loki"),
        (Gender.UNKNOWN, False, "Godzilla"),
        (Gender.UNKNOWN, True, "Living Brain"),
    ]
)


def test_combined_hero_function_all_combination(gender, with_work, tallest_hero):
    result = combined_hero_function(gender, with_work)
    assert result['name'] == tallest_hero
    assert result['appearance']['gender'] == gender.value
