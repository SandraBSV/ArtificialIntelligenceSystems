import json
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

import joblib
import pandas as pd


# ============================================================
# НАЛАШТУВАННЯ ШЛЯХІВ
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

MODELS_DIR = BASE_DIR / "models"
RESULTS_PATH = BASE_DIR / "model_results.csv"
METADATA_PATH = BASE_DIR / "metadata.json"


# ============================================================
# ОСНОВНИЙ КЛАС
# ============================================================

class CarPriceApp:

    # ========================================================
    # КОЛЬОРОВА СХЕМА
    # ========================================================

    BG = "#0F0B1A"
    PANEL = "#171126"
    PANEL_2 = "#211638"
    CARD = "#2A1D42"
    BORDER = "#493365"

    TEXT = "#F3E8FF"
    MUTED = "#B8A9C9"

    ACCENT = "#A78BFA"
    ACCENT_2 = "#8B5CF6"

    SUCCESS = "#2DD4BF"
    WARNING = "#FBBF24"

    # ========================================================
    # ІНІЦІАЛІЗАЦІЯ
    # ========================================================

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Car Price Prediction"
        )

        self.root.geometry(
            "1500x860"
        )

        self.root.minsize(
            1180,
            720
        )

        self.root.configure(
            bg=self.BG
        )

        self.metadata = self.load_metadata()

        self.results_df = self.load_results()

        self.loaded_models = {}

        self.model_files = (
            self.metadata["model_files"]
        )

        self.model_names = list(
            self.model_files.keys()
        )

        self.setup_styles()

        self.build_interface()

    # ========================================================
    # ЗАВАНТАЖЕННЯ ДАНИХ ПРО НАВЧЕНІ МОДЕЛІ
    # ========================================================

    def load_metadata(self):

        if not METADATA_PATH.exists():

            messagebox.showerror(
                "Моделі ще не підготовлені",

                "Не знайдено metadata.json.\n\n"
                "Спочатку один раз запустіть "
                "train_models.py."
            )

            raise SystemExit

        with open(
            METADATA_PATH,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    # ========================================================

    def load_results(self):

        if RESULTS_PATH.exists():

            return pd.read_csv(
                RESULTS_PATH
            )

        return pd.DataFrame()

    # ========================================================

    def get_model(
        self,
        model_name
    ):

        if model_name in self.loaded_models:

            return self.loaded_models[
                model_name
            ]

        model_path = (
            MODELS_DIR
            / self.model_files[model_name]
        )

        if not model_path.exists():

            raise FileNotFoundError(
                f"Не знайдено файл моделі:\n"
                f"{model_path}\n\n"
                f"Запустіть train_models.py."
            )

        model = joblib.load(
            model_path
        )

        self.loaded_models[
            model_name
        ] = model

        return model

    # ========================================================
    # СТИЛІ
    # ========================================================

    def setup_styles(self):

        self.style = ttk.Style()

        try:

            self.style.theme_use(
                "clam"
            )

        except tk.TclError:

            pass

        # ----------------------------------------------------
        # Основні фрейми
        # ----------------------------------------------------

        self.style.configure(
            "App.TFrame",
            background=self.BG
        )

        self.style.configure(
            "Panel.TFrame",
            background=self.PANEL
        )

        self.style.configure(
            "Header.TFrame",
            background=self.PANEL_2
        )

        self.style.configure(
            "Card.TFrame",
            background=self.CARD
        )

        # ----------------------------------------------------
        # Заголовки
        # ----------------------------------------------------

        self.style.configure(
            "Title.TLabel",

            background=self.PANEL_2,

            foreground=self.TEXT,

            font=(
                "Segoe UI",
                18,
                "bold"
            )
        )

        self.style.configure(
            "Subtitle.TLabel",

            background=self.PANEL_2,

            foreground=self.MUTED,

            font=(
                "Segoe UI",
                9
            )
        )

        self.style.configure(
            "PanelTitle.TLabel",

            background=self.PANEL,

            foreground=self.TEXT,

            font=(
                "Segoe UI",
                12,
                "bold"
            )
        )

        # ----------------------------------------------------
        # Текст
        # ----------------------------------------------------

        self.style.configure(
            "Field.TLabel",

            background=self.PANEL,

            foreground=self.MUTED,

            font=(
                "Segoe UI",
                9
            )
        )

        self.style.configure(
            "Body.TLabel",

            background=self.PANEL,

            foreground=self.MUTED,

            font=(
                "Segoe UI",
                10
            )
        )

        # ----------------------------------------------------
        # Результат
        # ----------------------------------------------------

        self.style.configure(
            "Result.TLabel",

            background=self.CARD,

            foreground=self.SUCCESS,

            font=(
                "Segoe UI",
                20,
                "bold"
            )
        )

        self.style.configure(
            "ResultCaption.TLabel",

            background=self.CARD,

            foreground=self.MUTED,

            font=(
                "Segoe UI",
                9
            )
        )

        # ----------------------------------------------------
        # Кнопки
        # ----------------------------------------------------

        self.style.configure(
            "Accent.TButton",

            background=self.ACCENT_2,

            foreground="#FFFFFF",

            borderwidth=0,

            padding=(
                16,
                10
            ),

            font=(
                "Segoe UI",
                9,
                "bold"
            )
        )

        self.style.map(
            "Accent.TButton",

            background=[
                (
                    "active",
                    self.ACCENT
                ),

                (
                    "pressed",
                    "#7C3AED"
                )
            ]
        )

        self.style.configure(
            "Secondary.TButton",

            background=self.CARD,

            foreground=self.TEXT,

            borderwidth=1,

            padding=(
                14,
                10
            ),

            font=(
                "Segoe UI",
                9
            )
        )

        self.style.map(
            "Secondary.TButton",

            background=[
                (
                    "active",
                    self.BORDER
                )
            ]
        )

        # ----------------------------------------------------
        # Combobox
        # ----------------------------------------------------

        self.style.configure(
            "Modern.TCombobox",

            fieldbackground=self.CARD,

            background=self.CARD,

            foreground=self.TEXT,

            arrowcolor=self.ACCENT,

            bordercolor=self.BORDER,

            padding=6
        )

        self.style.map(
            "Modern.TCombobox",

            fieldbackground=[
                (
                    "readonly",
                    self.CARD
                )
            ],

            foreground=[
                (
                    "readonly",
                    self.TEXT
                )
            ]
        )

        self.root.option_add(
            "*TCombobox*Listbox.background",
            self.CARD
        )

        self.root.option_add(
            "*TCombobox*Listbox.foreground",
            self.TEXT
        )

        self.root.option_add(
            "*TCombobox*Listbox.selectBackground",
            self.ACCENT_2
        )

        self.root.option_add(
            "*TCombobox*Listbox.selectForeground",
            "#FFFFFF"
        )

    # ========================================================
    # ІНТЕРФЕЙС
    # ========================================================

    def build_interface(self):

        main = ttk.Frame(
            self.root,

            style="App.TFrame"
        )

        main.pack(
            fill=tk.BOTH,
            expand=True
        )

        # ----------------------------------------------------
        # HEADER
        # ----------------------------------------------------

        header = ttk.Frame(
            main,

            style="Header.TFrame",

            padding=(
                24,
                15
            )
        )

        header.pack(
            fill=tk.X
        )

        ttk.Label(
            header,

            text="CAR PRICE PREDICTION",

            style="Title.TLabel"
        ).pack(
            anchor="w"
        )

        ttk.Label(
            header,

            text=(
                "Used Car Marketplace • "
                "Regression Models"
            ),

            style="Subtitle.TLabel"
        ).pack(
            anchor="w",

            pady=(
                4,
                0
            )
        )

        # ----------------------------------------------------
        # WORKSPACE
        # ----------------------------------------------------

        workspace = ttk.Frame(
            main,

            style="App.TFrame",

            padding=18
        )

        workspace.pack(
            fill=tk.BOTH,
            expand=True
        )

        # ----------------------------------------------------
        # ЛІВА ПАНЕЛЬ
        # ----------------------------------------------------

        left = ttk.Frame(
            workspace,

            style="Panel.TFrame",

            padding=24
        )

        left.pack(
            side=tk.LEFT,

            fill=tk.BOTH,

            expand=True,

            padx=(
                0,
                14
            )
        )

        # ----------------------------------------------------
        # ПРАВА ПАНЕЛЬ
        # ----------------------------------------------------

        right = ttk.Frame(
            workspace,

            style="Panel.TFrame",

            width=470,

            padding=20
        )

        right.pack(
            side=tk.RIGHT,

            fill=tk.Y
        )

        right.pack_propagate(
            False
        )

        self.build_input_panel(
            left
        )

        self.build_result_panel(
            right
        )

    # ========================================================
    # ПАНЕЛЬ ВВЕДЕННЯ
    # ========================================================

    def build_input_panel(
        self,
        parent
    ):

        ttk.Label(
            parent,

            text="ПАРАМЕТРИ АВТОМОБІЛЯ",

            style="PanelTitle.TLabel"
        ).pack(
            anchor="w",

            pady=(
                0,
                20
            )
        )

        form = ttk.Frame(
            parent,

            style="Panel.TFrame"
        )

        form.pack(
            fill=tk.X
        )

        form.columnconfigure(
            0,
            weight=1
        )

        form.columnconfigure(
            1,
            weight=1
        )

        categories = (
            self.metadata["categories"]
        )

        self.input_vars = {}

        # ----------------------------------------------------
        # Категоріальні поля
        # ----------------------------------------------------

        fields = [

            (
                "brand",
                "Марка автомобіля"
            ),

            (
                "model",
                "Модель"
            ),

            (
                "fuel_type",
                "Тип палива"
            ),

            (
                "transmission",
                "Коробка передач"
            )
        ]

        for index, (
            column,
            label
        ) in enumerate(fields):

            row = index // 2

            col = index % 2

            field_frame = ttk.Frame(
                form,

                style="Panel.TFrame"
            )

            field_frame.grid(
                row=row,

                column=col,

                sticky="ew",

                padx=(
                    (0, 18)
                    if col == 0
                    else (0, 0)
                ),

                pady=(
                    0,
                    15
                )
            )

            ttk.Label(
                field_frame,

                text=label + ":",

                style="Field.TLabel"
            ).pack(
                anchor="w"
            )

            values = categories.get(
                column,
                []
            )

            default = (
                values[0]
                if values
                else ""
            )

            variable = tk.StringVar(
                value=default
            )

            self.input_vars[
                column
            ] = variable

            combo = ttk.Combobox(
                field_frame,

                textvariable=variable,

                values=values,

                state="readonly",

                style="Modern.TCombobox"
            )

            combo.pack(
                fill=tk.X,

                pady=(
                    6,
                    0
                )
            )

        # ====================================================
        # ЧИСЛОВІ ПАРАМЕТРИ
        # ====================================================

        numeric_frame = ttk.Frame(
            form,

            style="Panel.TFrame"
        )

        numeric_frame.grid(
            row=2,

            column=0,

            columnspan=2,

            sticky="ew",

            pady=(
                4,
                18
            )
        )

        numeric_frame.columnconfigure(
            0,
            weight=1
        )

        numeric_frame.columnconfigure(
            1,
            weight=1
        )

        # ----------------------------------------------------
        # Рік
        # ----------------------------------------------------

        self.year_var = tk.StringVar(
            value="2015"
        )

        year_frame = ttk.Frame(
            numeric_frame,

            style="Panel.TFrame"
        )

        year_frame.grid(
            row=0,

            column=0,

            sticky="ew",

            padx=(
                0,
                18
            )
        )

        ttk.Label(
            year_frame,

            text="Рік випуску:",

            style="Field.TLabel"
        ).pack(
            anchor="w"
        )

        tk.Entry(
            year_frame,

            textvariable=self.year_var,

            bg=self.CARD,

            fg=self.TEXT,

            insertbackground=self.TEXT,

            relief=tk.FLAT,

            bd=0,

            font=(
                "Segoe UI",
                10
            )
        ).pack(
            fill=tk.X,

            ipady=8,

            pady=(
                6,
                0
            )
        )

        # ----------------------------------------------------
        # Об'єм двигуна
        # ----------------------------------------------------

        self.engine_size_var = tk.StringVar(
            value="2.0"
        )

        engine_frame = ttk.Frame(
            numeric_frame,

            style="Panel.TFrame"
        )

        engine_frame.grid(
            row=0,

            column=1,

            sticky="ew"
        )

        ttk.Label(
            engine_frame,

            text="Об'єм двигуна, л:",

            style="Field.TLabel"
        ).pack(
            anchor="w"
        )

        tk.Entry(
            engine_frame,

            textvariable=self.engine_size_var,

            bg=self.CARD,

            fg=self.TEXT,

            insertbackground=self.TEXT,

            relief=tk.FLAT,

            bd=0,

            font=(
                "Segoe UI",
                10
            )
        ).pack(
            fill=tk.X,

            ipady=8,

            pady=(
                6,
                0
            )
        )

        # ----------------------------------------------------
        # Пробіг
        # ----------------------------------------------------

        mileage_frame = ttk.Frame(
            numeric_frame,

            style="Panel.TFrame"
        )

        mileage_frame.grid(
            row=1,

            column=0,

            columnspan=2,

            sticky="ew",

            pady=(
                15,
                0
            )
        )

        ttk.Label(
            mileage_frame,

            text="Пробіг, км:",

            style="Field.TLabel"
        ).pack(
            anchor="w"
        )

        self.mileage_var = tk.StringVar(
            value="100000"
        )

        tk.Entry(
            mileage_frame,

            textvariable=self.mileage_var,

            bg=self.CARD,

            fg=self.TEXT,

            insertbackground=self.TEXT,

            relief=tk.FLAT,

            bd=0,

            font=(
                "Segoe UI",
                10
            )
        ).pack(
            fill=tk.X,

            ipady=8,

            pady=(
                6,
                0
            )
        )

        # ====================================================
        # ВИБІР МОДЕЛІ
        # ====================================================

        ttk.Label(
            parent,

            text="МОДЕЛЬ ДЛЯ ПРОГНОЗУ",

            style="PanelTitle.TLabel"
        ).pack(
            anchor="w",

            pady=(
                8,
                12
            )
        )

        self.model_var = tk.StringVar(
            value=self.model_names[0]
        )

        ttk.Combobox(
            parent,

            textvariable=self.model_var,

            values=self.model_names,

            state="readonly",

            width=38,

            style="Modern.TCombobox"
        ).pack(
            anchor="w",

            pady=(
                0,
                18
            )
        )

        # ====================================================
        # КНОПКИ
        # ====================================================

        buttons = ttk.Frame(
            parent,

            style="Panel.TFrame"
        )

        buttons.pack(
            anchor="w",

            pady=(
                0,
                18
            )
        )

        ttk.Button(
            buttons,

            text="Спрогнозувати вартість",

            style="Accent.TButton",

            command=self.predict_price
        ).pack(
            side=tk.LEFT,

            padx=(
                0,
                12
            )
        )

        ttk.Button(
            buttons,

            text="Результати моделей",

            style="Secondary.TButton",

            command=self.show_model_results
        ).pack(
            side=tk.LEFT,

            padx=(
                0,
                12
            )
        )

        ttk.Button(
            buttons,

            text="Очистити",

            style="Secondary.TButton",

            command=self.clear_output
        ).pack(
            side=tk.LEFT
        )

        # ====================================================
        # СТАТУС
        # ====================================================

        self.status_label = ttk.Label(
            parent,

            text=(
                "Готово до прогнозування. "
                "Повторне навчання не потрібне."
            ),

            style="Body.TLabel"
        )

        self.status_label.pack(
            anchor="w",

            pady=(
                20,
                0
            )
        )

    # ========================================================
    # ПАНЕЛЬ РЕЗУЛЬТАТУ
    # ========================================================

    def build_result_panel(
        self,
        parent
    ):

        ttk.Label(
            parent,

            text="РЕЗУЛЬТАТ ПРОГНОЗУ",

            style="PanelTitle.TLabel"
        ).pack(
            anchor="w",

            pady=(
                0,
                15
            )
        )

        price_card = ttk.Frame(
            parent,

            style="Card.TFrame",

            padding=18
        )

        price_card.pack(
            fill=tk.X,

            pady=(
                0,
                14
            )
        )

        ttk.Label(
            price_card,

            text="ПРОГНОЗОВАНА ВАРТІСТЬ",

            style="ResultCaption.TLabel"
        ).pack(
            anchor="w"
        )

        self.price_label = ttk.Label(
            price_card,

            text="—",

            style="Result.TLabel"
        )

        self.price_label.pack(
            anchor="w",

            pady=(
                8,
                0
            )
        )

        self.model_used_label = ttk.Label(
            price_card,

            text="",

            style="ResultCaption.TLabel"
        )

        self.model_used_label.pack(
            anchor="w",

            pady=(
                6,
                0
            )
        )

        # ====================================================
        # TEXT
        # ====================================================

        self.info_text = tk.Text(
            parent,

            wrap=tk.WORD,

            state=tk.DISABLED,

            font=(
                "Segoe UI",
                10
            ),

            bg=self.CARD,

            fg=self.TEXT,

            insertbackground=self.TEXT,

            selectbackground=self.ACCENT_2,

            selectforeground="#FFFFFF",

            relief=tk.FLAT,

            bd=0,

            padx=14,

            pady=14
        )

        self.info_text.pack(
            fill=tk.BOTH,

            expand=True
        )

        self.info_text.tag_configure(
            "title",

            foreground=self.ACCENT,

            font=(
                "Segoe UI",
                11,
                "bold"
            )
        )

        self.info_text.tag_configure(
            "normal",

            foreground=self.TEXT,

            font=(
                "Segoe UI",
                10
            )
        )

        self.info_text.tag_configure(
            "muted",

            foreground=self.MUTED,

            font=(
                "Segoe UI",
                9
            )
        )

    # ========================================================
    # ЗБІР ДАНИХ
    # ========================================================

    def collect_input(self):

        try:

            year = int(
                self.year_var
                .get()
                .strip()
            )

        except ValueError:

            raise ValueError(
                "Рік випуску повинен бути "
                "цілим числом."
            )

        try:

            engine_size = float(
                self.engine_size_var
                .get()
                .strip()
                .replace(",", ".")
            )

        except ValueError:

            raise ValueError(
                "Об'єм двигуна повинен бути "
                "числом."
            )

        try:

            mileage = float(
                self.mileage_var
                .get()
                .strip()
                .replace(",", ".")
            )

        except ValueError:

            raise ValueError(
                "Пробіг повинен бути числом."
            )

        # ----------------------------------------------------
        # Перевірка значень
        # ----------------------------------------------------

        if year < 1900 or year > 2100:

            raise ValueError(
                "Рік автомобіля повинен бути "
                "від 1900 до 2100."
            )

        if engine_size <= 0:

            raise ValueError(
                "Об'єм двигуна повинен бути "
                "більшим за 0."
            )

        if mileage < 0:

            raise ValueError(
                "Пробіг не може бути від'ємним."
            )

        # ----------------------------------------------------
        # Попередження
        # ----------------------------------------------------

        warnings = []

        ranges = self.metadata.get(
            "numeric_ranges",
            {}
        )

        # Рік

        year_range = ranges.get(
            "year"
        )

        if year_range:

            if not (
                year_range["min"]
                <= year
                <= year_range["max"]
            ):

                warnings.append(
                    "Рік автомобіля виходить "
                    "за межі навчального датасету."
                )

        # Об'єм двигуна

        engine_range = ranges.get(
            "engine_size"
        )

        if engine_range:

            if not (
                engine_range["min"]
                <= engine_size
                <= engine_range["max"]
            ):

                warnings.append(
                    "Об'єм двигуна виходить "
                    "за межі навчального датасету."
                )

        # Пробіг

        mileage_range = ranges.get(
            "mileage"
        )

        if mileage_range:

            if not (
                mileage_range["min"]
                <= mileage
                <= mileage_range["max"]
            ):

                warnings.append(
                    "Пробіг виходить за межі "
                    "навчального датасету."
                )

        # ----------------------------------------------------
        # Формування запису
        # ----------------------------------------------------

        row = {

            "brand":
                self.input_vars[
                    "brand"
                ].get(),

            "model":
                self.input_vars[
                    "model"
                ].get(),

            "fuel_type":
                self.input_vars[
                    "fuel_type"
                ].get(),

            "transmission":
                self.input_vars[
                    "transmission"
                ].get(),

            "year":
                year,

            "engine_size":
                engine_size,

            "mileage":
                mileage
        }

        return (
            pd.DataFrame([row]),
            warnings
        )

    # ========================================================
    # ПРОГНОЗ
    # ========================================================

    def predict_price(self):

        try:

            model_name = (
                self.model_var.get()
            )

            input_df, warnings = (
                self.collect_input()
            )

            self.status_label.config(
                text=(
                    f"Виконується прогноз: "
                    f"{model_name}..."
                )
            )

            self.root.update_idletasks()

            model = self.get_model(
                model_name
            )

            prediction = float(
                model.predict(
                    input_df
                )[0]
            )

            # ------------------------------------------------
            # Відображення ціни
            # ------------------------------------------------

            self.price_label.config(
                text=f"${prediction:,.2f}"
            )

            self.model_used_label.config(
                text=(
                    f"Модель: {model_name}"
                )
            )

            self.show_prediction_details(
                input_df.iloc[0].to_dict(),

                model_name,

                prediction,

                warnings
            )

            self.status_label.config(
                text="Прогноз успішно отримано."
            )

        except Exception as error:

            self.status_label.config(
                text="Не вдалося виконати прогноз."
            )

            messagebox.showerror(
                "Помилка",

                str(error)
            )

    # ========================================================
    # ДЕТАЛІ ПРОГНОЗУ
    # ========================================================

    def show_prediction_details(
        self,
        row,
        model_name,
        prediction,
        warnings
    ):

        self.info_text.config(
            state=tk.NORMAL
        )

        self.info_text.delete(
            "1.0",
            tk.END
        )

        self.info_text.insert(
            tk.END,

            "ПАРАМЕТРИ АВТОМОБІЛЯ\n\n",

            "title"
        )

        labels = {

            "brand":
                "Марка",

            "model":
                "Модель",

            "fuel_type":
                "Тип палива",

            "transmission":
                "Коробка передач",

            "year":
                "Рік випуску",

            "engine_size":
                "Об'єм двигуна",

            "mileage":
                "Пробіг"
        }

        for key, value in row.items():

            text = (
                f"{labels[key]}: "
                f"{value}"
            )

            if key == "engine_size":

                text += " л"

            elif key == "mileage":

                text += " км"

            self.info_text.insert(
                tk.END,

                text + "\n",

                "normal"
            )

        # ----------------------------------------------------
        # Результат
        # ----------------------------------------------------

        self.info_text.insert(
            tk.END,

            "\nРЕЗУЛЬТАТ\n\n",

            "title"
        )

        self.info_text.insert(
            tk.END,

            f"Обрана модель: {model_name}\n"
            f"Прогнозована вартість: "
            f"${prediction:,.2f}\n",

            "normal"
        )

        # ----------------------------------------------------
        # Метрики
        # ----------------------------------------------------

        metric_row = (
            self.get_metric_row(
                model_name
            )
        )

        if metric_row is not None:

            self.info_text.insert(
                tk.END,

                "\nЯКІСТЬ МОДЕЛІ "
                "НА VALIDATION\n\n",

                "title"
            )

            self.info_text.insert(
                tk.END,

                f"MAE:  "
                f"{metric_row['MAE']:.2f}\n"

                f"RMSE: "
                f"{metric_row['RMSE']:.2f}\n"

                f"R²:   "
                f"{metric_row['R2']:.4f}\n",

                "normal"
            )

        # ----------------------------------------------------
        # Попередження
        # ----------------------------------------------------

        if warnings:

            self.info_text.insert(
                tk.END,

                "\nУВАГА\n\n",

                "title"
            )

            for warning in warnings:

                self.info_text.insert(
                    tk.END,

                    "• "
                    + warning
                    + "\n",

                    "muted"
                )

        self.info_text.config(
            state=tk.DISABLED
        )

    # ========================================================
    # РЕЗУЛЬТАТИ МОДЕЛЕЙ
    # ========================================================

    def get_metric_row(
        self,
        model_name
    ):

        if self.results_df.empty:

            return None

        rows = self.results_df[
            self.results_df["Model"]
            == model_name
        ]

        if rows.empty:

            return None

        return rows.iloc[0]

    # ========================================================

    def show_model_results(self):

        self.info_text.config(
            state=tk.NORMAL
        )

        self.info_text.delete(
            "1.0",
            tk.END
        )

        self.info_text.insert(
            tk.END,

            "РЕЗУЛЬТАТИ МОДЕЛЕЙ\n\n",

            "title"
        )

        if self.results_df.empty:

            self.info_text.insert(
                tk.END,

                "Файл model_results.csv "
                "не знайдено.\n"
                "Запустіть train_models.py.",

                "normal"
            )

            self.info_text.config(
                state=tk.DISABLED
            )

            return

        for _, row in (
            self.results_df.iterrows()
        ):

            self.info_text.insert(
                tk.END,

                f"{row['Model']}\n",

                "title"
            )

            self.info_text.insert(
                tk.END,

                f"Час навчання: "
                f"{row['Training Time (s)']:.3f} с\n"

                f"Час прогнозу: "
                f"{row['Prediction Time (s)']:.3f} с\n"

                f"MAE:  "
                f"{row['MAE']:.2f}\n"

                f"RMSE: "
                f"{row['RMSE']:.2f}\n"

                f"R²:   "
                f"{row['R2']:.4f}\n\n",

                "normal"
            )

        self.info_text.insert(
            tk.END,

            "Менші MAE та RMSE означають "
            "меншу середню помилку прогнозу. "
            "R² показує, наскільки добре модель "
            "пояснює варіацію ціни.",

            "muted"
        )

        self.info_text.config(
            state=tk.DISABLED
        )

        self.status_label.config(
            text=(
                "Показано результати "
                "навчання моделей."
            )
        )

    # ========================================================
    # ОЧИЩЕННЯ
    # ========================================================

    def clear_output(self):

        self.price_label.config(
            text="—"
        )

        self.model_used_label.config(
            text=""
        )

        self.info_text.config(
            state=tk.NORMAL
        )

        self.info_text.delete(
            "1.0",
            tk.END
        )

        self.info_text.config(
            state=tk.DISABLED
        )

        self.status_label.config(
            text=(
                "Готово до прогнозування. "
                "Повторне навчання не потрібне."
            )
        )


# ============================================================
# ЗАПУСК
# ============================================================

def main():

    root = tk.Tk()

    try:

        CarPriceApp(root)

    except SystemExit:

        root.destroy()

        return

    root.mainloop()


if __name__ == "__main__":

    main()