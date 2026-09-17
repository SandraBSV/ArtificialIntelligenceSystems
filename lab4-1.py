"""
ЛАБОРАТОРНА РОБОТА №4
Функціональне тестування прототипу IDSS
на 8 тестових сценаріях.

Предметна область:
Оцінювання ринкової вартості та аналіз вигідності
пропозицій під час купівлі вживаних автомобілів.

AI-компонент:
Linear Regression.

Запуск:
    python test_scenarios.py
"""

import sys

import idss_core as core


try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


# ============================================================
# ДОПОМІЖНІ ФУНКЦІЇ
# ============================================================

def get_category_value(
    column,
    preferred=None,
    index=0,
):
    """
    Отримує значення категоріальної ознаки
    з CATEGORIES, щоб тестові сценарії відповідали
    metadata.json.

    Якщо preferred існує серед допустимих значень —
    використовується воно.

    Інакше використовується значення за індексом.
    """

    values = core.CATEGORIES.get(
        column,
        [],
    )

    if not values:
        return preferred or ""

    if preferred in values:
        return preferred

    index = min(
        index,
        len(values) - 1,
    )

    return values[index]


def get_numeric_value(
    column,
    position=0.5,
):
    """
    Формує числове значення на основі діапазону
    з metadata.json.

    position:
        0.0 — мінімум;
        0.5 — середина;
        1.0 — максимум.
    """

    minimum, maximum = core.get_numeric_range(
        column
    )

    if minimum is None or maximum is None:
        return 0

    value = minimum + (
        maximum - minimum
    ) * position

    return round(
        value,
        2,
    )


def get_example_car(
    price,
    category_index=0,
):
    """
    Формує базовий тестовий автомобіль.

    Категоріальні значення беруться з CATEGORIES,
    тому вони відповідають metadata.json.
    """

    return {
        "brand": get_category_value(
            "brand",
            index=category_index,
        ),

        "model": get_category_value(
            "model",
            index=category_index,
        ),

        "fuel_type": get_category_value(
            "fuel_type",
            index=category_index,
        ),

        "transmission": get_category_value(
            "transmission",
            index=category_index,
        ),

        "year": 2018,

        "engine_size": 2.0,

        "mileage": 85000,

        "current_price": price,
    }


# ============================================================
# ТЕСТОВІ СЦЕНАРІЇ
# ============================================================

SCENARIOS = [
    # --------------------------------------------------------
    # 1
    # --------------------------------------------------------

    {
        "name": "Вигідна пропозиція — низька ціна",
        "note": (
            "поточна ціна автомобіля суттєво нижча "
            "за прогнозовану ринкову"
        ),

        "expected": "BUY_NOW",

        "data": get_example_car(
            price=5000,
            category_index=0,
        ),
    },


    # --------------------------------------------------------
    # 2
    # --------------------------------------------------------

    {
        "name": "Завищена ціна автомобіля",
        "note": (
            "поточна ціна автомобіля суттєво вища "
            "за прогнозовану ринкову"
        ),

        "expected": "WAIT_BETTER_PRICE",

        "data": get_example_car(
            price=50000,
            category_index=1,
        ),
    },


    # --------------------------------------------------------
    # 3
    # --------------------------------------------------------

    {
        "name": "Ціна близька до ринкової",
        "note": (
            "поточна ціна знаходиться поблизу "
            "прогнозованої вартості"
        ),

        "expected": "MARKET_FAIR_PRICE",

        "data": get_example_car(
            price=22000,
            category_index=0,
        ),
    },


    # --------------------------------------------------------
    # 4
    # --------------------------------------------------------

    {
        "name": "Молодий автомобіль з малим пробігом",
        "note": (
            "перевірка роботи системи для автомобіля "
            "з невеликим пробігом"
        ),

        "expected": None,

        "data": {
            "brand": get_category_value(
                "brand",
                index=0,
            ),

            "model": get_category_value(
                "model",
                index=0,
            ),

            "fuel_type": get_category_value(
                "fuel_type",
                index=0,
            ),

            "transmission": get_category_value(
                "transmission",
                index=0,
            ),

            "year": 2022,

            "engine_size": 1.6,

            "mileage": 25000,

            "current_price": 25000,
        },
    },


    # --------------------------------------------------------
    # 5
    # --------------------------------------------------------

    {
        "name": "Автомобіль з великим пробігом",
        "note": (
            "перевірка системи для автомобіля "
            "з великим пробігом"
        ),

        "expected": None,

        "data": {
            "brand": get_category_value(
                "brand",
                index=1,
            ),

            "model": get_category_value(
                "model",
                index=1,
            ),

            "fuel_type": get_category_value(
                "fuel_type",
                index=0,
            ),

            "transmission": get_category_value(
                "transmission",
                index=1,
            ),

            "year": 2014,

            "engine_size": 2.0,

            "mileage": 180000,

            "current_price": 12000,
        },
    },


    # --------------------------------------------------------
    # 6
    # --------------------------------------------------------

    {
        "name": "Автомобіль з дорогим двигуном",
        "note": (
            "перевірка роботи моделі для автомобіля "
            "з більшим об'ємом двигуна"
        ),

        "expected": None,

        "data": {
            "brand": get_category_value(
                "brand",
                index=0,
            ),

            "model": get_category_value(
                "model",
                index=0,
            ),

            "fuel_type": get_category_value(
                "fuel_type",
                index=0,
            ),

            "transmission": get_category_value(
                "transmission",
                index=0,
            ),

            "year": 2019,

            "engine_size": 3.0,

            "mileage": 70000,

            "current_price": 30000,
        },
    },


    # --------------------------------------------------------
    # 7
    # --------------------------------------------------------

    {
        "name": "Неповні вхідні дані",
        "note": (
            "не заповнено пробіг та поточну ціну автомобіля"
        ),

        "expected": "VALIDATION_ERROR",

        "data": {
            "brand": get_category_value(
                "brand",
                index=0,
            ),

            "model": get_category_value(
                "model",
                index=0,
            ),

            "fuel_type": get_category_value(
                "fuel_type",
                index=0,
            ),

            "transmission": get_category_value(
                "transmission",
                index=0,
            ),

            "year": 2018,

            "engine_size": 2.0,

            "mileage": "",

            "current_price": "",
        },
    },


    # --------------------------------------------------------
    # 8
    # --------------------------------------------------------

    {
        "name": "Некоректні вхідні дані",
        "note": (
            "від'ємний пробіг, некоректний рік "
            "та текстове значення ціни"
        ),

        "expected": "VALIDATION_ERROR",

        "data": {
            "brand": get_category_value(
                "brand",
                index=0,
            ),

            "model": get_category_value(
                "model",
                index=0,
            ),

            "fuel_type": get_category_value(
                "fuel_type",
                index=0,
            ),

            "transmission": get_category_value(
                "transmission",
                index=0,
            ),

            "year": 1900,

            "engine_size": -2,

            "mileage": -5000,

            "current_price": "дешево",
        },
    },
]


# ============================================================
# ВИВЕДЕННЯ ВХІДНИХ ДАНИХ
# ============================================================

def print_car_data(data):

    print(
        f"  Марка:             "
        f"{data.get('brand', '—')}"
    )

    print(
        f"  Модель:            "
        f"{data.get('model', '—')}"
    )

    print(
        f"  Тип палива:        "
        f"{data.get('fuel_type', '—')}"
    )

    print(
        f"  Коробка передач:   "
        f"{data.get('transmission', '—')}"
    )

    print(
        f"  Рік випуску:       "
        f"{data.get('year', '—')}"
    )

    print(
        f"  Об'єм двигуна:     "
        f"{data.get('engine_size', '—')} л"
    )

    print(
        f"  Пробіг:            "
        f"{data.get('mileage', '—')} км"
    )

    print(
        f"  Поточна ціна:      "
        f"{data.get('current_price', '—')}"
    )


# ============================================================
# ВИКОНАННЯ ОДНОГО СЦЕНАРІЮ
# ============================================================

def run_scenario(
    number,
    scenario,
    ai,
):
    print("=" * 82)

    print(
        f"СЦЕНАРІЙ {number}: "
        f"{scenario['name']}"
    )

    print(
        f"({scenario['note']})"
    )

    print("=" * 82)


    # --------------------------------------------------------
    # Вхідні дані
    # --------------------------------------------------------

    data = scenario["data"]

    print("\nВхідні дані:")

    print_car_data(
        data
    )


    # --------------------------------------------------------
    # Аналіз
    # --------------------------------------------------------

    try:

        result = core.analyze(
            data,
            ai,
        )

    except Exception as error:

        print(
            "\nПОМИЛКА ВИКОНАННЯ:"
        )

        print(
            f"  {error}"
        )

        return {
            "number": number,
            "name": scenario["name"],
            "predicted": "—",
            "current": "—",
            "delta": "—",
            "decision": "ERROR",
            "confidence": "—",
            "expected": scenario["expected"] or "будь-яке",
            "match": "ні",
        }


    # ========================================================
    # ПОМИЛКА ВАЛІДАЦІЇ
    # ========================================================

    if not result["ok"]:

        print(
            "\nРезультат валідації: "
            "ДАНІ ВІДХИЛЕНО"
        )

        print("\nЗнайдені помилки:")

        for index, message in enumerate(
            result["errors"],
            start=1,
        ):

            print(
                f"  {index}. {message}"
            )


        print(
            "\nAI-компонент не викликався, "
            "рекомендація не формується."
        )


        actual = "VALIDATION_ERROR"

        expected = scenario["expected"]

        if expected is None:

            match = "—"

        elif expected == actual:

            match = "так"

        else:

            match = "ні"


        print(
            f"\nЧас оброблення: "
            f"{result['elapsed_ms']:.2f} мс"
        )

        print()


        return {
            "number": number,

            "name": scenario["name"],

            "predicted": "—",

            "current": "—",

            "delta": "—",

            "decision": "VALIDATION_ERROR",

            "confidence": "—",

            "expected": expected or "будь-яке",

            "match": match,
        }


    # ========================================================
    # КОРЕКТНІ ДАНІ
    # ========================================================

    print(
        "\nРезультат валідації: "
        "дані коректні"
    )

    print(
        f"AI-компонент: "
        f"{result['model_name']}"
    )


    print(
        f"Прогнозована ринкова вартість: "
        f"{result['predicted_price']:.2f}"
    )


    print(
        f"Поточна ціна:                 "
        f"{result['current_price']:.2f}"
    )


    print(
        f"Відхилення: "
        f"{result['delta']:+.2f} "
        f"({result['delta_percent']:+.2f}%)"
    )


    print(
        f"Впевненість: "
        f"{result['confidence']:.2f} "
        f"({result['confidence_level']})"
    )


    # ========================================================
    # РЕКОМЕНДАЦІЯ
    # ========================================================

    print(
        f"\nРЕКОМЕНДАЦІЯ: "
        f"{result['decision_title']} "
        f"[{result['decision']}]"
    )

    print(
        f"  {result['decision_text']}"
    )

    print(
        f"  {result['decision_mode']}"
    )


    # ========================================================
    # СИСТЕМНЕ ПОЯСНЕННЯ
    # ========================================================

    print(
        "\nСистемне пояснення:"
    )

    for line in result[
        "explanation"
    ]["system"]:

        print(
            f"  - {line}"
        )


    # ========================================================
    # ПОЯСНЕННЯ ФАКТОРІВ
    # ========================================================

    print(
        "\nПояснення впливу ознак:"
    )

    for line in result[
        "explanation"
    ]["factors"]:

        print(
            f"  - {line}"
        )


    # ========================================================
    # ДІЇ КОРИСТУВАЧА
    # ========================================================

    print(
        "\nВаріанти дій користувача:"
    )

    for action in result[
        "actions"
    ]:

        print(
            f"  [ ] {action}"
        )


    print(
        f"\nЧас оброблення: "
        f"{result['elapsed_ms']:.2f} мс"
    )

    print()


    # ========================================================
    # ПОРІВНЯННЯ З ОЧІКУВАНИМ РЕЗУЛЬТАТОМ
    # ========================================================

    expected = scenario[
        "expected"
    ]


    if expected is None:

        match = "—"

    elif expected == result[
        "decision"
    ]:

        match = "так"

    else:

        match = "ні"


    return {

        "number": number,

        "name": scenario[
            "name"
        ],

        "predicted": (
            f"{result['predicted_price']:.0f}"
        ),

        "current": (
            f"{result['current_price']:.0f}"
        ),

        "delta": (
            f"{result['delta_percent']:+.2f}%"
        ),

        "decision": result[
            "decision"
        ],

        "confidence": (
            f"{result['confidence']:.2f}"
        ),

        "expected": (
            expected
            or "будь-яке"
        ),

        "match": match,
    }


# ============================================================
# ЗВЕДЕНА ТАБЛИЦЯ
# ============================================================

def print_summary(rows):

    print()
    print("=" * 100)

    print(
        "ЗВЕДЕНА ТАБЛИЦЯ "
        "РЕЗУЛЬТАТІВ ТЕСТУВАННЯ"
    )

    print("=" * 100)


    header = (
        f"{'№':<3}"
        f"{'Сценарій':<36}"
        f"{'Прогноз':>12}"
        f"{'Ціна':>12}"
        f"{'Δ%':>10}"
        f"{'Рішення':>24}"
        f"{'Впевн.':>9}"
        f"{'Збіг':>7}"
    )


    print(
        header
    )

    print(
        "-" * len(header)
    )


    for row in rows:

        print(

            f"{row['number']:<3}"

            f"{row['name'][:35]:<36}"

            f"{row['predicted']:>12}"

            f"{row['current']:>12}"

            f"{row['delta']:>10}"

            f"{row['decision']:>24}"

            f"{row['confidence']:>9}"

            f"{row['match']:>7}"
        )


    print(
        "-" * len(header)
    )


    # ========================================================
    # СТАТИСТИКА
    # ========================================================

    checked = [
        row
        for row in rows
        if row["match"] != "—"
    ]


    passed = [
        row
        for row in checked
        if row["match"] == "так"
    ]


    print()

    print(
        "СТАТИСТИКА:"
    )

    print(
        f"  Усього сценаріїв: "
        f"{len(rows)}"
    )

    print(
        f"  Сценаріїв із фіксованим "
        f"очікуваним результатом: "
        f"{len(checked)}"
    )

    print(
        f"  Успішно пройдено: "
        f"{len(passed)}"
    )

    print(
        f"  Не пройдено: "
        f"{len(checked) - len(passed)}"
    )


    print()

    print(
        "Сценарії 4–6 не мають "
        "жорстко заданого очікуваного рішення."
    )

    print(
        "Для них перевіряється коректність "
        "валідації, прогнозування та формування "
        "рекомендації системою."
    )


# ============================================================
# ПЕРЕВІРКА КОНФІГУРАЦІЇ
# ============================================================

def print_configuration(ai):

    print(
        "КОНФІГУРАЦІЯ IDSS"
    )

    print(
        "-" * 60
    )

    print(
        f"AI-компонент: "
        f"{ai.name}"
    )

    print(
        f"MAE моделі:   "
        f"{ai.mae:.2f}"
    )

    print(
        f"Поріг вигідної ціни: "
        f"{core.BUY_THRESHOLD:.0f}%"
    )

    print(
        f"Поріг завищеної ціни: "
        f"+{core.WAIT_THRESHOLD:.0f}%"
    )

    print()

    print(
        "Ознаки моделі:"
    )

    for column in core.FEATURE_COLUMNS:

        print(
            f"  - {column}"
        )

    print()

    print(
        f"Цільова змінна: "
        f"{core.TARGET_COLUMN}"
    )

    print()

    print(
        "Категоріальні ознаки:"
    )

    for column in core.CATEGORICAL_COLUMNS:

        print(
            f"  - {column}"
        )

    print()

    print(
        "Числові ознаки:"
    )

    for column in core.NUMERIC_COLUMNS:

        print(
            f"  - {column}"
        )

    print()


# ============================================================
# MAIN
# ============================================================

def main():

    print()

    print(
        "=" * 82
    )

    print(
        "ТЕСТУВАННЯ ПРОТОТИПУ IDSS"
    )

    print(
        "ЛАБОРАТОРНА РОБОТА №4"
    )

    print(
        "Оцінювання ринкової вартості "
        "та вигідності пропозицій "
        "вживаних автомобілів"
    )

    print(
        "=" * 82
    )

    print()


    # --------------------------------------------------------
    # AI-компонент
    # --------------------------------------------------------

    ai = core.AIComponent()


    # --------------------------------------------------------
    # Конфігурація
    # --------------------------------------------------------

    print_configuration(
        ai
    )


    # --------------------------------------------------------
    # Виконання тестів
    # --------------------------------------------------------

    rows = []


    for number, scenario in enumerate(
        SCENARIOS,
        start=1,
    ):

        rows.append(
            run_scenario(
                number,
                scenario,
                ai,
            )
        )


    # --------------------------------------------------------
    # Зведена таблиця
    # --------------------------------------------------------

    print_summary(
        rows
    )


    print()

    print(
        "=" * 82
    )

    print(
        "ТЕСТУВАННЯ ЗАВЕРШЕНО"
    )

    print(
        "=" * 82
    )


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    main()