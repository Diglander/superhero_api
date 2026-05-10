from superhero_api.superheroes import Gender, combined_hero_function

if __name__ == "__main__":
    # Ввод пола с проверками корректности
    gender = input("Введите пол (Male/Female/-): ").capitalize()
    while gender not in (Gender.MALE, Gender.FEMALE, Gender.UNKNOWN):
        gender = input(
            "Введите пол ТОЛЬКО из указанных вариантов (Male/Female/-): "
        ).capitalize()
    # Ввод наличия работы с проверками корректности
    with_work = input("Введите наличие работы (True/False): ").capitalize()
    while with_work not in ("True", "False"):
        with_work = input(
            "Введите наличие работы ТОЛЬКО из указанных вариантов (True/False): "
        ).capitalize()
    with_work = with_work == "True"
    # Вывод самого высокого героя по выбранным критериям
    final_hero = combined_hero_function(Gender(gender), with_work)
    if final_hero:
        print(
            f'Самый высокий герой по вашим критериям:\n {final_hero["name"]}, {final_hero["appearance"]["height"][1]}'
        )
    else:
        print("Нет подходящих героев")
