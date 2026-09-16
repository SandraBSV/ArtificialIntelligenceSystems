import json
import time
import sys
from pathlib import Path

import joblib
import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeRegressor


# ============================================================
# НАЛАШТУВАННЯ
# ============================================================

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "Car_Price_Prediction.csv"

MODELS_DIR = BASE_DIR / "models"

RESULTS_PATH = BASE_DIR / "model_results.csv"
PREDICTIONS_PATH = BASE_DIR / "validation_predictions.csv"
METADATA_PATH = BASE_DIR / "metadata.json"

RANDOM_STATE = 42


# ============================================================
# СТРУКТУРА ДАТАСЕТУ
# ============================================================

DATASET_COLUMNS = [
    "brand",
    "model",
    "year",
    "engine_size",
    "mileage",
    "fuel_type",
    "transmission",
    "price",
]


# Цільова змінна
TARGET_COLUMN = "price"


# Категоріальні ознаки
CATEGORICAL_COLUMNS = [
    "brand",
    "model",
    "fuel_type",
    "transmission",
]


# Числові ознаки
NUMERIC_COLUMNS = [
    "year",
    "engine_size",
    "mileage",
]


# Усі ознаки
FEATURE_COLUMNS = (
    CATEGORICAL_COLUMNS +
    NUMERIC_COLUMNS
)


# Назви файлів навчених моделей
MODEL_FILES = {
    "Linear Regression": "linear_regression.joblib",
    "Decision Tree Regressor": "decision_tree.joblib",
    "Random Forest Regressor": "random_forest.joblib",
}


# ============================================================
# ПІДГОТОВКА ДАНИХ
# ============================================================

def create_preprocessor():

    return ColumnTransformer(
        transformers=[
            (
                "categorical",
                OneHotEncoder(
                    handle_unknown="ignore"
                ),
                CATEGORICAL_COLUMNS,
            ),
            (
                "numeric",
                StandardScaler(),
                NUMERIC_COLUMNS,
            ),
        ]
    )


# ============================================================
# СТВОРЕННЯ МОДЕЛЕЙ
# ============================================================

def create_models():

    return {
        "Linear Regression": LinearRegression(),

        "Decision Tree Regressor": DecisionTreeRegressor(
            random_state=RANDOM_STATE,
            max_depth=15,
        ),

        "Random Forest Regressor": RandomForestRegressor(
            n_estimators=150,
            random_state=RANDOM_STATE,
            n_jobs=-1,
        ),
    }


# ============================================================
# ЗАВАНТАЖЕННЯ ДАТАСЕТУ
# ============================================================

def load_dataset():

    if not DATASET_PATH.exists():

        raise FileNotFoundError(
            f"\nНе знайдено файл: {DATASET_PATH.name}\n"
            f"Помістіть файл у папку:\n{BASE_DIR}"
        )


    df = pd.read_csv(
        DATASET_PATH,
        header=None,
        names=DATASET_COLUMNS,
    )


    # --------------------------------------------------------
    # Перевірка структури
    # --------------------------------------------------------

    if df.shape[1] != len(DATASET_COLUMNS):

        raise ValueError(
            "Кількість колонок у датасеті не відповідає "
            "очікуваній структурі."
        )


    # --------------------------------------------------------
    # Перетворення числових колонок
    # --------------------------------------------------------

    for column in NUMERIC_COLUMNS + [TARGET_COLUMN]:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce",
        )


    # --------------------------------------------------------
    # Видалення некоректних записів
    # --------------------------------------------------------

    before_cleaning = len(df)

    df = df.dropna(
        subset=FEATURE_COLUMNS + [TARGET_COLUMN]
    )

    removed_rows = before_cleaning - len(df)


    if removed_rows > 0:

        print(
            f"\nВидалено некоректних записів: "
            f"{removed_rows}"
        )


    # --------------------------------------------------------
    # Перевірка логічності значень
    # --------------------------------------------------------

    # Ціна повинна бути більшою за 0
    df = df[df[TARGET_COLUMN] > 0]

    # Рік автомобіля
    df = df[
        (df["year"] >= 1900) &
        (df["year"] <= 2100)
    ]

    # Об'єм двигуна
    df = df[df["engine_size"] > 0]

    # Пробіг
    df = df[df["mileage"] >= 0]


    # --------------------------------------------------------
    # Видалення дублікатів
    # --------------------------------------------------------

    duplicate_count = df.duplicated().sum()

    if duplicate_count > 0:

        print(
            f"Видалено дублікатів: "
            f"{duplicate_count}"
        )

        df = df.drop_duplicates()


    return df.reset_index(drop=True)


# ============================================================
# ОСНОВНА ФУНКЦІЯ
# ============================================================

def main():

    print("=" * 72)
    print(
        "USED CAR PRICE PREDICTION"
    )
    print(
        "НАВЧАННЯ МОДЕЛЕЙ ДЛЯ АВТОМОБІЛЬНОГО МАРКЕТПЛЕЙСУ"
    )
    print("=" * 72)


    # --------------------------------------------------------
    # Створення папки для моделей
    # --------------------------------------------------------

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )


    # --------------------------------------------------------
    # Завантаження даних
    # --------------------------------------------------------

    print("\nЗавантаження датасету...")

    df = load_dataset()


    print(
        f"Датасет успішно завантажено: "
        f"{DATASET_PATH.name}"
    )


    # --------------------------------------------------------
    # Загальна інформація
    # --------------------------------------------------------

    print("\n" + "-" * 72)
    print("ІНФОРМАЦІЯ ПРО ДАТАСЕТ")
    print("-" * 72)

    print(
        f"Кількість автомобілів: {len(df)}"
    )

    print(
        f"Кількість ознак: {len(FEATURE_COLUMNS)}"
    )

    print(
        f"Цільова змінна: {TARGET_COLUMN}"
    )


    # --------------------------------------------------------
    # Формування X та y
    # --------------------------------------------------------

    X = df[FEATURE_COLUMNS]

    y = df[TARGET_COLUMN]


    # --------------------------------------------------------
    # Розподіл даних
    # --------------------------------------------------------

    # 70% — навчання
    # 15% — validation
    # 15% — test

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y,
        test_size=0.30,
        random_state=RANDOM_STATE,
    )


    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=0.50,
        random_state=RANDOM_STATE,
    )


    print("\nРозподіл даних:")

    print(
        f"Train:       {len(X_train)} "
        f"({len(X_train) / len(df) * 100:.1f}%)"
    )

    print(
        f"Validation:  {len(X_val)} "
        f"({len(X_val) / len(df) * 100:.1f}%)"
    )

    print(
        f"Test:        {len(X_test)} "
        f"({len(X_test) / len(df) * 100:.1f}%)"
    )


    # --------------------------------------------------------
    # Таблиця для validation-прогнозів
    # --------------------------------------------------------

    validation_table = pd.DataFrame({

        "real_price":
            y_val.reset_index(drop=True)

    })


    # --------------------------------------------------------
    # Навчання моделей
    # --------------------------------------------------------

    results = []


    for model_name, estimator in create_models().items():

        print("\n" + "=" * 72)

        print(
            f"МОДЕЛЬ: {model_name}"
        )

        print("=" * 72)


        # ----------------------------------------------------
        # Pipeline
        # ----------------------------------------------------

        pipeline = Pipeline(
            steps=[
                (
                    "preprocessor",
                    create_preprocessor()
                ),

                (
                    "model",
                    estimator
                ),
            ]
        )


        # ----------------------------------------------------
        # Навчання
        # ----------------------------------------------------

        start_train = time.perf_counter()

        pipeline.fit(
            X_train,
            y_train
        )

        training_time = (
            time.perf_counter()
            - start_train
        )


        # ----------------------------------------------------
        # Прогнозування
        # ----------------------------------------------------

        start_predict = time.perf_counter()

        y_pred = pipeline.predict(
            X_val
        )

        prediction_time = (
            time.perf_counter()
            - start_predict
        )


        # ----------------------------------------------------
        # Метрики
        # ----------------------------------------------------

        mae = mean_absolute_error(
            y_val,
            y_pred
        )

        rmse = mean_squared_error(
            y_val,
            y_pred
        ) ** 0.5

        r2 = r2_score(
            y_val,
            y_pred
        )


        # ----------------------------------------------------
        # Збереження результатів
        # ----------------------------------------------------

        results.append({

            "Model":
                model_name,

            "Training Time (s)":
                training_time,

            "Prediction Time (s)":
                prediction_time,

            "MAE":
                mae,

            "RMSE":
                rmse,

            "R2":
                r2,
        })


        # Додаємо прогноз моделі
        validation_table[
            model_name
        ] = y_pred


        # ----------------------------------------------------
        # Збереження моделі
        # ----------------------------------------------------

        model_path = (
            MODELS_DIR /
            MODEL_FILES[model_name]
        )


        joblib.dump(
            pipeline,
            model_path
        )


        # ----------------------------------------------------
        # Виведення результатів
        # ----------------------------------------------------

        print(
            f"\nЧас навчання: "
            f"{training_time:.4f} с"
        )

        print(
            f"Час прогнозування: "
            f"{prediction_time:.4f} с"
        )

        print(
            f"MAE:  {mae:.2f}"
        )

        print(
            f"RMSE: {rmse:.2f}"
        )

        print(
            f"R²:   {r2:.5f}"
        )

        print(
            f"Модель збережено: "
            f"{model_path.name}"
        )


    # ========================================================
    # ЗБЕРЕЖЕННЯ МЕТРИК
    # ========================================================

    results_df = pd.DataFrame(
        results
    )


    results_df.to_csv(
        RESULTS_PATH,
        index=False,
    )


    # ========================================================
    # ЗБЕРЕЖЕННЯ ПРОГНОЗІВ
    # ========================================================

    validation_table.to_csv(
        PREDICTIONS_PATH,
        index=False,
    )


    # ========================================================
    # МЕТАДАНІ
    # ========================================================

    metadata = {

        "project":
            "Used Car Price Prediction",

        "dataset":
            DATASET_PATH.name,

        "dataset_rows":
            int(len(df)),

        "train_rows":
            int(len(X_train)),

        "validation_rows":
            int(len(X_val)),

        "test_rows":
            int(len(X_test)),

        "target":
            TARGET_COLUMN,

        "categorical_columns":
            CATEGORICAL_COLUMNS,

        "numeric_columns":
            NUMERIC_COLUMNS,

        "feature_columns":
            FEATURE_COLUMNS,

        "model_files":
            MODEL_FILES,


        "categories": {

            column: sorted(
                [
                    str(value)
                    for value in
                    df[column]
                    .dropna()
                    .unique()
                    .tolist()
                ]
            )

            for column
            in CATEGORICAL_COLUMNS
        },


        "numeric_ranges": {

            column: {

                "min":
                    float(
                        df[column].min()
                    ),

                "max":
                    float(
                        df[column].max()
                    ),

            }

            for column
            in NUMERIC_COLUMNS
        },


        "price_range": {

            "min":
                float(
                    df[TARGET_COLUMN].min()
                ),

            "max":
                float(
                    df[TARGET_COLUMN].max()
                ),

            "mean":
                float(
                    df[TARGET_COLUMN].mean()
                ),

            "median":
                float(
                    df[TARGET_COLUMN].median()
                ),
        },
    }


    # ========================================================
    # ЗАПИС МЕТАДАНИХ
    # ========================================================

    with open(
        METADATA_PATH,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            metadata,
            file,
            ensure_ascii=False,
            indent=2,
        )


    # ========================================================
    # ПІДСУМКОВА ТАБЛИЦЯ
    # ========================================================

    print("\n" + "=" * 72)

    print(
        "ПОРІВНЯННЯ РЕЗУЛЬТАТІВ МОДЕЛЕЙ"
    )

    print("=" * 72)

    print(
        results_df.to_string(
            index=False
        )
    )


    # ========================================================
    # ЗАВЕРШЕННЯ
    # ========================================================

    print("\n" + "=" * 72)

    print(
        "НАВЧАННЯ МОДЕЛЕЙ ЗАВЕРШЕНО"
    )

    print("=" * 72)

    print(
        f"\nРезультати: "
        f"{RESULTS_PATH.name}"
    )

    print(
        f"Прогнози:   "
        f"{PREDICTIONS_PATH.name}"
    )

    print(
        f"Метадані:   "
        f"{METADATA_PATH.name}"
    )

    print(
        f"Моделі:     "
        f"{MODELS_DIR}"
    )

    print(
        "\nСистема готова до використання "
        "для прогнозування вартості автомобілів."
    )


# ============================================================
# ЗАПУСК
# ============================================================

if __name__ == "__main__":
    main()
