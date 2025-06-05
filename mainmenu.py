import tkinter as tk
from tkinter import messagebox

class MainMenu(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.main_app = main_app
        self.pack()

        tk.Label(self, text="Main Menu", font=("Arial", 24)).pack(pady=20)

        tk.Button(self, text="Random Battle", width=20, command=self.start_random_battle).pack(pady=5)
        tk.Button(self, text="Story Mode", width=20, command=self.story_mode_placeholder).pack(pady=5)
        tk.Button(self, text="Settings", width=20, command=self.settings_placeholder).pack(pady=5)

    def start_random_battle(self):
        self.pack_forget()
        self.main_app.show_battle()

    def story_mode_placeholder(self):
        messagebox.showinfo("Story Mode", "Story Mode coming soon!")

    def settings_placeholder(self):
        messagebox.showinfo("Settings", "Settings coming soon!")
