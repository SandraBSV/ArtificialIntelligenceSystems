import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sys
from pathlib import Path

# ============================================================
# НАЛАШТУВАННЯ
# ============================================================

sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Car_Price_Prediction.csv"

# Завантаження даних
df = pd.read_csv(DATA_PATH)

# Стиль графіків
sns.set_theme(
    style="whitegrid",
    context="notebook"
)

plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.titlesize"] = 15
plt.rcParams["axes.labelsize"] = 11


# ============================================================
# 1. ПОЧАТКОВИЙ АНАЛІЗ ДАТАСЕТУ
# ============================================================

print("=" * 70)
print("     АНАЛІЗ ДАТАСЕТУ ВЖИВАНИХ АВТОМОБІЛІВ")
print("=" * 70)

print("\nПерші 5 записів:")
print(df.head())

print("\nРозмір набору даних:")
print(f"Кількість записів: {df.shape[0]}")
print(f"Кількість колонок: {df.shape[1]}")

print("\nНазви колонок:")
print(list(df.columns))


# ============================================================
# 2. ЗАГАЛЬНА ІНФОРМАЦІЯ
# ============================================================

print("\n" + "=" * 70)
print("ЗАГАЛЬНА ІНФОРМАЦІЯ ПРО ДАНІ")
print("=" * 70)

df.info()

print("\nТипи даних:")
print(df.dtypes)


# ============================================================
# 3. ВИЗНАЧЕННЯ ЧИСЛОВИХ ТА КАТЕГОРІАЛЬНИХ ОЗНАК
# ============================================================

numeric_columns = df.select_dtypes(
    include=["int64", "float64"]
).columns.tolist()

categorical_columns = df.select_dtypes(
    include=["object", "category", "bool"]
).columns.tolist()

print("\nЧислові ознаки:")
print(numeric_columns)

print("\nКатегоріальні ознаки:")
print(categorical_columns)


# ============================================================
# 4. ПРОПУЩЕНІ ЗНАЧЕННЯ
# ============================================================

print("\n" + "=" * 70)
print("ПРОПУЩЕНІ ЗНАЧЕННЯ")
print("=" * 70)

missing_values = df.isnull().sum()

print("\nКількість пропущених значень у кожній колонці:")
print(missing_values)

print(
    "\nЗагальна кількість пропущених значень:",
    missing_values.sum()
)


# Графік пропущених значень
missing_nonzero = missing_values[missing_values > 0]

if len(missing_nonzero) > 0:
    plt.figure(figsize=(10, 5))

    missing_nonzero.sort_values().plot(
        kind="barh"
    )

    plt.title(
        "Кількість пропущених значень за ознаками",
        fontweight="bold"
    )
    plt.xlabel("Кількість пропущених значень")
    plt.ylabel("Ознака")

    plt.tight_layout()
    plt.show()
else:
    print("\nПропущених значень у датасеті немає.")


# ============================================================
# 5. СТАТИСТИЧНИЙ АНАЛІЗ ЧИСЛОВИХ ОЗНАК
# ============================================================

print("\n" + "=" * 70)
print("СТАТИСТИЧНІ ХАРАКТЕРИСТИКИ")
print("=" * 70)

if numeric_columns:
    print(df[numeric_columns].describe())


# ============================================================
# 6. ПОШУК ЦІЛЬОВОЇ ЗМІННОЇ
# ============================================================

possible_price_columns = [
    "price",
    "Price",
    "selling_price",
    "sellingPrice",
    "car_price",
    "Car_Price",
    "SalePrice",
    "selling price"
]

target_column = None

for column in possible_price_columns:
    if column in df.columns:
        target_column = column
        break

# Якщо стандартної назви немає,
# шукаємо числову колонку з назвою, що містить price
if target_column is None:
    for column in df.columns:
        if "price" in column.lower():
            if pd.api.types.is_numeric_dtype(df[column]):
                target_column = column
                break


if target_column is None:
    print(
        "\nУвага: автоматично визначити колонку з ціною не вдалося."
    )
    print(
        "Перевір назву цільової змінної у своєму CSV-файлі."
    )

else:

    print("\nЦільова змінна:")
    print(target_column)

    print("\nСтатистичні характеристики вартості автомобілів:")
    print(df[target_column].describe())


    # ========================================================
    # 7. РОЗПОДІЛ ЦІНИ
    # ========================================================

    plt.figure(figsize=(11, 6))

    sns.histplot(
        data=df,
        x=target_column,
        bins=40,
        kde=True
    )

    plt.title(
        "Розподіл вартості вживаних автомобілів",
        fontweight="bold"
    )

    plt.xlabel("Вартість автомобіля")
    plt.ylabel("Кількість автомобілів")

    plt.tight_layout()
    plt.show()


    # ========================================================
    # 8. BOXPLOT ЦІНИ
    # ========================================================

    plt.figure(figsize=(11, 3.5))

    sns.boxplot(
        x=df[target_column]
    )

    plt.title(
        "Аналіз розподілу вартості автомобілів",
        fontweight="bold"
    )

    plt.xlabel("Вартість автомобіля")

    plt.tight_layout()
    plt.show()


    # ========================================================
    # 9. КОРЕЛЯЦІЙНИЙ АНАЛІЗ
    # ========================================================

    if len(numeric_columns) >= 2:

        correlation = df[numeric_columns].corr()

        plt.figure(
            figsize=(11, 8)
        )

        sns.heatmap(
            correlation,
            annot=True,
            fmt=".2f",
            linewidths=0.5,
            square=True
        )

        plt.title(
            "Кореляція між числовими характеристиками",
            fontweight="bold"
        )

        plt.tight_layout()
        plt.show()


    # ========================================================
    # 10. НАЙСИЛЬНІШІ ЗВ'ЯЗКИ З ЦІНОЮ
    # ========================================================

    if target_column in numeric_columns:

        price_correlations = (
            df[numeric_columns]
            .corr()[target_column]
            .sort_values(ascending=False)
        )

        print("\nКореляція ознак із ціною:")
        print(price_correlations)


    # ========================================================
    # 11. АНАЛІЗ ВИКИДІВ
    # ========================================================

    Q1 = df[target_column].quantile(0.25)
    Q3 = df[target_column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[target_column] < lower_bound) |
        (df[target_column] > upper_bound)
    ]

    print("\n" + "=" * 70)
    print("АНАЛІЗ МОЖЛИВИХ ВИКИДІВ")
    print("=" * 70)

    print(f"Q1: {Q1:.2f}")
    print(f"Q3: {Q3:.2f}")
    print(f"IQR: {IQR:.2f}")
    print(f"Нижня межа: {lower_bound:.2f}")
    print(f"Верхня межа: {upper_bound:.2f}")

    print(
        f"Кількість можливих викидів: {len(outliers)}"
    )


    # ========================================================
    # 12. ПЕРЕВІРКА НЕКОРЕКТНИХ ЦІН
    # ========================================================

    print("\nПеревірка некоректних значень:")

    print(
        "Кількість автомобілів з ціною <= 0:",
        (df[target_column] <= 0).sum()
    )


# ============================================================
# 13. ДУБЛІКАТИ
# ============================================================

print("\n" + "=" * 70)
print("ДУБЛІКАТИ")
print("=" * 70)

duplicate_count = df.duplicated().sum()

print(
    f"Кількість повністю однакових записів: "
    f"{duplicate_count}"
)


# ============================================================
# 14. УНІКАЛЬНІ ЗНАЧЕННЯ КАТЕГОРІАЛЬНИХ ОЗНАК
# ============================================================

print("\n" + "=" * 70)
print("КАТЕГОРІАЛЬНІ ОЗНАКИ")
print("=" * 70)

for column in categorical_columns:

    unique_count = df[column].nunique()

    print(
        f"\n{column}: "
        f"{unique_count} унікальних значень"
    )

    # Для колонок із невеликою кількістю значень
    # виводимо самі категорії
    if unique_count <= 15:
        print(df[column].unique())


# ============================================================
# 15. АНАЛІЗ ЧИСЛОВИХ ОЗНАК
# ============================================================

print("\n" + "=" * 70)
print("ПЕРЕВІРКА ЧИСЛОВИХ ОЗНАК")
print("=" * 70)

for column in numeric_columns:

    print(f"\n{column}:")

    print(
        "  Мінімальне значення:",
        df[column].min()
    )

    print(
        "  Максимальне значення:",
        df[column].max()
    )

    print(
        "  Середнє значення:",
        round(df[column].mean(), 2)
    )

    print(
        "  Медіана:",
        round(df[column].median(), 2)
    )


# ============================================================
# 16. ТОП-10 НАЙДОРОЖЧИХ АВТОМОБІЛІВ
# ============================================================

if target_column is not None:

    print("\n" + "=" * 70)
    print("10 НАЙДОРОЖЧИХ АВТОМОБІЛІВ")
    print("=" * 70)

    expensive_cars = (
        df.sort_values(
            by=target_column,
            ascending=False
        )
        .head(10)
    )

    print(expensive_cars)


# ============================================================
# 17. ТОП-10 НАЙДЕШЕВШИХ АВТОМОБІЛІВ
# ============================================================

if target_column is not None:

    print("\n" + "=" * 70)
    print("10 НАЙДЕШЕВШИХ АВТОМОБІЛІВ")
    print("=" * 70)

    cheap_cars = (
        df.sort_values(
            by=target_column,
            ascending=True
        )
        .head(10)
    )

    print(cheap_cars)


# ============================================================
# 18. РОЗПОДІЛ ЧИСЛОВИХ ОЗНАК
# ============================================================

for column in numeric_columns:

    plt.figure(figsize=(10, 5))

    sns.histplot(
        data=df,
        x=column,
        bins=30,
        kde=True
    )

    plt.title(
        f"Розподіл ознаки «{column}»",
        fontweight="bold"
    )

    plt.xlabel(column)
    plt.ylabel("Кількість записів")

    plt.tight_layout()
    plt.show()


# ============================================================
# ЗАВЕРШЕННЯ
# ============================================================

print("\n" + "=" * 70)
print("АНАЛІЗ ДАТАСЕТУ ЗАВЕРШЕНО")
print("=" * 70)
