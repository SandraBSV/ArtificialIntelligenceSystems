"""
ЛАБОРАТОРНА РОБОТА №4
Прототип інтелектуальної системи підтримки прийняття рішень (IDSS)

Предметна область:
Оцінювання ринкової вартості та аналіз вигідності
пропозицій під час купівлі вживаних автомобілів.

AI-компонент:
Linear Regression.

Основна логіка:
idss_core.py

GUI:
    1) введення характеристик автомобіля;
    2) введення поточної ціни;
    3) запуск аналізу;
    4) відображення прогнозованої ринкової вартості;
    5) порівняння з поточною ціною;
    6) рекомендація системи;
    7) пояснення результату;
    8) Human-in-the-Loop.
"""

import tkinter as tk
from tkinter import messagebox, ttk

import idss_core as core


class DecisionSupportApp:

    # ========================================================
    # КОЛЬОРОВА СХЕМА
    # ========================================================

    BG = "#0B1220"
    PANEL = "#111827"
    PANEL_2 = "#172235"
    CARD = "#1E2B3D"
    CARD_2 = "#223248"

    BORDER = "#33465F"

    TEXT = "#F1F5F9"
    MUTED = "#94A3B8"

    ACCENT = "#60A5FA"
    ACCENT_2 = "#3B82F6"

    SUCCESS = "#34D399"
    WARNING = "#FBBF24"
    DANGER = "#F87171"

    WHITE = "#FFFFFF"

    def __init__(self, root):

        self.root = root

        self.root.title(
            "Used Car Decision Support System"
        )

        # ----------------------------------------------------
        # Розмір вікна
        # ----------------------------------------------------

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        width = min(1450, screen_width - 80)
        height = min(820, screen_height - 80)

        self.root.geometry(
            f"{width}x{height}"
        )

        self.root.minsize(
            1050,
            650
        )

        self.root.configure(
            bg=self.BG
        )

        # ----------------------------------------------------
        # AI
        # ----------------------------------------------------

        self.ai = core.AIComponent()

        self.last_result = None

        # ----------------------------------------------------
        # Запуск GUI
        # ----------------------------------------------------

        self.setup_styles()
        self.build_interface()
        self.load_example()
        self.show_startup_info()

    # ========================================================
    # СТИЛІ
    # ========================================================

    def setup_styles(self):

        self.style = ttk.Style()

        try:
            self.style.theme_use("clam")
        except tk.TclError:
            pass

        # ----------------------------------------------------
        # Frames
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
        # Labels
        # ----------------------------------------------------

        self.style.configure(
            "Title.TLabel",
            background=self.PANEL_2,
            foreground=self.TEXT,
            font=("Segoe UI", 19, "bold")
        )

        self.style.configure(
            "Subtitle.TLabel",
            background=self.PANEL_2,
            foreground=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "PanelTitle.TLabel",
            background=self.PANEL,
            foreground=self.TEXT,
            font=("Segoe UI", 11, "bold")
        )

        self.style.configure(
            "Field.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "Body.TLabel",
            background=self.PANEL,
            foreground=self.MUTED,
            font=("Segoe UI", 9)
        )

        self.style.configure(
            "Result.TLabel",
            background=self.CARD,
            foreground=self.SUCCESS,
            font=("Segoe UI", 22, "bold")
        )

        self.style.configure(
            "ResultCaption.TLabel",
            background=self.CARD,
            foreground=self.MUTED,
            font=("Segoe UI", 9)
        )

        # ----------------------------------------------------
        # Основна кнопка
        # ----------------------------------------------------

        self.style.configure(
            "Accent.TButton",
            background=self.ACCENT_2,
            foreground=self.WHITE,
            borderwidth=0,
            padding=(12, 10),
            font=("Segoe UI", 9, "bold")
        )

        self.style.map(
            "Accent.TButton",
            background=[
                ("active", self.ACCENT),
                ("pressed", "#2563EB")
            ]
        )

        # ----------------------------------------------------
        # Додаткові кнопки
        # ----------------------------------------------------

        self.style.configure(
            "Secondary.TButton",
            background=self.CARD,
            foreground=self.TEXT,
            borderwidth=1,
            padding=(10, 8),
            font=("Segoe UI", 9)
        )

        self.style.map(
            "Secondary.TButton",
            background=[
                ("active", self.BORDER)
            ]
        )

        self.style.configure(
            "Action.TButton",
            background=self.CARD_2,
            foreground=self.TEXT,
            borderwidth=1,
            padding=(8, 7),
            font=("Segoe UI", 8, "bold")
        )

        self.style.map(
            "Action.TButton",
            background=[
                ("active", self.BORDER)
            ]
        )

        # ----------------------------------------------------
        # Scrollbar
        # ----------------------------------------------------

        self.style.configure(
            "Dark.Vertical.TScrollbar",
            background=self.BORDER,
            troughcolor=self.CARD,
            bordercolor=self.CARD,
            arrowcolor=self.MUTED,
            borderwidth=0
        )

        self.style.map(
            "Dark.Vertical.TScrollbar",
            background=[
                ("active", self.ACCENT_2)
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
            padding=5
        )

        self.style.map(
            "Modern.TCombobox",
            fieldbackground=[
                ("readonly", self.CARD)
            ],
            foreground=[
                ("readonly", self.TEXT)
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
            self.WHITE
        )

    # ========================================================
    # ГОЛОВНИЙ ІНТЕРФЕЙС
    # ========================================================

    def build_interface(self):

        main = tk.Frame(
            self.root,
            bg=self.BG
        )

        main.pack(
            fill=tk.BOTH,
            expand=True,
            padx=18,
            pady=12
        )

        # ====================================================
        # HEADER
        # ====================================================

        header = tk.Frame(
            main,
            bg=self.PANEL_2
        )

        header.pack(
            fill=tk.X
        )

        header_content = tk.Frame(
            header,
            bg=self.PANEL_2
        )

        header_content.pack(
            fill=tk.X,
            padx=22,
            pady=14
        )

        tk.Label(
            header_content,
            text="USED CAR DECISION SUPPORT SYSTEM",
            bg=self.PANEL_2,
            fg=self.TEXT,
            font=("Segoe UI", 18, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            header_content,
            text=(
                "Оцінювання ринкової вартості та аналіз "
                "вигідності пропозицій • Лабораторна робота №4"
            ),
            bg=self.PANEL_2,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            pady=(4, 0)
        )

        # ====================================================
        # WORKSPACE
        # ====================================================

        workspace = tk.Frame(
            main,
            bg=self.BG
        )

        workspace.pack(
            fill=tk.BOTH,
            expand=True,
            pady=(12, 0)
        )

        # ----------------------------------------------------
        # LEFT PANEL
        # ----------------------------------------------------

        left = tk.Frame(
            workspace,
            bg=self.PANEL,
            width=500
        )

        left.pack(
            side=tk.LEFT,
            fill=tk.Y,
            padx=(0, 10)
        )

        left.pack_propagate(False)

        # ----------------------------------------------------
        # RIGHT PANEL
        # ----------------------------------------------------

        right = tk.Frame(
            workspace,
            bg=self.PANEL
        )

        right.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        self.build_input_panel(left)
        self.build_result_panel(right)

    # ========================================================
    # ЛІВА ПАНЕЛЬ
    # ========================================================

    def build_input_panel(self, parent):

        # ----------------------------------------------------
        # Заголовок
        # ----------------------------------------------------

        title_frame = tk.Frame(
            parent,
            bg=self.PANEL
        )

        title_frame.pack(
            fill=tk.X,
            padx=18,
            pady=(16, 8)
        )

        tk.Label(
            title_frame,
            text="ХАРАКТЕРИСТИКИ АВТОМОБІЛЯ",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w"
        )

        # ====================================================
        # SCROLLABLE FORM
        # ====================================================

        form_container = tk.Frame(
            parent,
            bg=self.PANEL
        )

        form_container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=12
        )

        canvas = tk.Canvas(
            form_container,
            bg=self.PANEL,
            highlightthickness=0,
            bd=0
        )

        scrollbar = ttk.Scrollbar(
            form_container,
            orient=tk.VERTICAL,
            command=canvas.yview,
            style="Dark.Vertical.TScrollbar"
        )

        self.form_frame = tk.Frame(
            canvas,
            bg=self.PANEL
        )

        self.form_window = canvas.create_window(
            (0, 0),
            window=self.form_frame,
            anchor="nw"
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        def update_scroll_region(event=None):

            canvas.configure(
                scrollregion=canvas.bbox("all")
            )

        def resize_form(event):

            canvas.itemconfigure(
                self.form_window,
                width=event.width
            )

        self.form_frame.bind(
            "<Configure>",
            update_scroll_region
        )

        canvas.bind(
            "<Configure>",
            resize_form
        )

        # ----------------------------------------------------
        # Mouse wheel
        # ----------------------------------------------------

        def mouse_wheel(event):

            canvas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas.bind_all(
            "<MouseWheel>",
            mouse_wheel
        )

        self.input_vars = {}

        # ====================================================
        # ВИЗНАЧЕННЯ ПОЛІВ
        # ====================================================

        categorical_columns = getattr(
            core,
            "CATEGORICAL_COLUMNS",
            []
        )

        categories = getattr(
            core,
            "CATEGORIES",
            {}
        )

        feature_columns = getattr(
            core,
            "FEATURE_COLUMNS",
            []
        )

        # ----------------------------------------------------
        # Поля, які використовуємо для GUI
        # ----------------------------------------------------

        preferred_fields = [
            "brand",
            "model",
            "fuel_type",
            "fuel",
            "transmission",
            "seller_type",
            "owner"
        ]

        available_fields = []

        for field in preferred_fields:

            if field in feature_columns:

                available_fields.append(field)

        # Якщо core має інші категоріальні поля —
        # додаємо їх автоматично
        for field in categorical_columns:

            if field not in available_fields:

                available_fields.append(field)

        # ====================================================
        # КАТЕГОРІАЛЬНІ ПОЛЯ
        # ====================================================

        if available_fields:

            self.add_section_title(
                self.form_frame,
                "ОСНОВНІ ХАРАКТЕРИСТИКИ"
            )

        grid = tk.Frame(
            self.form_frame,
            bg=self.PANEL
        )

        grid.pack(
            fill=tk.X,
            padx=8
        )

        grid.columnconfigure(
            0,
            weight=1
        )

        grid.columnconfigure(
            1,
            weight=1
        )

        for index, column in enumerate(
            available_fields
        ):

            row = index // 2
            col = index % 2

            field = tk.Frame(
                grid,
                bg=self.PANEL
            )

            field.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=6,
                pady=6
            )

            label = core.FIELD_LABELS.get(
                column,
                self.pretty_name(column)
            )

            tk.Label(
                field,
                text=label + ":",
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 8)
            ).pack(
                anchor="w"
            )

            values = categories.get(
                column,
                []
            )

            variable = tk.StringVar()

            self.input_vars[column] = variable

            if values:

                variable.set(
                    values[0]
                )

                combo = ttk.Combobox(
                    field,
                    textvariable=variable,
                    values=values,
                    state="readonly",
                    style="Modern.TCombobox"
                )

                combo.pack(
                    fill=tk.X,
                    pady=(3, 0)
                )

            else:

                entry = self.create_entry(
                    field,
                    variable
                )

                entry.pack(
                    fill=tk.X,
                    pady=(3, 0)
                )

        # ====================================================
        # ЧИСЛОВІ ПОЛЯ
        # ====================================================

        numeric_columns = getattr(
            core,
            "NUMERIC_COLUMNS",
            []
        )

        if numeric_columns:

            self.add_section_title(
                self.form_frame,
                "ЧИСЛОВІ ПАРАМЕТРИ"
            )

        numeric_grid = tk.Frame(
            self.form_frame,
            bg=self.PANEL
        )

        numeric_grid.pack(
            fill=tk.X,
            padx=8
        )

        numeric_grid.columnconfigure(
            0,
            weight=1
        )

        numeric_grid.columnconfigure(
            1,
            weight=1
        )

        numeric_grid.columnconfigure(
            2,
            weight=1
        )

        self.numeric_vars = {}

        for index, column in enumerate(
            numeric_columns
        ):

            row = index // 3
            col = index % 3

            field = tk.Frame(
                numeric_grid,
                bg=self.PANEL
            )

            field.grid(
                row=row,
                column=col,
                sticky="ew",
                padx=6,
                pady=6
            )

            label = core.FIELD_LABELS.get(
                column,
                self.pretty_name(column)
            )

            tk.Label(
                field,
                text=label + ":",
                bg=self.PANEL,
                fg=self.MUTED,
                font=("Segoe UI", 8)
            ).pack(
                anchor="w"
            )

            variable = tk.StringVar()

            self.numeric_vars[column] = variable

            entry = self.create_entry(
                field,
                variable
            )

            entry.pack(
                fill=tk.X,
                pady=(3, 0)
            )

        # ====================================================
        # ПОТОЧНА ЦІНА
        # ====================================================

        self.add_section_title(
            self.form_frame,
            "ЦІНА ПРОПОЗИЦІЇ"
        )

        price_card = tk.Frame(
            self.form_frame,
            bg=self.CARD,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )

        price_card.pack(
            fill=tk.X,
            padx=14,
            pady=(3, 12)
        )

        tk.Label(
            price_card,
            text="Поточна ціна автомобіля:",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(
            anchor="w",
            padx=12,
            pady=(9, 0)
        )

        self.current_price_var = tk.StringVar()

        price_entry = tk.Entry(
            price_card,
            textvariable=self.current_price_var,
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 13, "bold")
        )

        price_entry.pack(
            fill=tk.X,
            padx=12,
            pady=(2, 9),
            ipady=5
        )

        # ====================================================
        # Нижня ФІКСОВАНА панель
        # ====================================================

        self.build_bottom_controls(parent)

    # ========================================================
    # ДОПОМІЖНІ МЕТОДИ ФОРМИ
    # ========================================================

    def add_section_title(
        self,
        parent,
        text
    ):

        tk.Label(
            parent,
            text=text,
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 10, "bold")
        ).pack(
            anchor="w",
            padx=14,
            pady=(10, 4)
        )

    def create_entry(
        self,
        parent,
        variable
    ):

        return tk.Entry(
            parent,
            textvariable=variable,
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 9)
        )

    def pretty_name(self, name):

        return (
            str(name)
            .replace("_", " ")
            .capitalize()
        )

    # ========================================================
    # НИЖНЯ ПАНЕЛЬ
    # ========================================================

    def build_bottom_controls(self, parent):

        bottom = tk.Frame(
            parent,
            bg=self.PANEL
        )

        bottom.pack(
            side=tk.BOTTOM,
            fill=tk.X,
            padx=14,
            pady=(6, 12)
        )

        # ====================================================
        # КНОПКА АНАЛІЗУ
        # ====================================================

        self.analyze_button = ttk.Button(
            bottom,
            text="ОЦІНИТИ ПРОПОЗИЦІЮ",
            style="Accent.TButton",
            command=self.run_analysis
        )

        self.analyze_button.pack(
            fill=tk.X
        )

        # ====================================================
        # ДОДАТКОВІ КНОПКИ
        # ====================================================

        buttons = tk.Frame(
            bottom,
            bg=self.PANEL
        )

        buttons.pack(
            fill=tk.X,
            pady=(7, 0)
        )

        buttons.columnconfigure(
            0,
            weight=1
        )

        buttons.columnconfigure(
            1,
            weight=1
        )

        ttk.Button(
            buttons,
            text="Приклад даних",
            style="Secondary.TButton",
            command=self.load_example
        ).grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5)
        )

        ttk.Button(
            buttons,
            text="Очистити",
            style="Secondary.TButton",
            command=self.clear_output
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0)
        )

        # ====================================================
        # СТАТУС
        # ====================================================

        self.error_label = tk.Label(
            bottom,
            text="",
            bg=self.PANEL,
            fg=self.DANGER,
            font=("Segoe UI", 8, "bold"),
            anchor="w",
            justify=tk.LEFT,
            wraplength=450
        )

        self.error_label.pack(
            fill=tk.X,
            pady=(6, 0)
        )

        self.status_label = tk.Label(
            bottom,
            text="",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 8),
            anchor="w",
            justify=tk.LEFT,
            wraplength=450
        )

        self.status_label.pack(
            fill=tk.X,
            pady=(3, 0)
        )

        # ====================================================
        # HUMAN-IN-THE-LOOP
        # ====================================================

        separator = tk.Frame(
            bottom,
            bg=self.BORDER,
            height=1
        )

        separator.pack(
            fill=tk.X,
            pady=(8, 7)
        )

        tk.Label(
            bottom,
            text="РІШЕННЯ КОРИСТУВАЧА",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w"
        )

        tk.Label(
            bottom,
            text=(
                "AI формує рекомендацію, але остаточне "
                "рішення приймає користувач."
            ),
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 7),
            wraplength=450,
            justify=tk.LEFT
        ).pack(
            anchor="w",
            pady=(2, 5)
        )

        # ====================================================
        # КНОПКИ HITL
        # ====================================================

        actions = tk.Frame(
            bottom,
            bg=self.PANEL
        )

        actions.pack(
            fill=tk.X
        )

        actions.columnconfigure(
            0,
            weight=1
        )

        actions.columnconfigure(
            1,
            weight=1
        )

        actions.columnconfigure(
            2,
            weight=1
        )

        self.action_buttons = []

        action_data = [
            (
                "✓  ПІДТВЕРДИТИ",
                "ПІДТВЕРДЖЕНО"
            ),
            (
                "◷  МОНІТОРИНГ",
                "МОНІТОРИНГ"
            ),
            (
                "✕  ВІДХИЛИТИ",
                "ВІДХИЛЕНО"
            )
        ]

        for index, (text, code) in enumerate(
            action_data
        ):

            button = ttk.Button(
                actions,
                text=text,
                style="Action.TButton",
                state=tk.DISABLED,
                command=lambda c=code, i=index:
                    self.fix_user_decision(c, i)
            )

            button.grid(
                row=0,
                column=index,
                sticky="ew",
                padx=(0, 4) if index < 2 else (0, 0)
            )

            self.action_buttons.append(
                button
            )

        self.user_decision_label = tk.Label(
            bottom,
            text="Рішення користувача ще не зафіксовано.",
            bg=self.PANEL,
            fg=self.MUTED,
            font=("Segoe UI", 7),
            anchor="w",
            justify=tk.LEFT,
            wraplength=450
        )

        self.user_decision_label.pack(
            fill=tk.X,
            pady=(5, 0)
        )

    # ========================================================
    # ПРАВА ПАНЕЛЬ
    # ========================================================

    def build_result_panel(self, parent):

        # ====================================================
        # Верхні картки
        # ====================================================

        top = tk.Frame(
            parent,
            bg=self.PANEL
        )

        top.pack(
            fill=tk.X,
            padx=18,
            pady=(16, 0)
        )

        top.columnconfigure(
            0,
            weight=1
        )

        top.columnconfigure(
            1,
            weight=1
        )

        # ====================================================
        # AI RESULT
        # ====================================================

        result_section = tk.Frame(
            top,
            bg=self.PANEL
        )

        result_section.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 7)
        )

        tk.Label(
            result_section,
            text="РЕЗУЛЬТАТ AI-КОМПОНЕНТА",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            pady=(0, 9)
        )

        price_card = tk.Frame(
            result_section,
            bg=self.CARD
        )

        price_card.pack(
            fill=tk.X
        )

        tk.Label(
            price_card,
            text="ПРОГНОЗОВАНА РИНКОВА ВАРТІСТЬ",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=16,
            pady=(14, 0)
        )

        self.price_label = tk.Label(
            price_card,
            text="—",
            bg=self.CARD,
            fg=self.SUCCESS,
            font=("Segoe UI", 22, "bold")
        )

        self.price_label.pack(
            anchor="w",
            padx=16,
            pady=(3, 0)
        )

        self.delta_label = tk.Label(
            price_card,
            text="",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9, "bold"),
            anchor="w",
            justify=tk.LEFT,
            wraplength=380
        )

        self.delta_label.pack(
            fill=tk.X,
            padx=16,
            pady=(5, 0)
        )

        self.confidence_label = tk.Label(
            price_card,
            text="",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8),
            anchor="w",
            justify=tk.LEFT
        )

        self.confidence_label.pack(
            anchor="w",
            padx=16,
            pady=(5, 0)
        )

        self.model_label = tk.Label(
            price_card,
            text="",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8),
            anchor="w"
        )

        self.model_label.pack(
            anchor="w",
            padx=16,
            pady=(2, 13)
        )

        # ====================================================
        # RECOMMENDATION
        # ====================================================

        decision_section = tk.Frame(
            top,
            bg=self.PANEL
        )

        decision_section.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(7, 0)
        )

        tk.Label(
            decision_section,
            text="РЕКОМЕНДАЦІЯ СИСТЕМИ",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w",
            pady=(0, 9)
        )

        decision_card = tk.Frame(
            decision_section,
            bg=self.CARD
        )

        decision_card.pack(
            fill=tk.X
        )

        self.decision_label = tk.Label(
            decision_card,
            text="РІШЕННЯ НЕ СФОРМОВАНО",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 14, "bold"),
            anchor="w",
            justify=tk.LEFT,
            wraplength=390
        )

        self.decision_label.pack(
            anchor="w",
            padx=16,
            pady=(15, 0)
        )

        self.decision_text_label = tk.Label(
            decision_card,
            text=(
                "Введіть характеристики автомобіля "
                "та виконайте аналіз пропозиції."
            ),
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI", 9),
            anchor="w",
            justify=tk.LEFT,
            wraplength=390
        )

        self.decision_text_label.pack(
            fill=tk.X,
            padx=16,
            pady=(7, 0)
        )

        self.decision_mode_label = tk.Label(
            decision_card,
            text="",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 8),
            anchor="w",
            justify=tk.LEFT,
            wraplength=390
        )

        self.decision_mode_label.pack(
            fill=tk.X,
            padx=16,
            pady=(6, 14)
        )

        # ====================================================
        # ПОЯСНЕННЯ
        # ====================================================

        explanation_header = tk.Frame(
            parent,
            bg=self.PANEL
        )

        explanation_header.pack(
            fill=tk.X,
            padx=18,
            pady=(14, 8)
        )

        tk.Label(
            explanation_header,
            text="ПОЯСНЕННЯ РЕЗУЛЬТАТУ",
            bg=self.PANEL,
            fg=self.TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(
            anchor="w"
        )

        # ====================================================
        # TEXT AREA
        # ====================================================

        text_container = tk.Frame(
            parent,
            bg=self.PANEL
        )

        text_container.pack(
            fill=tk.BOTH,
            expand=True,
            padx=18,
            pady=(0, 16)
        )

        self.info_text = tk.Text(
            text_container,
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            selectbackground=self.ACCENT_2,
            selectforeground=self.WHITE,
            relief=tk.FLAT,
            bd=0,
            font=("Segoe UI", 9),
            padx=15,
            pady=12
        )

        self.info_text.pack(
            side=tk.LEFT,
            fill=tk.BOTH,
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            text_container,
            orient=tk.VERTICAL,
            command=self.info_text.yview,
            style="Dark.Vertical.TScrollbar"
        )

        scrollbar.pack(
            side=tk.RIGHT,
            fill=tk.Y
        )

        self.info_text.config(
            yscrollcommand=scrollbar.set
        )

        # ----------------------------------------------------
        # Теги
        # ----------------------------------------------------

        self.info_text.tag_configure(
            "title",
            foreground=self.ACCENT,
            font=("Segoe UI", 9, "bold"),
            spacing1=8,
            spacing3=4
        )

        self.info_text.tag_configure(
            "normal",
            foreground=self.TEXT,
            font=("Segoe UI", 9)
        )

        self.info_text.tag_configure(
            "muted",
            foreground=self.MUTED,
            font=("Segoe UI", 8)
        )

        self.info_text.tag_configure(
            "error",
            foreground=self.DANGER,
            font=("Segoe UI", 9, "bold")
        )

    # ========================================================
    # ЗБІР ВХІДНИХ ДАНИХ
    # ========================================================

    def collect_raw_input(self):

        raw = {}

        # ----------------------------------------------------
        # Категоріальні
        # ----------------------------------------------------

        for column, variable in self.input_vars.items():

            raw[column] = variable.get().strip()

        # ----------------------------------------------------
        # Числові
        # ----------------------------------------------------

        for column, variable in self.numeric_vars.items():

            raw[column] = variable.get().strip()

        # ----------------------------------------------------
        # Поточна ціна
        # ----------------------------------------------------

        raw["current_price"] = (
            self.current_price_var
            .get()
            .strip()
        )

        return raw

    # ========================================================
    # АНАЛІЗ
    # ========================================================

    def run_analysis(self):

        raw = self.collect_raw_input()

        self.error_label.config(
            text=""
        )

        self.status_label.config(
            text="Виконується аналіз..."
        )

        self.root.update_idletasks()

        try:

            result = core.analyze(
                raw,
                self.ai
            )

        except Exception as error:

            messagebox.showerror(
                "Помилка аналізу",
                str(error)
            )

            self.status_label.config(
                text="Аналіз не виконано."
            )

            return

        if not result.get("ok", False):

            self.show_validation_errors(
                result
            )

            return

        self.last_result = result

        self.show_result(
            result
        )

    # ========================================================
    # ПОМИЛКИ
    # ========================================================

    def show_validation_errors(
        self,
        result
    ):

        self.last_result = None

        for button in self.action_buttons:

            button.config(
                state=tk.DISABLED
            )

        errors = result.get(
            "errors",
            []
        )

        self.error_label.config(
            text=(
                "Некоректні вхідні дані — "
                f"знайдено помилок: {len(errors)}."
            )
        )

        # ----------------------------------------------------
        # Результат
        # ----------------------------------------------------

        self.price_label.config(
            text="—"
        )

        self.delta_label.config(
            text=""
        )

        self.confidence_label.config(
            text=""
        )

        self.model_label.config(
            text=""
        )

        # ----------------------------------------------------
        # Recommendation
        # ----------------------------------------------------

        self.decision_label.config(
            text="РІШЕННЯ НЕ СФОРМОВАНО",
            fg=self.DANGER
        )

        self.decision_text_label.config(
            text=(
                "Система не формує рекомендацію, "
                "поки вхідні дані не пройдуть перевірку."
            )
        )

        self.decision_mode_label.config(
            text=""
        )

        # ----------------------------------------------------
        # Explanation
        # ----------------------------------------------------

        self.info_text.config(
            state=tk.NORMAL
        )

        self.info_text.delete(
            "1.0",
            tk.END
        )

        self.info_text.insert(
            tk.END,
            "ПОМИЛКИ ВАЛІДАЦІЇ\n",
            "title"
        )

        for index, error in enumerate(
            errors,
            start=1
        ):

            self.info_text.insert(
                tk.END,
                f"{index}. {error}\n",
                "error"
            )

        self.info_text.insert(
            tk.END,
            "\nВиправте зазначені поля "
            "та повторіть аналіз.",
            "muted"
        )

        self.info_text.config(
            state=tk.DISABLED
        )

        self.status_label.config(
            text=(
                "Валідація не пройдена. "
                "AI-компонент не викликався."
            )
        )

    # ========================================================
    # КОЛІР РІШЕННЯ
    # ========================================================

    def decision_color(
        self,
        code
    ):

        colors = {

            "BUY_NOW":
                self.SUCCESS,

            "MARKET_FAIR_PRICE":
                self.ACCENT,

            "WAIT_BETTER_PRICE":
                self.WARNING
        }

        return colors.get(
            code,
            self.MUTED
        )

    # ========================================================
    # ВІДОБРАЖЕННЯ РЕЗУЛЬТАТУ
    # ========================================================

    def show_result(
        self,
        result
    ):

        predicted_price = result[
            "predicted_price"
        ]

        current_price = result[
            "current_price"
        ]

        delta = result[
            "delta"
        ]

        delta_percent = result[
            "delta_percent"
        ]

        # ----------------------------------------------------
        # Прогнозована ціна
        # ----------------------------------------------------

        self.price_label.config(
            text=f"$ {predicted_price:,.2f}"
        )

        # ----------------------------------------------------
        # Порівняння
        # ----------------------------------------------------

        if delta_percent < 0:

            delta_text = (
                f"Поточна ціна НИЖЧА за прогноз "
                f"на {abs(delta_percent):.2f}%\n"
                f"Різниця: $ {abs(delta):,.2f}"
            )

        elif delta_percent > 0:

            delta_text = (
                f"Поточна ціна ВИЩА за прогноз "
                f"на {delta_percent:.2f}%\n"
                f"Різниця: $ {delta:,.2f}"
            )

        else:

            delta_text = (
                "Поточна ціна збігається "
                "з прогнозованою."
            )

        self.delta_label.config(
            text=delta_text,
            fg=self.decision_color(
                result["decision"]
            )
        )

        # ----------------------------------------------------
        # Confidence
        # ----------------------------------------------------

        self.confidence_label.config(
            text=(
                f"Впевненість: "
                f"{result['confidence']:.2f} "
                f"({result['confidence_level']})\n"
                f"Час аналізу: "
                f"{result['elapsed_ms']:.1f} мс"
            )
        )

        # ----------------------------------------------------
        # Model
        # ----------------------------------------------------

        self.model_label.config(
            text=(
                f"AI-компонент: "
                f"{result['model_name']}"
            )
        )

        # ----------------------------------------------------
        # Recommendation
        # ----------------------------------------------------

        decision = result[
            "decision"
        ]

        self.decision_label.config(
            text=result[
                "decision_title"
            ],
            fg=self.decision_color(
                decision
            )
        )

        self.decision_text_label.config(
            text=result[
                "decision_text"
            ]
        )

        actions = result.get(
            "actions",
            []
        )

        recommended_action = (
            actions[0]
            if actions
            else "—"
        )

        self.decision_mode_label.config(
            text=(
                f"Рекомендована дія: "
                f"{recommended_action}\n\n"
                f"{result['decision_mode']}"
            )
        )

        # ----------------------------------------------------
        # Human-in-the-loop
        # ----------------------------------------------------

        for button in self.action_buttons:

            button.config(
                state=tk.NORMAL
            )

        self.user_decision_label.config(
            text=(
                "Рішення користувача "
                "ще не зафіксовано."
            ),
            fg=self.MUTED
        )

        # ----------------------------------------------------
        # Explanation
        # ----------------------------------------------------

        self.show_explanation(
            result
        )

        self.status_label.config(
            text=(
                "Аналіз завершено. "
                "Оберіть остаточне рішення користувача."
            )
        )

    # ========================================================
    # ПОЯСНЕННЯ
    # ========================================================

    def show_explanation(
        self,
        result
    ):

        self.info_text.config(
            state=tk.NORMAL
        )

        self.info_text.delete(
            "1.0",
            tk.END
        )

        clean = result.get(
            "clean",
            {}
        )

        # ====================================================
        # ВХІДНІ ДАНІ
        # ====================================================

        self.info_text.insert(
            tk.END,
            "ВХІДНІ ДАНІ ПІСЛЯ ПЕРЕВІРКИ\n",
            "title"
        )

        for column, value in clean.items():

            label = core.FIELD_LABELS.get(
                column,
                self.pretty_name(column)
            )

            if isinstance(
                value,
                float
            ):

                value_text = f"{value:,.2f}"

            else:

                value_text = str(value)

            self.info_text.insert(
                tk.END,
                f"• {label}: {value_text}\n",
                "normal"
            )

        self.info_text.insert(
            tk.END,
            "\n"
        )

        # ====================================================
        # СИСТЕМНЕ ПОЯСНЕННЯ
        # ====================================================

        self.info_text.insert(
            tk.END,
            "СИСТЕМНЕ ПОЯСНЕННЯ\n",
            "title"
        )

        explanation = result.get(
            "explanation",
            {}
        )

        system_lines = explanation.get(
            "system",
            []
        )

        for line in system_lines:

            self.info_text.insert(
                tk.END,
                "• " + str(line) + "\n",
                "normal"
            )

        # ====================================================
        # ОЗНАКИ
        # ====================================================

        factor_lines = explanation.get(
            "factors",
            []
        )

        if factor_lines:

            self.info_text.insert(
                tk.END,
                "\nОЗНАКИ, ВРАХОВАНІ AI-КОМПОНЕНТОМ\n",
                "title"
            )

            for line in factor_lines:

                self.info_text.insert(
                    tk.END,
                    "• " + str(line) + "\n",
                    "normal"
                )

        # ====================================================
        # FINAL
        # ====================================================

        self.info_text.insert(
            tk.END,
            (
                "\nОстаточне рішення приймає "
                "користувач. AI-компонент лише "
                "формує прогноз та рекомендацію "
                "на основі заданих правил."
            ),
            "muted"
        )

        self.info_text.config(
            state=tk.DISABLED
        )

        self.info_text.see(
            "1.0"
        )

    # ========================================================
    # HUMAN-IN-THE-LOOP
    # ========================================================

    def fix_user_decision(
        self,
        code,
        index
    ):

        if self.last_result is None:

            return

        button_text = (
            self.action_buttons[
                index
            ].cget("text")
        )

        try:

            path = core.save_user_decision(
                self.last_result,
                code
            )

        except Exception as error:

            messagebox.showerror(
                "Помилка збереження",
                str(error)
            )

            return

        if code == "ПІДТВЕРДЖЕНО":

            color = self.SUCCESS

        elif code == "МОНІТОРИНГ":

            color = self.WARNING

        else:

            color = self.DANGER

        self.user_decision_label.config(
            text=(
                f"✓ Рішення користувача зафіксовано: "
                f"{button_text}.\n"
                f"AI-рекомендація: "
                f"{self.last_result['decision_title']}.\n"
                f"Запис збережено у: "
                f"{path.name}"
            ),
            fg=color
        )

        self.status_label.config(
            text=(
                "Остаточне рішення користувача "
                "збережено в журналі."
            )
        )

    # ========================================================
    # ПРИКЛАД
    # ========================================================

    def load_example(self):

        # ----------------------------------------------------
        # Категоріальні поля
        # ----------------------------------------------------

        example_values = {

            "brand": "Toyota",

            "model": "Model A",

            "fuel_type": "Petrol",

            "fuel": "Petrol",

            "transmission": "Automatic",

            "seller_type": "Dealer",

            "owner": "First Owner"
        }

        categories = getattr(
            core,
            "CATEGORIES",
            {}
        )

        for column, value in example_values.items():

            if column not in self.input_vars:

                continue

            allowed = categories.get(
                column,
                []
            )

            if not allowed:

                self.input_vars[
                    column
                ].set(value)

            elif value in allowed:

                self.input_vars[
                    column
                ].set(value)

        # ----------------------------------------------------
        # Числові поля
        # ----------------------------------------------------

        defaults = {

            "year": "2018",

            "engine_size": "2.0",

            "engine": "2.0",

            "mileage": "85000",

            "km_driven": "85000",

            "max_power": "120",

            "seats": "5"
        }

        for column, value in defaults.items():

            if column in self.numeric_vars:

                self.numeric_vars[
                    column
                ].set(value)

        # ----------------------------------------------------
        # Поточна ціна
        # ----------------------------------------------------

        self.current_price_var.set(
            "22000"
        )

        self.error_label.config(
            text=""
        )

        self.status_label.config(
            text=(
                "Завантажено приклад даних "
                "вживаного автомобіля."
            )
        )

    # ========================================================
    # ОЧИЩЕННЯ
    # ========================================================

    def clear_output(self):

        self.last_result = None

        # ----------------------------------------------------
        # Результат
        # ----------------------------------------------------

        self.price_label.config(
            text="—"
        )

        self.delta_label.config(
            text="",
            fg=self.MUTED
        )

        self.confidence_label.config(
            text=""
        )

        self.model_label.config(
            text=""
        )

        # ----------------------------------------------------
        # Recommendation
        # ----------------------------------------------------

        self.decision_label.config(
            text="РІШЕННЯ НЕ СФОРМОВАНО",
            fg=self.MUTED
        )

        self.decision_text_label.config(
            text=(
                "Введіть характеристики автомобіля "
                "та виконайте аналіз пропозиції."
            )
        )

        self.decision_mode_label.config(
            text=""
        )

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        for button in self.action_buttons:

            button.config(
                state=tk.DISABLED
            )

        self.user_decision_label.config(
            text=(
                "Рішення користувача "
                "ще не зафіксовано."
            ),
            fg=self.MUTED
        )

        # ----------------------------------------------------
        # Errors
        # ----------------------------------------------------

        self.error_label.config(
            text=""
        )

        # ----------------------------------------------------
        # Explanation
        # ----------------------------------------------------

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
            text="Форму очищено."
        )

    # ========================================================
    # СТАРТОВА ІНФОРМАЦІЯ
    # ========================================================

    def show_startup_info(self):

        if self.ai.is_real_model:

            self.status_label.config(
                text=(
                    f"AI-компонент завантажено: "
                    f"{self.ai.name}."
                )
            )

        else:

            self.status_label.config(
                text=(
                    "Модель Linear Regression "
                    "не знайдена. Перевірте файл "
                    "models/linear_regression.joblib."
                )
            )


# ============================================================
# MAIN
# ============================================================

def main():

    root = tk.Tk()

    DecisionSupportApp(
        root
    )

    root.mainloop()


if __name__ == "__main__":

    main()