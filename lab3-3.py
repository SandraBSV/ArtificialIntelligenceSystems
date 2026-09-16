from pathlib import Path
import sys

import joblib
import pandas as pd

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

from sklearn.model_selection import train_test_split


sys.stdout.reconfigure(encoding="utf-8")


# ============================================================
# НАЛАШТУВАННЯ
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR
    / "Car_Price_Prediction.csv"
)

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "random_forest.joblib"
)

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
    "price"
]


# ============================================================
# ОЗНАКИ
# ============================================================

CATEGORICAL_COLUMNS = [
    "brand",
    "model",
    "fuel_type",
    "transmission",
]


NUMERIC_COLUMNS = [
    "year",
    "engine_size",
    "mileage",
]


FEATURE_COLUMNS = (
    CATEGORICAL_COLUMNS
    + NUMERIC_COLUMNS
)


# ============================================================
# ЗАВАНТАЖЕННЯ ДАТАСЕТУ
# ============================================================

# У датасеті немає заголовка,
# тому задаємо назви колонок вручну

df = pd.read_csv(
    DATASET_PATH,
    header=None,
    names=DATASET_COLUMNS
)


# ============================================================
# ПІДГОТОВКА ДАНИХ
# ============================================================

# Перетворюємо числові колонки
# у числовий формат

for column in NUMERIC_COLUMNS + ["price"]:

    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )


# Видаляємо некоректні записи

df = df.dropna(
    subset=FEATURE_COLUMNS + ["price"]
)


# ============================================================
# ПЕРЕВІРКА КОРЕКТНОСТІ ДАНИХ
# ============================================================

# Ціна повинна бути більшою за 0

df = df[
    df["price"] > 0
]


# Рік автомобіля

df = df[
    (df["year"] >= 1900)
    &
    (df["year"] <= 2100)
]


# Об'єм двигуна

df = df[
    df["engine_size"] > 0
]


# Пробіг

df = df[
    df["mileage"] >= 0
]


# Видалення дублікатів

df = df.drop_duplicates()


# ============================================================
# ФОРМУВАННЯ X ТА y
# ============================================================

X = df[
    FEATURE_COLUMNS
]

y = df[
    "price"
]


# ============================================================
# ВІДТВОРЕННЯ ТОГО САМОГО ПОДІЛУ
# ============================================================

# 70% — навчальна вибірка
# 15% — валідаційна вибірка
# 15% — тестова вибірка

X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.30,
    random_state=RANDOM_STATE
)


X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.50,
    random_state=RANDOM_STATE
)


# ============================================================
# ЗАВАНТАЖЕННЯ ГОТОВОЇ МОДЕЛІ
# ============================================================

model = joblib.load(
    MODEL_PATH
)


# ============================================================
# ФІНАЛЬНИЙ ПРОГНОЗ НА TEST
# ============================================================

y_test_pred = model.predict(
    X_test
)


# ============================================================
# МЕТРИКИ
# ============================================================

test_mae = mean_absolute_error(
    y_test,
    y_test_pred
)


test_rmse = (
    mean_squared_error(
        y_test,
        y_test_pred
    ) ** 0.5
)


test_r2 = r2_score(
    y_test,
    y_test_pred
)


# ============================================================
# РЕЗУЛЬТАТ
# ============================================================

print("=" * 60)

print(
    "ФІНАЛЬНЕ ОЦІНЮВАННЯ "
    "RANDOM FOREST НА TEST"
)

print("=" * 60)

print(
    f"Кількість автомобілів у датасеті: "
    f"{len(df)}"
)

print(
    f"Кількість тестових записів: "
    f"{len(X_test)}"
)

print()

print(
    f"MAE:  {test_mae:.2f}"
)

print(
    f"RMSE: {test_rmse:.2f}"
)

print(
    f"R²:   {test_r2:.4f}"
)