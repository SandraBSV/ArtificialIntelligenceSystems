import tkinter as tk
from tkinter import ttk

try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    from matplotlib.figure import Figure
    HAS_MATPLOTLIB = True
except ImportError:
    HAS_MATPLOTLIB = False


# ============================================================
# 1. ПОЧАТКОВІ ФАКТИ
# ============================================================

INPUT_FACTS = [
    {
        "name": "family_size",
        "label": "Кількість членів сім'ї",
        "type": "int",
        "min": 1,
        "max": 12,
        "default": 3
    },
    {
        "name": "children_count",
        "label": "Кількість дітей",
        "type": "int",
        "min": 0,
        "max": 10,
        "default": 1
    },
    {
        "name": "budget_level",
        "label": "Рівень бюджету",
        "type": "enum",
        "values": ["low", "medium", "high"],
        "default": "medium",
        "titles": {
            "low": "низький",
            "medium": "середній",
            "high": "високий"
        }
    },
    {
        "name": "shopping_frequency",
        "label": "Частота закупівель",
        "type": "enum",
        "values": ["rare", "weekly", "frequent"],
        "default": "weekly",
        "titles": {
            "rare": "раз на місяць",
            "weekly": "раз на тиждень",
            "frequent": "кілька разів на тиждень"
        }
    },
    {
        "name": "healthy_food_priority",
        "label": "Пріоритет здорового харчування",
        "type": "bool",
        "default": True
    },
    {
        "name": "vegetarian",
        "label": "Сім'я дотримується вегетаріанського харчування",
        "type": "bool",
        "default": False
    },
    {
        "name": "has_pet",
        "label": "Є домашня тварина",
        "type": "bool",
        "default": False
    },
    {
        "name": "bulk_buying",
        "label": "Готовність купувати великими упаковками",
        "type": "bool",
        "default": False
    },
    {
        "name": "has_freezer",
        "label": "Є велика морозильна камера",
        "type": "bool",
        "default": True
    },
    {
        "name": "special_diet",
        "label": "Є спеціальні дієтичні потреби",
        "type": "bool",
        "default": False
    }
]


# ============================================================
# 2. ПРОМІЖНІ ФАКТИ
# ============================================================

INTERMEDIATE_FACTS = [
    {
        "name": "large_family",
        "label": "Велика сім'я"
    },
    {
        "name": "children_priority",
        "label": "Потрібні продукти для дітей"
    },
    {
        "name": "economy_priority",
        "label": "Пріоритет економії"
    },
    {
        "name": "healthy_priority",
        "label": "Пріоритет здорового харчування"
    },
    {
        "name": "bulk_strategy",
        "label": "Доцільна закупівля великими упаковками"
    },
    {
        "name": "storage_ready",
        "label": "Є умови для довготривалого зберігання"
    },
    {
        "name": "special_products_needed",
        "label": "Потрібні спеціальні продукти"
    },
    {
        "name": "pet_products_needed",
        "label": "Потрібні товари для тварини"
    },
    {
        "name": "vegetarian_products",
        "label": "Потрібен вегетаріанський набір"
    }
]


GOAL_FACT = "shopping_recommendation"


# ============================================================
# 3. КІНЦЕВІ РІШЕННЯ
# ============================================================

DECISIONS = {

    "FAMILY_BULK_SHOPPING": {
        "label": "Велика планова закупівля",
        "text": (
            "Для сім'ї доцільно сформувати великий список продуктів "
            "тривалого зберігання та купувати частину товарів великими упаковками."
        )
    },

    "ECONOMY_SHOPPING": {
        "label": "Економна закупівля",
        "text": (
            "Основний акцент варто зробити на акційних товарах, "
            "продуктах власних торгових марок та товарах із вигідною ціною."
        )
    },

    "HEALTHY_SHOPPING": {
        "label": "Закупівля здорового харчування",
        "text": (
            "До списку варто включити більше овочів, фруктів, "
            "цільнозернових продуктів та інших корисних продуктів."
        )
    },

    "CHILDREN_SHOPPING": {
        "label": "Закупівля з пріоритетом дитячих продуктів",
        "text": (
            "Основну увагу слід приділити продуктам для дітей: "
            "молочним продуктам, кашам, фруктам та корисним перекусам."
        )
    },

    "VEGETARIAN_SHOPPING": {
        "label": "Вегетаріанський продуктовий кошик",
        "text": (
            "Сформовано кошик без м'ясних продуктів із додаванням "
            "овочів, фруктів, круп, бобових та рослинних джерел білка."
        )
    },

    "SPECIAL_DIET_SHOPPING": {
        "label": "Закупівля спеціальних дієтичних продуктів",
        "text": (
            "До списку закупівлі потрібно включити продукти, "
            "що відповідають спеціальним дієтичним потребам сім'ї."
        )
    },

    "PET_SHOPPING": {
        "label": "Комплексна закупівля продуктів і товарів для тварини",
        "text": (
            "До основного списку продуктів потрібно додати корм "
            "та необхідні товари для домашньої тварини."
        )
    },

    "WEEKLY_SHOPPING": {
        "label": "Стандартна щотижнева закупівля",
        "text": (
            "Рекомендується сформувати збалансований продуктовий кошик "
            "на один тиждень без надмірного запасу."
        )
    },

    "FRESH_FOOD_SHOPPING": {
        "label": "Часті закупівлі свіжих продуктів",
        "text": (
            "Доцільно купувати свіжі овочі, фрукти, молочні та інші "
            "швидкопсувні продукти невеликими партіями."
        )
    }
}


# ============================================================
# 4. ПРАВИЛА БАЗИ ЗНАНЬ
# ============================================================

RULES = [

    {
        "id": "R01",
        "priority": 95,
        "text": "Сім'я з 5 або більше людей вважається великою",
        "if": {
            "all": [
                ("family_size", ">=", 5)
            ]
        },
        "then": ("large_family", True)
    },

    {
        "id": "R02",
        "priority": 94,
        "text": "Наявність дітей створює потребу в дитячих продуктах",
        "if": {
            "all": [
                ("children_count", ">=", 1)
            ]
        },
        "then": ("children_priority", True)
    },

    {
        "id": "R03",
        "priority": 93,
        "text": "Низький бюджет визначає пріоритет економії",
        "if": {
            "all": [
                ("budget_level", "==", "low")
            ]
        },
        "then": ("economy_priority", True)
    },

    {
        "id": "R04",
        "priority": 92,
        "text": "Високий пріоритет здорового харчування формує відповідний напрям закупівлі",
        "if": {
            "all": [
                ("healthy_food_priority", "==", True)
            ]
        },
        "then": ("healthy_priority", True)
    },

    {
        "id": "R05",
        "priority": 90,
        "text": "Велика сім'я та готовність купувати великими упаковками формують оптову стратегію",
        "if": {
            "all": [
                ("large_family", "==", True),
                ("bulk_buying", "==", True)
            ]
        },
        "then": ("bulk_strategy", True)
    },

    {
        "id": "R06",
        "priority": 89,
        "text": "Морозильна камера дозволяє зберігати запас продуктів",
        "if": {
            "all": [
                ("has_freezer", "==", True)
            ]
        },
        "then": ("storage_ready", True)
    },

    {
        "id": "R07",
        "priority": 88,
        "text": "Спеціальна дієта вимагає спеціального набору продуктів",
        "if": {
            "all": [
                ("special_diet", "==", True)
            ]
        },
        "then": ("special_products_needed", True)
    },

    {
        "id": "R08",
        "priority": 87,
        "text": "Наявність домашньої тварини створює потребу в товарах для неї",
        "if": {
            "all": [
                ("has_pet", "==", True)
            ]
        },
        "then": ("pet_products_needed", True)
    },

    {
        "id": "R09",
        "priority": 86,
        "text": "Вегетаріанське харчування формує окремий продуктовий набір",
        "if": {
            "all": [
                ("vegetarian", "==", True)
            ]
        },
        "then": ("vegetarian_products", True)
    },

    {
        "id": "R10",
        "priority": 80,
        "text": "Велика сім'я, великі упаковки та можливість зберігання формують велику закупівлю",
        "if": {
            "all": [
                ("large_family", "==", True),
                ("bulk_strategy", "==", True),
                ("storage_ready", "==", True)
            ]
        },
        "then": (GOAL_FACT, "FAMILY_BULK_SHOPPING")
    },

    {
        "id": "R11",
        "priority": 78,
        "text": "Низький бюджет формує економну закупівлю",
        "if": {
            "all": [
                ("economy_priority", "==", True)
            ]
        },
        "then": (GOAL_FACT, "ECONOMY_SHOPPING")
    },

    {
        "id": "R12",
        "priority": 76,
        "text": "Здорове харчування є пріоритетом сім'ї",
        "if": {
            "all": [
                ("healthy_priority", "==", True),
                ("budget_level", "in", ["medium", "high"])
            ]
        },
        "then": (GOAL_FACT, "HEALTHY_SHOPPING")
    },

    {
        "id": "R13",
        "priority": 74,
        "text": "Наявність дітей формує дитячий продуктовий кошик",
        "if": {
            "all": [
                ("children_priority", "==", True)
            ]
        },
        "then": (GOAL_FACT, "CHILDREN_SHOPPING")
    },

    {
        "id": "R14",
        "priority": 72,
        "text": "Вегетаріанське харчування визначає вегетаріанський кошик",
        "if": {
            "all": [
                ("vegetarian_products", "==", True)
            ]
        },
        "then": (GOAL_FACT, "VEGETARIAN_SHOPPING")
    },

    {
        "id": "R15",
        "priority": 70,
        "text": "Спеціальні дієтичні потреби визначають спеціальний кошик",
        "if": {
            "all": [
                ("special_products_needed", "==", True)
            ]
        },
        "then": (GOAL_FACT, "SPECIAL_DIET_SHOPPING")
    },

    {
        "id": "R16",
        "priority": 68,
        "text": "Домашня тварина додає товари для тварини до закупівлі",
        "if": {
            "all": [
                ("pet_products_needed", "==", True)
            ]
        },
        "then": (GOAL_FACT, "PET_SHOPPING")
    },

    {
        "id": "R17",
        "priority": 50,
        "text": "Щотижневі закупівлі формують стандартний продуктовий кошик",
        "if": {
            "all": [
                ("shopping_frequency", "==", "weekly")
            ]
        },
        "then": (GOAL_FACT, "WEEKLY_SHOPPING")
    },

    {
        "id": "R18",
        "priority": 40,
        "text": "Часті закупівлі орієнтовані на свіжі продукти",
        "if": {
            "all": [
                ("shopping_frequency", "==", "frequent")
            ]
        },
        "then": (GOAL_FACT, "FRESH_FOOD_SHOPPING")
    }
]


# ============================================================
# 5. ДОДАТКОВІ ПРАВИЛА
# ============================================================

EXTRA_RULES = [

    {
        "id": "R19",
        "priority": 85,
        "text": "Велика сім'я з дітьми та здоровим харчуванням потребує комплексної закупівлі",
        "if": {
            "all": [
                ("large_family", "==", True),
                ("children_priority", "==", True),
                ("healthy_priority", "==", True)
            ]
        },
        "then": (GOAL_FACT, "HEALTHY_SHOPPING")
    },

    {
        "id": "R20",
        "priority": 83,
        "text": "Низький бюджет і велика сім'я посилюють необхідність економної закупівлі",
        "if": {
            "all": [
                ("large_family", "==", True),
                ("economy_priority", "==", True)
            ]
        },
        "then": (GOAL_FACT, "ECONOMY_SHOPPING")
    }
]


# ============================================================
# 6. ТЕСТОВІ СЦЕНАРІЇ
# ============================================================

TEST_SCENARIOS = [

    {
        "id": "T1",
        "kind": "типовий",
        "name": "Велика сім'я з можливістю зберігання",
        "facts": {
            "family_size": 6,
            "children_count": 2,
            "budget_level": "medium",
            "shopping_frequency": "weekly",
            "healthy_food_priority": False,
            "vegetarian": False,
            "has_pet": False,
            "bulk_buying": True,
            "has_freezer": True,
            "special_diet": False
        },
        "expect": "FAMILY_BULK_SHOPPING"
    },

    {
        "id": "T2",
        "kind": "економія",
        "name": "Сім'я з обмеженим бюджетом",
        "facts": {
            "family_size": 4,
            "children_count": 1,
            "budget_level": "low",
            "shopping_frequency": "weekly",
            "healthy_food_priority": False,
            "vegetarian": False,
            "has_pet": False,
            "bulk_buying": False,
            "has_freezer": False,
            "special_diet": False
        },
        "expect": "ECONOMY_SHOPPING"
    },

    {
        "id": "T3",
        "kind": "здорове харчування",
        "name": "Сім'я з пріоритетом здорового харчування",
        "facts": {
            "family_size": 3,
            "children_count": 0,
            "budget_level": "high",
            "shopping_frequency": "weekly",
            "healthy_food_priority": True,
            "vegetarian": False,
            "has_pet": False,
            "bulk_buying": False,
            "has_freezer": True,
            "special_diet": False
        },
        "expect": "HEALTHY_SHOPPING"
    },

    {
        "id": "T4",
        "kind": "вегетаріанський профіль",
        "name": "Вегетаріанська сім'я",
        "facts": {
            "family_size": 3,
            "children_count": 0,
            "budget_level": "medium",
            "shopping_frequency": "weekly",
            "healthy_food_priority": True,
            "vegetarian": True,
            "has_pet": False,
            "bulk_buying": False,
            "has_freezer": False,
            "special_diet": False
        },
        "expect": "VEGETARIAN_SHOPPING"
    },

    {
        "id": "T5",
        "kind": "спеціальні потреби",
        "name": "Сім'я зі спеціальною дієтою",
        "facts": {
            "family_size": 4,
            "children_count": 1,
            "budget_level": "high",
            "shopping_frequency": "weekly",
            "healthy_food_priority": True,
            "vegetarian": False,
            "has_pet": False,
            "bulk_buying": False,
            "has_freezer": True,
            "special_diet": True
        },
        "expect": "SPECIAL_DIET_SHOPPING"
    },

    {
        "id": "T6",
        "kind": "домашня тварина",
        "name": "Сім'я з домашньою твариною",
        "facts": {
            "family_size": 3,
            "children_count": 1,
            "budget_level": "medium",
            "shopping_frequency": "weekly",
            "healthy_food_priority": False,
            "vegetarian": False,
            "has_pet": True,
            "bulk_buying": False,
            "has_freezer": False,
            "special_diet": False
        },
        "expect": "PET_SHOPPING"
    },

    {
        "id": "T7",
        "kind": "діти",
        "name": "Сім'я з кількома дітьми",
        "facts": {
            "family_size": 5,
            "children_count": 3,
            "budget_level": "medium",
            "shopping_frequency": "weekly",
            "healthy_food_priority": False,
            "vegetarian": False,
            "has_pet": False,
            "bulk_buying": False,
            "has_freezer": False,
            "special_diet": False
        },
        "expect": "CHILDREN_SHOPPING"
    },

    {
        "id": "T8",
        "kind": "часті закупівлі",
        "name": "Сім'я, яка часто купує свіжі продукти",
        "facts": {
            "family_size": 2,
            "children_count": 0,
            "budget_level": "medium",
            "shopping_frequency": "frequent",
            "healthy_food_priority": False,
            "vegetarian": False,
            "has_pet": False,
            "bulk_buying": False,
            "has_freezer": False,
            "special_diet": False
        },
        "expect": "FRESH_FOOD_SHOPPING"
    },

    {
        "id": "T9",
        "kind": "неповний набір фактів",
        "name": "Відомий лише розмір сім'ї та бюджет",
        "facts": {
            "family_size": 6,
            "budget_level": "low"
        },
        "expect": "ECONOMY_SHOPPING"
    },

    {
        "id": "T10",
        "kind": "модифікація БЗ",
        "name": "Велика сім'я з дітьми та здоровим харчуванням",
        "facts": {
            "family_size": 6,
            "children_count": 2,
            "budget_level": "high",
            "shopping_frequency": "weekly",
            "healthy_food_priority": True,
            "vegetarian": False,
            "has_pet": False,
            "bulk_buying": False,
            "has_freezer": True,
            "special_diet": False
        },
        "expect": "CHILDREN_SHOPPING",
        "expect_extended": "HEALTHY_SHOPPING"
    }
]


# ============================================================
# 7. ДОПОМІЖНІ ФУНКЦІЇ
# ============================================================

def all_rules(extended=False):
    return RULES + EXTRA_RULES if extended else list(RULES)


def fact_spec(name):
    for spec in INPUT_FACTS:
        if spec["name"] == name:
            return spec

    for spec in INTERMEDIATE_FACTS:
        if spec["name"] == name:
            return spec

    return {
        "name": name,
        "label": name,
        "type": "any"
    }


def show_value(name, value):

    if isinstance(value, bool):
        return "так" if value else "ні"

    if name == GOAL_FACT and value in DECISIONS:
        return DECISIONS[value]["label"]

    titles = fact_spec(name).get("titles", {})

    return titles.get(value, str(value))


def check(condition, facts):

    if isinstance(condition, dict):

        if "all" in condition:
            return all(
                check(item, facts)
                for item in condition["all"]
            )

        return any(
            check(item, facts)
            for item in condition["any"]
        )

    if condition[0] == "NOT":
        return not check(condition[1], facts)

    name, operation, expected = condition

    if name not in facts:
        return False

    value = facts[name]

    if operation == "==":
        return value == expected

    if operation == "!=":
        return value != expected

    if operation == "in":
        return value in expected

    if operation == ">=":
        return isinstance(value, int) and value >= expected

    if operation == "<=":
        return isinstance(value, int) and value <= expected

    raise ValueError(
        "Невідома операція: " + str(operation)
    )


def premises(condition, facts):

    if isinstance(condition, dict):

        items = condition.get("all") or condition["any"]

        found = []

        for item in items:

            if "all" in condition or check(item, facts):
                found += premises(item, facts)

        return found

    if condition[0] == "NOT":

        return [
            (
                condition[1][0],
                facts.get(condition[1][0], "невідомо")
            )
        ]

    return [
        (
            condition[0],
            facts.get(condition[0], "невідомо")
        )
    ]


def condition_vars(condition):

    if isinstance(condition, dict):

        items = condition.get("all") or condition["any"]

        names = []

        for item in items:
            names += condition_vars(item)

        return names

    if condition[0] == "NOT":
        return condition_vars(condition[1])

    return [condition[0]]


def condition_text(condition):

    if isinstance(condition, dict):

        if "all" in condition:
            return " AND ".join(
                condition_text(c)
                for c in condition["all"]
            )

        return " OR ".join(
            condition_text(c)
            for c in condition["any"]
        )

    if condition[0] == "NOT":
        return "NOT " + condition_text(condition[1])

    name, operation, expected = condition

    if isinstance(expected, list):
        expected = "[" + ", ".join(
            str(v) for v in expected
        ) + "]"

    return "%s %s %s" % (
        name,
        operation,
        expected
    )


def rule_text(rule):

    return "IF %s THEN %s = %s" % (
        condition_text(rule["if"]),
        rule["then"][0],
        rule["then"][1]
    )


# ============================================================
# 8. РЕЗУЛЬТАТ ВИВЕДЕННЯ
# ============================================================

class Result:

    def __init__(self, initial):

        self.facts = dict(initial)

        self.source = {
            name: "вхідний факт"
            for name in initial
        }

        self.steps = []
        self.rejected = []
        self.cycles = 0

    @property
    def decision(self):
        return self.facts.get(GOAL_FACT)

    def fired_ids(self):
        return [
            step["rule"]["id"]
            for step in self.steps
        ]


# ============================================================
# 9. FORWARD CHAINING
# ============================================================

def infer(rules, initial_facts):

    result = Result(initial_facts)

    used = set()

    while True:

        result.cycles += 1

        conflict_set = [
            rule
            for rule in rules
            if (
                rule["id"] not in used
                and check(rule["if"], result.facts)
            )
        ]

        if not conflict_set:
            break

        rule = max(
            conflict_set,
            key=lambda item: item["priority"]
        )

        conflict_set.sort(
            key=lambda item: -item["priority"]
        )

        used.add(rule["id"])

        name, value = rule["then"]

        if name in result.facts:

            result.rejected.append(
                {
                    "rule": rule,
                    "reason": (
                        "факт %s уже виведено правилом %s "
                        "зі значенням %s"
                        % (
                            name,
                            result.source[name],
                            result.facts[name]
                        )
                    )
                }
            )

            continue

        support = premises(
            rule["if"],
            result.facts
        )

        result.facts[name] = value

        result.source[name] = rule["id"]

        result.steps.append(
            {
                "rule": rule,
                "produced": (name, value),
                "premises": support,
                "conflict": [
                    r["id"]
                    for r in conflict_set
                ]
            }
        )

    return result


# ============================================================
# 10. ТЕКСТОВЕ ПОЯСНЕННЯ
# ============================================================

def explanation_text(result):

    lines = [
        "ПОЧАТКОВІ ФАКТИ:",
        ""
    ]

    for name, value in result.facts.items():

        if result.source[name] == "вхідний факт":

            lines.append(
                "   %s = %s"
                % (
                    fact_spec(name)["label"],
                    show_value(name, value)
                )
            )

    lines += [
        "",
        "АКТИВОВАНІ ПРАВИЛА:"
    ]

    if not result.steps:

        lines.append(
            "   жодне правило не спрацювало"
        )

    for number, step in enumerate(
        result.steps,
        1
    ):

        rule = step["rule"]

        conflict = ""

        if len(step["conflict"]) > 1:

            conflict = (
                "   конфліктна множина: "
                + ", ".join(step["conflict"])
            )

        lines.append("")

        lines.append(
            "   Крок %d. %s (пріоритет %d)%s"
            % (
                number,
                rule["id"],
                rule["priority"],
                conflict
            )
        )

        lines.append(
            "      %s"
            % rule["text"]
        )

        lines.append(
            "      %s"
            % rule_text(rule)
        )

        lines.append(
            "      обґрунтування: "
            + ", ".join(
                "%s = %s"
                % (
                    fact_spec(name)["label"],
                    show_value(name, value)
                )
                for name, value in step["premises"]
            )
        )

        lines.append(
            "      отримано факт: %s = %s"
            % (
                fact_spec(
                    step["produced"][0]
                )["label"],
                show_value(
                    *step["produced"]
                )
            )
        )

    if result.rejected:

        lines += [
            "",
            "ВІДХИЛЕНІ ПРАВИЛА:",
        ]

        for item in result.rejected:

            lines.append(
                "   %s (пріоритет %d) — %s"
                % (
                    item["rule"]["id"],
                    item["rule"]["priority"],
                    item["reason"]
                )
            )

    lines += [
        "",
        "РЕЗУЛЬТАТ: "
        + (
            "%s — %s"
            % (
                result.decision,
                DECISIONS[
                    result.decision
                ]["label"]
            )
            if result.decision
            else "рішення не сформовано"
        )
    ]

    return "\n".join(lines)


def chain_text(
    result,
    name=None,
    level=0
):

    name = name or GOAL_FACT

    if name not in result.facts:

        return "Цільовий факт не виведено."

    indent = "    " * level

    origin = result.source[name]

    lines = [
        "%s%s = %s"
        % (
            indent,
            fact_spec(name)["label"],
            show_value(
                name,
                result.facts[name]
            )
        )
    ]

    if origin == "вхідний факт":

        lines[0] += " [початковий факт]"

        return "\n".join(lines)

    step = next(
        s
        for s in result.steps
        if s["produced"][0] == name
    )

    lines[0] += (
        " [правило %s]"
        % origin
    )

    for premise_name, _ in step["premises"]:

        lines.append(
            chain_text(
                result,
                premise_name,
                level + 1
            )
        )

    return "\n".join(lines)


# ============================================================
# 11. ДИЗАЙН
# ============================================================

BG = "#F4F7F5"
PANEL = "#FFFFFF"
CARD = "#FFFFFF"
BORDER = "#D7E2DA"

TEXT = "#17231C"
MUTED = "#718078"

GREEN = "#16805C"
GREEN_DARK = "#0D6044"
GREEN_LIGHT = "#DDF4EA"

ORANGE = "#F59E0B"
ORANGE_LIGHT = "#FEF3C7"

RED = "#DC4C64"
RED_LIGHT = "#FDE8EC"

BLUE = "#3B82F6"
BLUE_LIGHT = "#E8F0FE"

NOT_SET = "— не задано —"


# ============================================================
# 12. ОСНОВНИЙ ДОДАТОК
# ============================================================

class Application:

    def __init__(self, root):

        self.root = root

        self.result = None
        self.fields = {}

        root.title(
            "SmartMarket — система планування закупівель"
        )

        root.geometry(
            "1450x900"
        )

        root.minsize(
            1150,
            720
        )

        root.configure(
            bg=BG
        )

        self.extended = tk.BooleanVar(
            value=False
        )

        self.scenario = tk.StringVar()

        self.status = tk.StringVar(
            value=(
                "Заповніть параметри сім'ї "
                "та натисніть «Сформувати рекомендацію»."
            )
        )

        self._styles()
        self._header()
        self._body()
        self._defaults()
        self._show_rules()
        self._draw_graph()


    # ========================================================
    # СТИЛІ
    # ========================================================

    def _styles(self):

        style = ttk.Style()

        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TFrame",
            background=PANEL
        )

        style.configure(
            "Bg.TFrame",
            background=BG
        )

        style.configure(
            "Card.TFrame",
            background=CARD
        )

        style.configure(
            "Title.TLabel",
            background=PANEL,
            foreground=TEXT,
            font=("Segoe UI", 16, "bold")
        )

        style.configure(
            "Sub.TLabel",
            background=PANEL,
            foreground=MUTED,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Field.TLabel",
            background=PANEL,
            foreground=TEXT,
            font=("Segoe UI", 9, "bold")
        )

        style.configure(
            "Decision.TLabel",
            background=CARD,
            foreground=GREEN,
            font=("Segoe UI", 11, "bold"),
            wraplength=320,
            justify="left"
        )

        style.configure(
            "Go.TButton",
            background=GREEN,
            foreground="white",
            borderwidth=0,
            padding=(12, 10),
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Go.TButton",
            background=[
                ("active", GREEN_DARK)
            ]
        )

        style.configure(
            "TButton",
            background="#E8EFEA",
            foreground=TEXT,
            borderwidth=0,
            padding=(10, 8),
            font=("Segoe UI", 9)
        )

        style.map(
            "TButton",
            background=[
                ("active", "#D8E5DD")
            ]
        )

        style.configure(
            "TCheckbutton",
            background=PANEL,
            foreground=TEXT,
            font=("Segoe UI", 9)
        )

        style.map(
            "TCheckbutton",
            background=[
                ("active", PANEL)
            ]
        )

        style.configure(
            "TCombobox",
            fieldbackground=CARD,
            background=CARD,
            foreground=TEXT,
            arrowcolor=GREEN,
            bordercolor=BORDER,
            padding=5
        )

        style.map(
            "TCombobox",
            fieldbackground=[
                ("readonly", CARD)
            ],
            foreground=[
                ("readonly", TEXT)
            ]
        )

        style.configure(
            "TSpinbox",
            fieldbackground=CARD,
            background=CARD,
            foreground=TEXT,
            arrowcolor=GREEN,
            padding=4
        )

        style.configure(
            "TNotebook",
            background=PANEL,
            borderwidth=0
        )

        style.configure(
            "TNotebook.Tab",
            background="#EDF2EF",
            foreground=MUTED,
            padding=(15, 8),
            borderwidth=0,
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "TNotebook.Tab",
            background=[
                ("selected", GREEN_LIGHT)
            ],
            foreground=[
                ("selected", GREEN_DARK)
            ]
        )

        style.configure(
            "Treeview",
            background=CARD,
            fieldbackground=CARD,
            foreground=TEXT,
            borderwidth=0,
            rowheight=26,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background="#EDF2EF",
            foreground=TEXT,
            relief="flat",
            font=("Segoe UI", 9, "bold")
        )

        style.map(
            "Treeview",
            background=[
                ("selected", GREEN)
            ],
            foreground=[
                ("selected", "white")
            ]
        )

        self.root.option_add(
            "*TCombobox*Listbox.background",
            CARD
        )

        self.root.option_add(
            "*TCombobox*Listbox.foreground",
            TEXT
        )

        self.root.option_add(
            "*TCombobox*Listbox.selectBackground",
            GREEN
        )


    # ========================================================
    # HEADER
    # ========================================================

    def _header(self):

        head = ttk.Frame(
            self.root,
            padding=(22, 16)
        )

        head.pack(
            fill="x"
        )

        title_frame = ttk.Frame(
            head
        )

        title_frame.pack(
            fill="x"
        )

        ttk.Label(
            title_frame,
            text="🛒 SmartMarket",
            style="Title.TLabel"
        ).pack(
            side="left"
        )

        ttk.Label(
            title_frame,
            text="ПЛАНУВАННЯ ЗАКУПІВЕЛЬ",
            foreground=GREEN,
            background=PANEL,
            font=("Segoe UI", 10, "bold")
        ).pack(
            side="left",
            padx=(15, 0)
        )

        ttk.Label(
            head,
            text=(
                "Система підтримки прийняття рішень для формування "
                "продуктового кошика відповідно до потреб сім'ї."
            ),
            style="Sub.TLabel"
        ).pack(
            anchor="w",
            pady=(5, 0)
        )


    # ========================================================
    # BODY
    # ========================================================

    def _body(self):

        body = ttk.Frame(
            self.root,
            style="Bg.TFrame",
            padding=(15, 5, 15, 5)
        )

        body.pack(
            fill="both",
            expand=True
        )

        # ====================================================
        # ЛІВА ПАНЕЛЬ ЗІ СКРОЛОМ
        # ====================================================

        left_container = tk.Frame(
            body,
            bg=BG,
            width=360
        )

        left_container.pack(
            side="left",
            fill="y"
        )

        left_container.pack_propagate(False)

        left_canvas = tk.Canvas(
            left_container,
            bg=BG,
            highlightthickness=0,
            bd=0
        )

        left_scrollbar = ttk.Scrollbar(
            left_container,
            orient="vertical",
            command=left_canvas.yview
        )

        left_canvas.configure(
            yscrollcommand=left_scrollbar.set
        )

        left_scrollbar.pack(
            side="right",
            fill="y"
        )

        left_canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        left = ttk.Frame(
            left_canvas,
            padding=(10, 10)
        )

        window_id = left_canvas.create_window(
            (0, 0),
            window=left,
            anchor="nw"
        )

        def update_scroll(event=None):
            left_canvas.configure(
                scrollregion=left_canvas.bbox("all")
            )

        left.bind(
            "<Configure>",
            update_scroll
        )

        def resize_left(event):
            left_canvas.itemconfigure(
                window_id,
                width=event.width
            )

        left_canvas.bind(
            "<Configure>",
            resize_left
        )

        # Колесо миші
        def mouse_wheel(event):
            left_canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        left_canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel
        )

        self._input_panel(left)

        # ====================================================
        # ПРАВА ПАНЕЛЬ
        # ====================================================

        right = ttk.Frame(
            body
        )

        right.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(15, 0)
        )

        self._tabs(right)

        # ====================================================
        # STATUS BAR
        # ====================================================

        bar = ttk.Frame(
            self.root,
            padding=(20, 7)
        )

        bar.pack(
            fill="x",
            side="bottom"
        )

        ttk.Label(
            bar,
            textvariable=self.status,
            style="Sub.TLabel"
        ).pack(
            anchor="w"
        )


    # ========================================================
    # INPUT PANEL
    # ========================================================

    def _input_panel(self, parent):

        ttk.Label(
            parent,
            text="ПАРАМЕТРИ СІМ'Ї",
            style="Title.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            parent,
            text=(
                "Вкажіть відомі характеристики сім'ї. "
                "Незаповнені поля залишаються невідомими."
            ),
            style="Sub.TLabel",
            wraplength=330
        ).pack(
            anchor="w",
            pady=(3, 12)
        )

        for spec in INPUT_FACTS:

            row = ttk.Frame(
                parent
            )

            row.pack(
                fill="x",
                pady=3
            )

            ttk.Label(
                row,
                text=spec["label"],
                style="Field.TLabel",
                wraplength=330
            ).pack(
                anchor="w"
            )

            variable = tk.StringVar()

            if spec["type"] == "bool":

                widget = ttk.Combobox(
                    row,
                    textvariable=variable,
                    state="readonly",
                    width=32,
                    values=[
                        NOT_SET,
                        "так",
                        "ні"
                    ]
                )

            elif spec["type"] == "enum":

                titles = spec.get(
                    "titles",
                    {}
                )

                values = [
                    NOT_SET
                ] + [
                    (
                        "%s — %s"
                        % (
                            v,
                            titles[v]
                        )
                        if v in titles
                        else v
                    )
                    for v in spec["values"]
                ]

                widget = ttk.Combobox(
                    row,
                    textvariable=variable,
                    state="readonly",
                    width=32,
                    values=values
                )

            else:

                widget = ttk.Spinbox(
                    row,
                    textvariable=variable,
                    width=32,
                    from_=spec["min"],
                    to=spec["max"]
                )

            widget.pack(
                fill="x",
                pady=(2, 0)
            )

            self.fields[
                spec["name"]
            ] = variable

        ttk.Separator(
            parent,
            orient="horizontal"
        ).pack(
            fill="x",
            pady=12
        )

        ttk.Label(
            parent,
            text="ТЕСТОВИЙ СЦЕНАРІЙ",
            style="Field.TLabel"
        ).pack(
            anchor="w"
        )

        box = ttk.Combobox(
            parent,
            textvariable=self.scenario,
            state="readonly",
            width=32,
            values=[
                "%s — %s"
                % (
                    s["id"],
                    s["name"]
                )
                for s in TEST_SCENARIOS
            ]
        )

        box.pack(
            fill="x",
            pady=(3, 8)
        )

        box.bind(
            "<<ComboboxSelected>>",
            lambda event: self._load_scenario()
        )

        ttk.Checkbutton(
            parent,
            text="Розширена база знань (+2 правила)",
            variable=self.extended,
            command=self._switch_kb
        ).pack(
            anchor="w",
            pady=(0, 8)
        )

        ttk.Button(
            parent,
            text="🛒  Сформувати рекомендацію",
            style="Go.TButton",
            command=self.run
        ).pack(
            fill="x"
        )

        ttk.Button(
            parent,
            text="↺  Значення за замовчуванням",
            command=self._defaults
        ).pack(
            fill="x",
            pady=5
        )

        card = tk.Frame(
            parent,
            bg=CARD,
            highlightbackground=GREEN,
            highlightthickness=1
        )

        card.pack(
            fill="x",
            pady=(10, 0)
        )

        tk.Label(
            card,
            text="РЕКОМЕНДОВАНИЙ ТИП ЗАКУПІВЛІ",
            bg=CARD,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            padx=12,
            pady=(10, 3)
        )

        self.decision_label = ttk.Label(
            card,
            text="Рекомендація ще не сформована",
            style="Decision.TLabel"
        )

        self.decision_label.pack(
            anchor="w",
            padx=12,
            pady=(0, 12)
        )


    # ========================================================
    # TABS
    # ========================================================

    def _tabs(self, parent):

        self.notebook = ttk.Notebook(
            parent
        )

        self.notebook.pack(
            fill="both",
            expand=True
        )

        self.chain_text = self._text_tab(
            "Хід виведення"
        )

        self._graph_tab()

        self._rules_tab()


    def _text_tab(self, title):

        frame = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            frame,
            text=title
        )

        text = tk.Text(
            frame,
            wrap="none",
            font=("Consolas", 9),
            bg="#FAFCFB",
            fg=TEXT,
            relief="flat",
            padx=12,
            pady=10,
            borderwidth=0
        )

        bar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=text.yview
        )

        text.configure(
            yscrollcommand=bar.set,
            state="disabled"
        )

        text.pack(
            side="left",
            fill="both",
            expand=True
        )

        bar.pack(
            side="right",
            fill="y"
        )

        return text


    def _graph_tab(self):

        frame = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            frame,
            text="Граф бази знань"
        )

        if not HAS_MATPLOTLIB:

            tk.Label(
                frame,
                text=(
                    "Для відображення графа встановіть matplotlib:\n\n"
                    "pip install matplotlib"
                ),
                bg=PANEL,
                fg=MUTED,
                font=("Segoe UI", 11)
            ).pack(
                expand=True
            )

            self.figure = None

            return

        self.figure = Figure(
            figsize=(10, 6.5),
            dpi=100,
            facecolor=BG
        )

        self.axes = self.figure.add_subplot(
            111
        )

        self.canvas = FigureCanvasTkAgg(
            self.figure,
            master=frame
        )

        self.canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # ========================================================
    # RULES TAB
    # ========================================================

    def _rules_tab(self):

        frame = ttk.Frame(
            self.notebook
        )

        self.notebook.add(
            frame,
            text="База знань"
        )

        ttk.Label(
            frame,
            text=(
                "Зелений — правило спрацювало. "
                "Червоний — правило було відхилено через конфлікт."
            ),
            style="Sub.TLabel"
        ).pack(
            anchor="w",
            padx=10,
            pady=8
        )

        columns = (
            "priority",
            "rule",
            "meaning"
        )

        self.rules_table = ttk.Treeview(
            frame,
            columns=columns,
            show="tree headings"
        )

        self.rules_table.heading(
            "#0",
            text="ID"
        )

        self.rules_table.heading(
            "priority",
            text="Пріоритет"
        )

        self.rules_table.heading(
            "rule",
            text="IF → THEN"
        )

        self.rules_table.heading(
            "meaning",
            text="Пояснення"
        )

        self.rules_table.column(
            "#0",
            width=60
        )

        self.rules_table.column(
            "priority",
            width=80,
            anchor="center"
        )

        self.rules_table.column(
            "rule",
            width=500
        )

        self.rules_table.column(
            "meaning",
            width=450
        )

        bar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.rules_table.yview
        )

        self.rules_table.configure(
            yscrollcommand=bar.set
        )

        self.rules_table.pack(
            side="left",
            fill="both",
            expand=True
        )

        bar.pack(
            side="right",
            fill="y"
        )

        self.rules_table.tag_configure(
            "fired",
            background=GREEN_LIGHT,
            foreground=GREEN_DARK
        )

        self.rules_table.tag_configure(
            "rejected",
            background=RED_LIGHT,
            foreground=RED
        )


    # ========================================================
    # FORM
    # ========================================================

    def _defaults(self):

        for spec in INPUT_FACTS:

            self._set_field(
                spec["name"],
                spec["default"]
            )

        self.scenario.set("")

        self.result = None

        self.decision_label.configure(
            text="Рекомендація ще не сформована",
            foreground=GREEN
        )

        self.status.set(
            "Встановлено стандартні значення."
        )

        self._set_text(
            self.chain_text,
            "РЕЗУЛЬТАТ ВИВЕДЕННЯ\n"
            + "=" * 60
            + "\n\n"
            "Натисніть «Сформувати рекомендацію»."
        )

        self._show_rules()
        self._draw_graph()


    def _set_field(self, name, value):

        spec = fact_spec(name)

        if value is None:

            self.fields[name].set(
                "" if spec["type"] == "int"
                else NOT_SET
            )

        elif spec["type"] == "bool":

            self.fields[name].set(
                "так" if value else "ні"
            )

        elif spec["type"] == "enum":

            titles = spec.get(
                "titles",
                {}
            )

            self.fields[name].set(
                (
                    "%s — %s"
                    % (
                        value,
                        titles[value]
                    )
                )
                if value in titles
                else str(value)
            )

        else:

            self.fields[name].set(
                str(value)
            )


    def _load_scenario(self):

        chosen = self.scenario.get().split(
            " — "
        )[0]

        scenario = next(
            s
            for s in TEST_SCENARIOS
            if s["id"] == chosen
        )

        for spec in INPUT_FACTS:

            self._set_field(
                spec["name"],
                scenario["facts"].get(
                    spec["name"]
                )
            )

        self.status.set(
            "Завантажено %s: %s"
            % (
                scenario["id"],
                scenario["name"]
            )
        )


    def _collect(self):

        facts = {}

        for spec in INPUT_FACTS:

            raw = self.fields[
                spec["name"]
            ].get().strip()

            if raw in (
                "",
                NOT_SET
            ):
                continue

            if spec["type"] == "bool":

                facts[
                    spec["name"]
                ] = raw == "так"

            elif spec["type"] == "enum":

                facts[
                    spec["name"]
                ] = raw.split(
                    " — "
                )[0]

            else:

                try:

                    value = int(raw)

                    if not (
                        spec["min"]
                        <= value
                        <= spec["max"]
                    ):
                        raise ValueError

                    facts[
                        spec["name"]
                    ] = value

                except ValueError:

                    self.status.set(
                        "Факт «%s»: введіть число від %d до %d."
                        % (
                            spec["label"],
                            spec["min"],
                            spec["max"]
                        )
                    )

                    return None

        return facts


    # ========================================================
    # SWITCH KB
    # ========================================================

    def _switch_kb(self):

        self.result = None

        self._show_rules()
        self._draw_graph()

        self.status.set(
            "Використовується %s база знань (%d правил)."
            % (
                "розширена"
                if self.extended.get()
                else "базова",
                len(
                    all_rules(
                        self.extended.get()
                    )
                )
            )
        )


    # ========================================================
    # RUN
    # ========================================================

    def run(self):

        facts = self._collect()

        if facts is None:
            return

        self.result = infer(
            all_rules(
                self.extended.get()
            ),
            facts
        )

        content = (
            "ЛАНЦЮЖОК ЛОГІЧНОГО ВИВЕДЕННЯ\n"
            + "=" * 65
            + "\n\n"
            + chain_text(self.result)
            + "\n\n"
            + self._decision_block()
            + "\n\n"
            + "ПРОТОКОЛ ВИВЕДЕННЯ\n"
            + "=" * 65
            + "\n"
            + explanation_text(self.result)
        )

        self._set_text(
            self.chain_text,
            content
        )

        self._show_rules()
        self._draw_graph()

        decision = self.result.decision

        self.decision_label.configure(
            text=(
                DECISIONS[decision]["label"]
                if decision
                else "Рішення не сформовано"
            ),
            foreground=(
                GREEN
                if decision
                else RED
            )
        )

        self.status.set(
            "Виведення завершено за %d циклів. "
            "Активовані правила: %s%s"
            % (
                self.result.cycles,
                ", ".join(
                    self.result.fired_ids()
                )
                or "жодного",
                self._expected_note(facts)
            )
        )

        self.notebook.select(0)


    def _expected_note(self, facts):

        for scenario in TEST_SCENARIOS:

            if scenario["facts"] != facts:
                continue

            key = (
                "expect_extended"
                if (
                    self.extended.get()
                    and "expect_extended"
                    in scenario
                )
                else "expect"
            )

            expected = scenario[key]

            return (
                "   |   %s: очікувалося %s — %s"
                % (
                    scenario["id"],
                    expected,
                    (
                        "збіг"
                        if self.result.decision == expected
                        else "розбіжність"
                    )
                )
            )

        return ""


    def _decision_block(self):

        decision = self.result.decision

        if not decision:

            return (
                "РІШЕННЯ НЕ СФОРМОВАНО\n"
                "Для заданих фактів недостатньо "
                "умов для формування рекомендації."
            )

        info = DECISIONS[decision]

        return (
            "РЕКОМЕНДАЦІЯ\n"
            + "=" * 65
            + "\n"
            + info["label"]
            + "\n\n"
            + info["text"]
            + "\n\n"
            + "Код рішення: "
            + decision
            + "\n"
            + "Сформовано правилом: "
            + self.result.source[GOAL_FACT]
        )


    # ========================================================
    # TEXT
    # ========================================================

    def _set_text(
        self,
        widget,
        content
    ):

        widget.configure(
            state="normal"
        )

        widget.delete(
            "1.0",
            "end"
        )

        widget.insert(
            "end",
            content
        )

        widget.configure(
            state="disabled"
        )


    # ========================================================
    # SHOW RULES
    # ========================================================

    def _show_rules(self):

        self.rules_table.delete(
            *self.rules_table.get_children()
        )

        fired = (
            set(
                self.result.fired_ids()
            )
            if self.result
            else set()
        )

        rejected = (
            {
                item["rule"]["id"]
                for item in self.result.rejected
            }
            if self.result
            else set()
        )

        for rule in all_rules(
            self.extended.get()
        ):

            tag = (
                "fired"
                if rule["id"] in fired
                else (
                    "rejected"
                    if rule["id"] in rejected
                    else ""
                )
            )

            self.rules_table.insert(
                "",
                "end",
                text=rule["id"],
                values=(
                    rule["priority"],
                    rule_text(rule),
                    rule["text"]
                ),
                tags=(tag,)
                if tag
                else ()
            )


    # ========================================================
    # GRAPH
    # ========================================================

    def _draw_graph(self):

        if not HAS_MATPLOTLIB:
            return

        rules = all_rules(
            self.extended.get()
        )

        axes = self.axes

        axes.clear()

        axes.set_facecolor(
            BG
        )

        axes.set_xticks([])
        axes.set_yticks([])

        for spine in axes.spines.values():
            spine.set_visible(False)

        # ----------------------------------------------------
        # Розподіл вузлів по рівнях
        # ----------------------------------------------------

        column = {
            spec["name"]: 0
            for spec in INPUT_FACTS
        }

        changed = True

        while changed:

            changed = False

            for rule in rules:

                target = rule["then"][0]

                if target == GOAL_FACT:
                    continue

                sources = condition_vars(
                    rule["if"]
                )

                known_sources = [
                    name
                    for name in sources
                    if name in column
                ]

                if (
                    known_sources
                    and all(
                        name in column
                        for name in sources
                    )
                ):

                    new_column = (
                        max(
                            column[name]
                            for name in sources
                        )
                        + 1
                    )

                    if (
                        target not in column
                        or column[target]
                        < new_column
                    ):

                        column[target] = new_column
                        changed = True

        last = (
            max(column.values())
            + 1
        )

        for code in DECISIONS:

            column[code] = last

        groups = {}

        for name, index in column.items():

            groups.setdefault(
                index,
                []
            ).append(name)

        position = {}

        for index, names in groups.items():

            count = len(names)

            for order, name in enumerate(names):

                y = (
                    -(order - (count - 1) / 2)
                    * 1.15
                )

                position[name] = (
                    index * 3.8,
                    y
                )

        fired = (
            set(
                self.result.fired_ids()
            )
            if self.result
            else set()
        )

        # ----------------------------------------------------
        # Стрілки
        # ----------------------------------------------------

        for rule in rules:

            target = rule["then"][0]

            if target == GOAL_FACT:

                target = rule["then"][1]

            active = (
                rule["id"] in fired
            )

            for name in set(
                condition_vars(
                    rule["if"]
                )
            ):

                if (
                    name not in position
                    or target not in position
                ):
                    continue

                x1, y1 = position[name]
                x2, y2 = position[target]

                axes.annotate(
                    "",
                    xy=(
                        x2 - 0.85,
                        y2
                    ),
                    xytext=(
                        x1 + 0.85,
                        y1
                    ),
                    arrowprops=dict(
                        arrowstyle="-|>",
                        color=(
                            GREEN
                            if active
                            else BORDER
                        ),
                        linewidth=(
                            1.8
                            if active
                            else 0.8
                        ),
                        alpha=(
                            1.0
                            if active
                            else 0.5
                        )
                    )
                )

            if active:

                source_names = condition_vars(
                    rule["if"]
                )

                if source_names:

                    first = source_names[0]

                    if (
                        first in position
                        and target in position
                    ):

                        x1, y1 = position[first]
                        x2, y2 = position[target]

                        axes.text(
                            (
                                x1 + x2
                            ) / 2,
                            (
                                y1 + y2
                            ) / 2 + 0.12,
                            rule["id"],
                            color=GREEN_DARK,
                            fontsize=7,
                            ha="center",
                            fontweight="bold"
                        )

        # ----------------------------------------------------
        # Вузли
        # ----------------------------------------------------

        derived = (
            self.result.facts
            if self.result
            else {}
        )

        input_names = {
            spec["name"]
            for spec in INPUT_FACTS
        }

        intermediate_names = {
            spec["name"]
            for spec in INTERMEDIATE_FACTS
        }

        for name, (x, y) in position.items():

            if name in DECISIONS:

                face = ORANGE_LIGHT
                line = ORANGE

                if (
                    derived.get(GOAL_FACT)
                    == name
                ):

                    face = GREEN_LIGHT
                    line = GREEN

            elif name in input_names:

                face = BLUE_LIGHT
                line = BLUE

            elif name in intermediate_names:

                if name in derived:

                    face = GREEN_LIGHT
                    line = GREEN

                else:

                    face = CARD
                    line = BORDER

            else:

                face = CARD
                line = BORDER

            label = (
                fact_spec(name)["label"]
                if name not in DECISIONS
                else DECISIONS[name]["label"]
            )

            axes.text(
                x,
                y,
                label,
                ha="center",
                va="center",
                fontsize=7.5,
                color=TEXT,
                wrap=True,
                bbox=dict(
                    boxstyle="round,pad=0.45",
                    facecolor=face,
                    edgecolor=line,
                    linewidth=1.3
                )
            )

        axes.set_xlim(
            -1.5,
            last * 3.8 + 2
        )

        ys = [
            point[1]
            for point in position.values()
        ]

        if ys:

            axes.set_ylim(
                min(ys) - 1.2,
                max(ys) + 1.2
            )

        axes.set_title(
            "БАЗА ЗНАНЬ SMARTMARKET\n"
            "початкові параметри → проміжні висновки → рекомендація",
            color=TEXT,
            fontsize=11,
            fontweight="bold",
            pad=12
        )

        self.figure.tight_layout(
            pad=1.5
        )

        self.canvas.draw_idle()


# ============================================================
# 13. ЗАПУСК
# ============================================================

def main():

    root = tk.Tk()

    Application(root)

    root.mainloop()


if __name__ == "__main__":
    main()