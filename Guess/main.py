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
