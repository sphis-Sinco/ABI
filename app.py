import tkinter as tk
from mainmenu import MainMenu
from gameplay import BattleGame

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("A.I. Battle Interface")
        self.geometry("650x400")

        self.main_menu = MainMenu(self, self)
        self.battle_game = None

    def show_battle(self):
        self.main_menu.pack_forget()
        if self.battle_game:
            self.battle_game.destroy()
        self.battle_game = BattleGame(self, self)
        self.battle_game.pack()

    def show_main_menu(self):
        if self.battle_game:
            self.battle_game.destroy()
            self.battle_game = None
        self.main_menu.pack()

if __name__ == "__main__":
    app = Application()
    app.mainloop()
