import tkinter as tk
from tkinter import messagebox, simpledialog
from tkinter import Scrollbar
import random


class GuessNumberGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Угадай число")
        self.root.geometry("600x500")
        self.root.minsize(550, 450)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
        # Переменные игры
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.hint_used = False
        
        # Создание интерфейса
        self.create_widgets()
        self.create_menu()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Новая игра", command=self.restart_game)
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.root.quit)


        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Настройки", menu=settings_menu)
        settings_menu.add_command(
            label="Изменить размер окна",
            command=self.resize_window  # обязательная функциональность
        )

        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Правила", command=self.show_rules)
        help_menu.add_command(label="О программе", command=self.show_about)

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
        input_frame.pack(pady=15)

        tk.Label(input_frame, text="Ваше число:", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        
        self.entry = tk.Entry(input_frame, width=20, font=("Arial", 11), justify='center')
        self.entry.pack(side=tk.LEFT, padx=5)
        self.entry.bind("<Return>", lambda event: self.check_guess())

        tk.Label(main_frame, text="История попыток:", font=("Arial", 11)).pack(anchor='w', pady=(0, 5))

        # Кнопка проверки
        self.check_button = tk.Button(
            main_frame,
            text="Проверить",
            command=self.check_guess,
            width=15
        )
        self.check_button.pack(pady=10)

        # Кнопка подсказки
        self.hint_button = tk.Button(
            main_frame,
            text="Подсказка",
            command=self.give_hint,  # ← Новый метод
            width=15
        )
        self.hint_button.pack(pady=5)
        
        # Фрейм для текстового поля и метки
        result_frame = tk.Frame(main_frame)
        result_frame.pack(fill=tk.BOTH, expand=True)

        # Текстовое поле для результата
        self.result_text = tk.Text(
            result_frame, 
            height=12,  
            width=60,  
            state=tk.DISABLED,
            font=("Arial", 10),  
            bg="#F8F9F9",        
            relief=tk.SUNKEN     
        )

        # Полоса прокрутки
        scrollbar = tk.Scrollbar(result_frame, command=self.result_text.yview)
        self.result_text.config(yscrollcommand=scrollbar.set)
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def check_guess(self):
        try:
            guess_text = self.entry.get().strip()

            # Проверка на пустой ввод
            if not guess_text:
                raise ValueError("Пустой ввод")

            # Преобразуем в число
            guess = int(guess_text)

            # Проверка диапазона
            if guess < 1 or guess > 100:
                raise ValueError("Число вне диапазона 1-100")

            # Основная логика игры
            self.attempts += 1
            self.counter_label.config(text="Попытки: " + str(self.attempts))

            # Включаем текстовое поле для записи
            self.result_text.config(state=tk.NORMAL)

            if guess < self.secret_number:
                self.result_text.insert(tk.END, str(guess) + " — Загаданное число больше\n")
            elif guess > self.secret_number:
                self.result_text.insert(tk.END, str(guess) + " — Загаданное число меньше\n")
            else:
                self.result_text.insert(tk.END, "🎉 Ура! Вы угадали число " + str(self.secret_number) +
                                        " за " + str(self.attempts) + " попыток!\n")
                self.check_button.config(state=tk.DISABLED)
                self.entry.config(state=tk.DISABLED)

            # Отключаем редактирование
            self.result_text.config(state=tk.DISABLED)

            self.result_text.see(tk.END)

            self.entry.delete(0, tk.END)

        except ValueError as e:
            if "Пустой ввод" in str(e):
                messagebox.showwarning("Ошибка", "Пожалуйста, введите число")
            elif "Число вне диапазона" in str(e):
                messagebox.showwarning("Ошибка", "Число должно быть от 1 до 100")
            else:
                messagebox.showerror("Ошибка", "Пожалуйста, введите целое число")
            self.entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Ошибка", "Произошла ошибка: " + str(e))

    def give_hint(self):
        """Дать подсказку игроку"""
        if not self.hint_used:
            if self.secret_number % 2 == 0:
                hint_text = "Число четное"
            else:
                hint_text = "Число нечетное"
        
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"Подсказка: {hint_text}\n")
            self.result_text.config(state=tk.DISABLED)
            self.result_text.see(tk.END)
        
            self.hint_used = True
            self.hint_button.config(state=tk.DISABLED)
        else:
            messagebox.showinfo("Подсказка", "Подсказка уже использована!")
    
    def restart_game(self):
        self.secret_number = random.randint(1, 100)
        self.attempts = 0
        self.counter_label.config(text="Попытки: 0")

        self.hint_used = False
        self.hint_button.config(state=tk.NORMAL)
    
        # Очищаем поле результатов
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Начата новая игра! Угадайте число от 1 до 100\n")
        self.result_text.config(state=tk.DISABLED)

        # Активируем элементы
        self.check_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.NORMAL)
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def resize_window(self):
        try:
            # Диалог для изменения ширины
            width = simpledialog.askinteger(
                "Ширина окна",
                "Введите ширину окна (400-1200):",
                parent=self.root,
                initialvalue=self.root.winfo_width(),
                minvalue=400,
                maxvalue=1200
            )

            # Диалог для изменения высоты
            height = simpledialog.askinteger(
                "Высота окна",
                "Введите высоту окна (300-800):",
                initialvalue=self.root.winfo_height(),
                minvalue=300,
                maxvalue=800
            )

            # Применяем новые размеры
            if width and height:
                self.root.geometry(str(width) + "x" + str(height))

        except Exception as e:
            messagebox.showerror("Ошибка", "Не удалось изменить размер окна: " + str(e))

    def show_rules(self):
        rules_text = """Правила игры "Угадай число"

    1. Компьютер загадывает число от 1 до 100
    2. Вы пытаетесь угадать это число
    3. После каждой попытки вы получаете подсказку:
       - "Загаданное число больше"
       - "Загаданное число меньше"
    4. Можно один раз за игру использовать подсказку
    5. Цель: угадать число за минимальное количество попыток

    Удачи в игре!"""

        rules_window = tk.Toplevel(self.root)
        rules_window.title("Правила игры")
        rules_window.geometry("600x500")
        rules_window.resizable(False, False)

        rules_window.transient(self.root)
        rules_window.grab_set()

        # Центрирование относительно главного окна
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        rules_window.geometry(f"600x500+{x}+{y}")

        # Содержимое окна
        text_frame = tk.Frame(rules_window, padx=20, pady=20)
        text_frame.pack(fill=tk.BOTH, expand=True)

        # Используем Text вместо Label для лучшего форматирования
        rules_widget = tk.Text(
            text_frame,
            font=("Arial", 11),
            wrap=tk.WORD,
            height=12,
            width=50,
            bg=rules_window.cget("bg"),
            relief=tk.FLAT,
            bd=0
        )
        rules_widget.pack(fill=tk.BOTH, expand=True)

        # Вставляем текст правил
        rules_widget.insert(tk.END, rules_text)
        rules_widget.config(state=tk.DISABLED)  # Делаем только для чтения

        close_button = tk.Button(
            rules_window,
            text="Понятно",
            command=rules_window.destroy,
            width=15
        )
        close_button.pack(pady=20)

        rules_window.focus_set()

    def show_about(self):
        about_text = """Игра "Угадай число"

    Лабораторная работа по программированию

    Выполненные требования:
    - Меню приложения
    - Настройка размеров окна
    - Обработка исключений
    - Система подсказок

    Все исключения обрабатываются, 
    программа не завершается при ошибках."""

        about_window = tk.Toplevel(self.root)
        about_window.title("О программе")
        about_window.geometry("600x500")
        about_window.resizable(False, False)

        about_window.transient(self.root)
        about_window.grab_set()

        # Центрирование относительно главного окна
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 300
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 250
        about_window.geometry(f"600x500+{x}+{y}")

        # Содержимое окна
        text_frame = tk.Frame(about_window, padx=20, pady=20)
        text_frame.pack(fill=tk.BOTH, expand=True)

        text_label = tk.Label(
            text_frame,
            text=about_text,
            font=("Arial", 11),
            justify=tk.LEFT
        )
        text_label.pack()

        close_button = tk.Button(
            about_window,
            text="Закрыть",
            command=about_window.destroy,
            width=15
        )
        close_button.pack(pady=20)

        about_window.focus_set()



if __name__ == "__main__":
    root = tk.Tk()
    game = GuessNumberGame(root)


    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(str(width) + 'x' + str(height) + '+' + str(x) + '+' + str(y))


    game.entry.focus()

    root.mainloop()







