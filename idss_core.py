"""
ЛАБОРАТОРНА РОБОТА №4
Прототип інтелектуальної системи підтримки прийняття рішень (IDSS)

Предметна область:
Оцінювання ринкової вартості та аналіз вигідності пропозицій
під час купівлі вживаних автомобілів.

Структура системи:
    1) модуль валідації вхідних даних;
    2) модуль попереднього оброблення;
    3) AI-компонент — Linear Regression;
    4) модуль інтерпретації результату;
    5) модуль формування рекомендації;
    6) модуль пояснення результату;
    7) журналювання рішення користувача.

Джерела даних:
    - Car_Price_Prediction.csv
    - metadata.json
    - linear_regression.joblib
"""

import json
import time
from pathlib import Path

import joblib
import pandas as pd


# ============================================================
# ШЛЯХИ
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "Car_Price_Prediction.csv"
METADATA_PATH = BASE_DIR / "metadata.json"

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "linear_regression.joblib"
)

RESULTS_PATH = BASE_DIR / "model_results.csv"

DECISIONS_LOG_PATH = (
    BASE_DIR / "decisions_log.csv"
)


# ============================================================
# НАЛАШТУВАННЯ IDSS
# ============================================================

# Якщо поточна ціна нижча за прогнозовану
# на 10% і більше → вигідна пропозиція.
BUY_THRESHOLD = -10.0

# Якщо поточна ціна вища за прогнозовану
# на 15% і більше → ціна завищена.
WAIT_THRESHOLD = 15.0

CONFIDENCE_HIGH = 0.80
CONFIDENCE_LOW = 0.50

DEFAULT_MAE = 1000.0

# Окреме поле GUI.
# Воно НЕ входить до ознак Linear Regression.
CURRENT_PRICE_COLUMN = "current_price"


# ============================================================
# НАЗВИ ПОЛІВ
# ============================================================

FIELD_LABELS = {

    "brand":
        "Марка автомобіля",

    "model":
        "Модель",

    "fuel_type":
        "Тип палива",

    "transmission":
        "Коробка передач",

    "year":
        "Рік випуску",

    "engine_size":
        "Об'єм двигуна, л",

    "mileage":
        "Пробіг, км",

    "current_price":
        "Поточна ціна автомобіля",

    "price":
        "Ринкова вартість",
}


# ============================================================
# РІШЕННЯ СИСТЕМИ
# ============================================================

DECISION_TITLES = {

    "BUY_NOW":
        "ВИГІДНА ПРОПОЗИЦІЯ",

    "MARKET_FAIR_PRICE":
        "ЦІНА ВІДПОВІДАЄ РИНКУ",

    "WAIT_BETTER_PRICE":
        "ЦІНА ЗАВИЩЕНА",
}


DECISION_TEXTS = {

    "BUY_NOW": (
        "Поточна ціна автомобіля нижча за прогнозовану "
        "моделлю ринкову вартість. Пропозиція може бути "
        "вигідною для покупця."
    ),

    "MARKET_FAIR_PRICE": (
        "Поточна ціна автомобіля близька до прогнозованої "
        "ринкової вартості. Ціна загалом відповідає "
        "очікуваному рівню."
    ),

    "WAIT_BETTER_PRICE": (
        "Поточна ціна автомобіля суттєво перевищує "
        "прогнозовану ринкову вартість. Рекомендується "
        "порівняти інші пропозиції або дочекатися "
        "нижчої ціни."
    ),
}


# ============================================================
# РОБОТА З METADATA.JSON
# ============================================================

def load_metadata():
    """
    Завантажує metadata.json.
    """

    if not METADATA_PATH.exists():
        return {}

    try:

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except Exception:

        return {}


METADATA = load_metadata()


# ============================================================
# ВИЗНАЧЕННЯ ОЗНАК
# ============================================================

def get_feature_columns():
    """
    Отримує список ознак із metadata.json.

    Для поточного датасету:

        brand
        model
        fuel_type
        transmission
        year
        engine_size
        mileage

    current_price сюди НЕ входить.
    """

    for key in (
        "feature_columns",
        "features",
        "feature_names",
        "input_features",
    ):

        value = METADATA.get(key)

        if (
            isinstance(value, list)
            and value
        ):

            return value

    # Резервний варіант:
    # отримання колонок із датасету.

    if DATASET_PATH.exists():

        try:

            data = pd.read_csv(
                DATASET_PATH
            )

            target = get_target_column()

            return [
                column
                for column in data.columns
                if column != target
            ]

        except Exception:

            pass

    return []


def get_target_column():
    """
    Отримує назву цільової змінної.
    """

    for key in (
        "target_column",
        "target",
        "target_variable",
        "y_column",
    ):

        value = METADATA.get(key)

        if (
            isinstance(value, str)
            and value
        ):

            return value

    possible_targets = [
        "price",
        "Price",
        "selling_price",
        "Selling_Price",
    ]

    if DATASET_PATH.exists():

        try:

            data = pd.read_csv(
                DATASET_PATH
            )

            for target in possible_targets:

                if target in data.columns:

                    return target

        except Exception:

            pass

    return "price"


def get_categorical_columns():
    """
    Отримує категоріальні ознаки
    з metadata.json.
    """

    for key in (
        "categorical_columns",
        "categorical_features",
        "categorical",
    ):

        value = METADATA.get(key)

        if isinstance(value, list):

            return value

    return []


def get_numeric_columns():
    """
    Отримує числові ознаки
    з metadata.json.
    """

    for key in (
        "numeric_columns",
        "numeric_features",
        "numerical_columns",
        "numerical_features",
    ):

        value = METADATA.get(key)

        if isinstance(value, list):

            return value

    return []


FEATURE_COLUMNS = get_feature_columns()

TARGET_COLUMN = get_target_column()

CATEGORICAL_COLUMNS = (
    get_categorical_columns()
)

NUMERIC_COLUMNS = (
    get_numeric_columns()
)


# ============================================================
# КАТЕГОРІЇ
# ============================================================

CATEGORIES = {}


def load_categories():
    """
    Завантажує допустимі категорії
    з metadata.json.
    """

    metadata_categories = (
        METADATA.get(
            "categories",
            {},
        )
    )

    if isinstance(
        metadata_categories,
        dict,
    ):

        for column, values in (
            metadata_categories.items()
        ):

            if isinstance(
                values,
                list,
            ):

                CATEGORIES[column] = values


load_categories()


# ============================================================
# ЧИСЛОВІ ДІАПАЗОНИ
# ============================================================

NUMERIC_RANGES = (
    METADATA.get(
        "numeric_ranges",
        {},
    )
)


def get_numeric_range(column):
    """
    Повертає допустимий діапазон
    числової ознаки.
    """

    if column in NUMERIC_RANGES:

        values = NUMERIC_RANGES[column]

        if isinstance(
            values,
            dict,
        ):

            minimum = values.get(
                "min"
            )

            maximum = values.get(
                "max"
            )

            if (
                minimum is not None
                and maximum is not None
            ):

                return (
                    float(minimum),
                    float(maximum),
                )

    # Якщо діапазон відсутній
    # у metadata — беремо його з датасету.

    if DATASET_PATH.exists():

        try:

            data = pd.read_csv(
                DATASET_PATH
            )

            # metadata використовує
            # внутрішні назви полів,
            # тому для цього датасету
            # виконуємо відповідність назв.

            dataset_column_map = {

                "brand": "Make",

                "model": "Model",

                "year": "Year",

                "engine_size": "Engine Size",

                "mileage": "Mileage",

                "fuel_type": "Fuel Type",

                "transmission": "Transmission",

                "price": "Price",
            }

            dataset_column = (
                dataset_column_map.get(
                    column,
                    column,
                )
            )

            if dataset_column in data.columns:

                numeric = pd.to_numeric(
                    data[dataset_column],
                    errors="coerce",
                ).dropna()

                if not numeric.empty:

                    return (
                        float(numeric.min()),
                        float(numeric.max()),
                    )

        except Exception:

            pass

    return None, None


# ============================================================
# МОДУЛЬ ВАЛІДАЦІЇ
# ============================================================

def validate_input(raw):
    """
    Перевірка вхідних даних користувача.

    Перевіряються:
        - усі ознаки моделі;
        - категоріальні значення;
        - числові значення;
        - поточна ціна автомобіля.

    current_price не входить до моделі,
    але використовується для порівняння
    з прогнозованою ціною.
    """

    errors = []

    clean = {}


    # ========================================================
    # 1. Перевірка ознак моделі
    # ========================================================

    for column in FEATURE_COLUMNS:

        value = raw.get(column)

        if (
            value is None
            or str(value).strip() == ""
        ):

            errors.append(
                "Не заповнено обов'язкове поле: "
                f"{FIELD_LABELS.get(column, column)}."
            )


    # ========================================================
    # 2. Перевірка поточної ціни
    # ========================================================

    current_price_text = raw.get(
        CURRENT_PRICE_COLUMN
    )

    if (
        current_price_text is None
        or str(current_price_text).strip() == ""
    ):

        errors.append(
            "Не заповнено обов'язкове поле: "
            "Поточна ціна автомобіля."
        )

    else:

        text = (
            str(current_price_text)
            .strip()
            .replace(",", ".")
        )

        try:

            current_price = float(
                text
            )

            if current_price <= 0:

                errors.append(
                    "Поточна ціна автомобіля "
                    "повинна бути більшою за 0."
                )

            else:

                clean[
                    CURRENT_PRICE_COLUMN
                ] = current_price

        except ValueError:

            errors.append(
                "Поточна ціна автомобіля: "
                f"значення «{text}» "
                "не є числом."
            )


    # Якщо вже є помилки обов'язкових полів,
    # все одно перевіряємо інші поля,
    # щоб користувач отримав повний список.

    # ========================================================
    # 3. Категоріальні ознаки
    # ========================================================

    for column in CATEGORICAL_COLUMNS:

        if column not in raw:

            continue

        value = str(
            raw[column]
        ).strip()

        if value == "":

            continue

        allowed_values = (
            CATEGORIES.get(
                column,
                [],
            )
        )

        if allowed_values:

            if value not in allowed_values:

                errors.append(
                    f"{FIELD_LABELS.get(column, column)}: "
                    f"невідоме значення «{value}». "
                    f"Допустимі: "
                    + ", ".join(
                        map(
                            str,
                            allowed_values,
                        )
                    )
                    + "."
                )

            else:

                clean[column] = value

        else:

            clean[column] = value


    # ========================================================
    # 4. Числові ознаки
    # ========================================================

    for column in NUMERIC_COLUMNS:

        if column not in raw:

            continue

        text = (
            str(raw[column])
            .strip()
            .replace(",", ".")
        )

        if text == "":

            continue

        try:

            value = float(text)

        except ValueError:

            errors.append(
                f"{FIELD_LABELS.get(column, column)}: "
                f"значення «{text}» "
                "не є числом."
            )

            continue

        minimum, maximum = (
            get_numeric_range(
                column
            )
        )

        if (
            minimum is not None
            and maximum is not None
        ):

            if not (
                minimum
                <= value
                <= maximum
            ):

                errors.append(
                    f"{FIELD_LABELS.get(column, column)} "
                    f"повинно бути в межах "
                    f"{minimum:.2f}–{maximum:.2f}. "
                    f"Введено: {value:.2f}."
                )

                continue

        clean[column] = value


    # ========================================================
    # Результат
    # ========================================================

    if errors:

        return errors, {}

    return [], clean


# ============================================================
# МОДУЛЬ ПОПЕРЕДНЬОГО ОБРОБЛЕННЯ
# ============================================================

def preprocess(clean):

    row = {}

    for column in FEATURE_COLUMNS:

        row[column] = clean[column]

    return pd.DataFrame(
        [row],
        columns=FEATURE_COLUMNS,
    )


# ============================================================
# AI-КОМПОНЕНТ
# ============================================================

class AIComponent:

    def __init__(self):

        self.model = None

        self.name = (
            "Linear Regression "
            "(модель не завантажена)"
        )

        self.mae = DEFAULT_MAE

        self.is_real_model = False

        self.load_model()

        self.load_mae()


    # ========================================================
    # ЗАВАНТАЖЕННЯ МОДЕЛІ
    # ========================================================

    def load_model(self):

        if not MODEL_PATH.exists():

            return

        try:

            self.model = joblib.load(
                MODEL_PATH
            )

            self.name = (
                "Linear Regression"
            )

            self.is_real_model = True

        except Exception:

            self.model = None


    # ========================================================
    # ЗАВАНТАЖЕННЯ MAE
    # ========================================================

    def load_mae(self):

        if not RESULTS_PATH.exists():

            return

        try:

            results = pd.read_csv(
                RESULTS_PATH
            )


            # -----------------------------------------------
            # Варіант 1:
            # Model
            # -----------------------------------------------

            if "Model" in results.columns:

                rows = results[
                    results["Model"]
                    .astype(str)
                    .str.contains(
                        "Linear Regression",
                        case=False,
                        na=False,
                    )
                ]

                if not rows.empty:

                    if "MAE" in rows.columns:

                        self.mae = float(
                            rows.iloc[0]["MAE"]
                        )

                        return


            # -----------------------------------------------
            # Варіант 2:
            # model
            # -----------------------------------------------

            if "model" in results.columns:

                rows = results[
                    results["model"]
                    .astype(str)
                    .str.contains(
                        "Linear Regression",
                        case=False,
                        na=False,
                    )
                ]

                if not rows.empty:

                    if "MAE" in rows.columns:

                        self.mae = float(
                            rows.iloc[0]["MAE"]
                        )

                        return

        except Exception:

            pass


    # ========================================================
    # ПРОГНОЗ
    # ========================================================

    def predict(self, features):

        if self.model is None:

            raise RuntimeError(
                "Модель Linear Regression "
                "не знайдена.\n\n"
                "Очікуваний файл:\n"
                f"{MODEL_PATH}"
            )

        try:

            prediction = (
                self.model.predict(
                    features
                )
            )

            return float(
                prediction[0]
            )

        except Exception as error:

            raise RuntimeError(
                "Помилка під час прогнозування: "
                f"{error}"
            )


# ============================================================
# МОДУЛЬ ІНТЕРПРЕТАЦІЇ
# ============================================================

def interpret(
    current_price,
    predicted_price,
    mae,
):

    if predicted_price <= 0:

        return {

            "delta": 0.0,

            "delta_percent": 0.0,

            "confidence": 0.0,

            "confidence_level": "низька",
        }


    # --------------------------------------------------------
    # Різниця між цінами
    # --------------------------------------------------------

    delta = (
        current_price
        - predicted_price
    )


    # --------------------------------------------------------
    # Відхилення у відсотках
    # --------------------------------------------------------

    delta_percent = (
        delta
        / predicted_price
    ) * 100.0


    # --------------------------------------------------------
    # Оцінка впевненості
    # --------------------------------------------------------

    if mae <= 0:

        mae = DEFAULT_MAE

    confidence = (
        0.35
        + 0.30
        * (
            abs(delta)
            / mae
        )
    )

    confidence = min(
        0.95,
        round(
            confidence,
            2,
        ),
    )


    if confidence >= CONFIDENCE_HIGH:

        confidence_level = (
            "висока"
        )

    elif confidence >= CONFIDENCE_LOW:

        confidence_level = (
            "середня"
        )

    else:

        confidence_level = (
            "низька"
        )


    return {

        "delta": round(
            delta,
            2,
        ),

        "delta_percent": round(
            delta_percent,
            2,
        ),

        "confidence": confidence,

        "confidence_level":
            confidence_level,
    }


# ============================================================
# МОДУЛЬ ФОРМУВАННЯ РЕКОМЕНДАЦІЇ
# ============================================================

def make_recommendation(
    delta_percent,
    confidence,
):

    # --------------------------------------------------------
    # Основне правило
    # --------------------------------------------------------

    if delta_percent <= BUY_THRESHOLD:

        code = "BUY_NOW"

    elif delta_percent >= WAIT_THRESHOLD:

        code = "WAIT_BETTER_PRICE"

    else:

        code = "MARKET_FAIR_PRICE"


    # --------------------------------------------------------
    # Режим рекомендації
    # --------------------------------------------------------

    if confidence >= CONFIDENCE_HIGH:

        mode = (
            "Рекомендація сформована "
            "автоматично на основі "
            "прогнозу Linear Regression."
        )

    elif confidence >= CONFIDENCE_LOW:

        mode = (
            "Рекомендується додатковий аналіз, "
            "оскільки відхилення ціни "
            "співмірне з похибкою моделі."
        )

    else:

        mode = (
            "Впевненість низька. "
            "Остаточне рішення залишається "
            "за користувачем."
        )


    # --------------------------------------------------------
    # Доступні дії
    # --------------------------------------------------------

    actions = {

        "BUY_NOW": [

            "Розглянути купівлю автомобіля",

            "Порівняти з аналогічними "
            "пропозиціями",

            "Відхилити рекомендацію",
        ],

        "MARKET_FAIR_PRICE": [

            "Розглянути купівлю автомобіля",

            "Порівняти з іншими "
            "автомобілями",

            "Відхилити рекомендацію",
        ],

        "WAIT_BETTER_PRICE": [

            "Пошукати дешевші "
            "аналогічні автомобілі",

            "Перевірити ціну пізніше",

            "Купити автомобіль попри "
            "завищену ціну",
        ],
    }


    return {

        "decision": code,

        "title":
            DECISION_TITLES[code],

        "text":
            DECISION_TEXTS[code],

        "mode": mode,

        "actions":
            actions[code],
    }


# ============================================================
# МОДУЛЬ ПОЯСНЕННЯ
# ============================================================

def explain(
    clean,
    predicted_price,
    analysis,
    recommendation,
    model_name,
):
    """
    Формує пояснення результату
    для користувача.
    """

    system_lines = []


    # --------------------------------------------------------
    # Поточна ціна
    # --------------------------------------------------------

    current_price = clean.get(
        CURRENT_PRICE_COLUMN
    )

    if current_price is None:

        current_price = predicted_price


    # --------------------------------------------------------
    # Основний результат
    # --------------------------------------------------------

    system_lines.append(
        f"AI-компонент ({model_name}) "
        f"спрогнозував ринкову вартість "
        f"{predicted_price:,.2f}."
    )

    system_lines.append(
        f"Поточна ціна автомобіля "
        f"становить {current_price:,.2f}."
    )

    system_lines.append(
        f"Відхилення поточної ціни "
        f"від прогнозу: "
        f"{analysis['delta']:,.2f} "
        f"({analysis['delta_percent']:+.2f}%)."
    )


    # --------------------------------------------------------
    # Правило рекомендації
    # --------------------------------------------------------

    if (
        recommendation["decision"]
        == "BUY_NOW"
    ):

        system_lines.append(
            "Поточна ціна нижча за "
            "прогнозовану ринкову "
            f"на {abs(analysis['delta_percent']):.2f}%."
        )

        system_lines.append(
            f"Спрацювало правило: "
            f"{analysis['delta_percent']:+.2f}% "
            f"<= {BUY_THRESHOLD:.0f}%."
        )


    elif (
        recommendation["decision"]
        == "WAIT_BETTER_PRICE"
    ):

        system_lines.append(
            "Поточна ціна перевищує "
            "прогнозовану ринкову "
            f"вартість на "
            f"{analysis['delta_percent']:.2f}%."
        )

        system_lines.append(
            f"Спрацювало правило: "
            f"{analysis['delta_percent']:+.2f}% "
            f">= +{WAIT_THRESHOLD:.0f}%."
        )


    else:

        system_lines.append(
            "Відхилення поточної ціни "
            "знаходиться в межах "
            f"{BUY_THRESHOLD:.0f}% ... "
            f"+{WAIT_THRESHOLD:.0f}%."
        )

        system_lines.append(
            "Ціна вважається близькою "
            "до прогнозованої ринкової "
            "вартості."
        )


    # --------------------------------------------------------
    # Впевненість
    # --------------------------------------------------------

    system_lines.append(
        f"Впевненість оцінки: "
        f"{analysis['confidence']:.2f} "
        f"({analysis['confidence_level']})."
    )


    # ========================================================
    # ФАКТОРИ
    # ========================================================

    factor_lines = []

    for column in FEATURE_COLUMNS:

        if column not in clean:

            continue

        label = FIELD_LABELS.get(
            column,
            column,
        )

        value = clean[column]

        if column == "mileage":

            value = (
                f"{value:,.0f} км"
            )

        elif column == "engine_size":

            value = (
                f"{value:.1f} л"
            )

        elif column == "year":

            value = (
                f"{value:.0f}"
            )

        factor_lines.append(
            f"{label}: {value}."
        )


    return {

        "system":
            system_lines,

        "factors":
            factor_lines,
    }


# ============================================================
# ПОТОЧНА ЦІНА
# ============================================================

def get_current_price(clean):
    """
    Отримує поточну ціну автомобіля.

    Вона використовується тільки
    для порівняння з прогнозом.

    У Linear Regression вона НЕ передається.
    """

    value = clean.get(
        CURRENT_PRICE_COLUMN
    )

    if value is None:

        return None

    return float(value)


# ============================================================
# НАСКРІЗНИЙ АНАЛІЗ
# ============================================================

def analyze(
    raw,
    ai_component=None,
):
    """
    Повний сценарій роботи IDSS:

        Вхідні дані
             ↓
        Валідація
             ↓
        Preprocessing
             ↓
        Linear Regression
             ↓
        Порівняння цін
             ↓
        Інтерпретація
             ↓
        Бізнес-правила
             ↓
        Пояснення
    """

    start = time.perf_counter()


    # --------------------------------------------------------
    # AI-компонент
    # --------------------------------------------------------

    if ai_component is None:

        ai_component = AIComponent()


    # --------------------------------------------------------
    # Валідація
    # --------------------------------------------------------

    errors, clean = validate_input(
        raw
    )

    if errors:

        return {

            "ok": False,

            "errors": errors,

            "elapsed_ms": (
                time.perf_counter()
                - start
            ) * 1000,
        }


    # --------------------------------------------------------
    # Preprocessing
    # --------------------------------------------------------

    try:

        features = preprocess(
            clean
        )

    except Exception as error:

        return {

            "ok": False,

            "errors": [
                "Помилка попереднього "
                f"оброблення даних: {error}"
            ],

            "elapsed_ms": (
                time.perf_counter()
                - start
            ) * 1000,
        }


    # --------------------------------------------------------
    # Поточна ціна
    # --------------------------------------------------------

    current_price = (
        get_current_price(
            clean
        )
    )

    if current_price is None:

        return {

            "ok": False,

            "errors": [
                "Не знайдено поле "
                "поточної ціни автомобіля."
            ],

            "elapsed_ms": (
                time.perf_counter()
                - start
            ) * 1000,
        }


    # --------------------------------------------------------
    # AI prediction
    # --------------------------------------------------------

    try:

        predicted_price = (
            ai_component.predict(
                features
            )
        )

    except Exception as error:

        return {

            "ok": False,

            "errors": [
                str(error)
            ],

            "elapsed_ms": (
                time.perf_counter()
                - start
            ) * 1000,
        }


    # --------------------------------------------------------
    # Захист від некоректного прогнозу
    # --------------------------------------------------------

    predicted_price = max(
        0.0,
        predicted_price,
    )


    # --------------------------------------------------------
    # Інтерпретація
    # --------------------------------------------------------

    analysis = interpret(

        current_price,

        predicted_price,

        ai_component.mae,
    )


    # --------------------------------------------------------
    # Рекомендація
    # --------------------------------------------------------

    recommendation = (
        make_recommendation(

            analysis[
                "delta_percent"
            ],

            analysis[
                "confidence"
            ],
        )
    )


    # --------------------------------------------------------
    # Пояснення
    # --------------------------------------------------------

    explanation = explain(

        clean,

        predicted_price,

        analysis,

        recommendation,

        ai_component.name,
    )


    # --------------------------------------------------------
    # Фінальний результат
    # --------------------------------------------------------

    return {

        "ok": True,

        "errors": [],

        "clean": clean,

        "features": features,

        "model_name":
            ai_component.name,

        "predicted_price":
            round(
                predicted_price,
                2,
            ),

        "current_price":
            round(
                current_price,
                2,
            ),

        "delta":
            analysis["delta"],

        "delta_percent":
            analysis[
                "delta_percent"
            ],

        "confidence":
            analysis["confidence"],

        "confidence_level":
            analysis[
                "confidence_level"
            ],

        "decision":
            recommendation[
                "decision"
            ],

        "decision_title":
            recommendation[
                "title"
            ],

        "decision_text":
            recommendation[
                "text"
            ],

        "decision_mode":
            recommendation[
                "mode"
            ],

        "actions":
            recommendation[
                "actions"
            ],

        "explanation":
            explanation,

        "elapsed_ms":
            (
                time.perf_counter()
                - start
            ) * 1000,
    }


# ============================================================
# ЛОГУВАННЯ РІШЕННЯ КОРИСТУВАЧА
# ============================================================

def save_user_decision(
    result,
    user_action,
):
    """
    Зберігає остаточне рішення користувача
    у decisions_log.csv.
    """

    clean = result["clean"]


    record = {

        "time":
            time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

        "model":
            result["model_name"],

        "predicted_price":
            result["predicted_price"],

        "current_price":
            result["current_price"],

        "delta_percent":
            result["delta_percent"],

        "confidence":
            result["confidence"],

        "ai_recommendation":
            result["decision"],

        "user_decision":
            user_action,
    }


    # --------------------------------------------------------
    # Характеристики автомобіля
    # --------------------------------------------------------

    for column in FEATURE_COLUMNS:

        if column in clean:

            record[column] = (
                clean[column]
            )


    # --------------------------------------------------------
    # DataFrame
    # --------------------------------------------------------

    frame = pd.DataFrame(
        [record]
    )


    # --------------------------------------------------------
    # Збереження
    # --------------------------------------------------------

    frame.to_csv(

        DECISIONS_LOG_PATH,

        mode="a",

        header=(
            not DECISIONS_LOG_PATH.exists()
        ),

        index=False,

        encoding="utf-8",
    )


    return DECISIONS_LOG_PATH