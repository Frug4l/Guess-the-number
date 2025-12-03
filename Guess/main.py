import tkinter as tk
import random

class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай число")
        self.root.geometry("500x400")
        
        # Переменные игры
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        
    def create_menu(self):
        """Создание меню приложения"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новая игра", command=self.restart_game)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Настройки", menu=settings_menu)
        settings_menu.add_command(
            label="Изменить размер окна", 
            command=self.resize_window  
        )
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Правила", command=self.show_rules)
        help_menu.add_command(label="О программе", command=self.show_about)
        
    def create_widgets(self):
        """Создание основных виджетов игры"""
        # Основной фрейм
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = tk.Label(
            main_frame, 
            text="Угадай число от 1 до 100", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Описание
        self.description_label = tk.Label(
            main_frame,
            text="Я загадал число от 1 до 100. Попробуй угадать!",
            font=("Arial", 12)
        )
        self.description_label.pack(pady=5)
        
        # Счетчик попыток
        self.counter_label = tk.Label(
            main_frame,
            text="Попытки: 0",
            font=("Arial", 12)
        )
        self.counter_label.pack(pady=5)
        
        # Поле для ввода
        input_frame = tk.Frame(main_frame)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Ваше число:").pack(side=tk.LEFT, padx=5)
        
        self.entry = tk.Entry(input_frame, width=15)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.check_guess())
        
        # Кнопка проверки
        self.check_button = tk.Button(
            main_frame,
            text="Проверить",
            command=self.check_guess,
            width=15
        )
        self.check_button.pack(pady=10)
        
        # Текстовое поле для результата
        self.result_text = tk.Text(main_frame, height=10, width=50, state=tk.DISABLED)
        self.result_text.pack(pady=10)
        
    def create_widgets(self):
        main_frame = tk.Frame(self.root, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = tk.Label(
            main_frame, 
            text="Угадай число от 1 до 100", 
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=10)
        
        # Описание
        self.description_label = tk.Label(
            main_frame,
            text="Я загадал число от 1 до 100. Попробуй угадать!",
            font=("Arial", 12)
        )
        self.description_label.pack(pady=5)
        
        # Счетчик попыток
        self.counter_label = tk.Label(
            main_frame,
            text="Попытки: 0",
            font=("Arial", 12)
        )
        self.counter_label.pack(pady=5)
        
        # Поле для ввода
        input_frame = tk.Frame(main_frame)
        input_frame.pack(pady=10)
        
        tk.Label(input_frame, text="Ваше число:").pack(side=tk.LEFT, padx=5)
        
        self.entry = tk.Entry(input_frame, width=15)
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.check_guess())
        
        # Кнопка проверки
        self.check_button = tk.Button(
            main_frame,
            text="Проверить",
            command=self.check_guess,
            width=15
        )
        self.check_button.pack(pady=10)
        
        # Текстовое поле для результата
        self.result_text = tk.Text(main_frame, height=10, width=50, state=tk.DISABLED)
        self.result_text.pack(pady=10)
        
    def check_guess(self):
        try:
            # Получаем ввод
            guess_text = self.entry.get().strip()
            
            # Проверка на пустой ввод
            if not guess_text:
                raise ValueError("Пустой ввод")
            
            guess = int(guess_text)
            if guess < 1 or guess > 100:
                raise ValueError("Число вне диапазона 1-100")
            
            self.attempts += 1
            self.counter_label.config(text="Попытки: " + str(self.attempts))
            self.result_text.config(state=tk.NORMAL)

