import tkinter as tk
import random
from .ai_script import AIScript
from .moves import Move

class BattleGame(tk.Frame):
    def __init__(self, master, main_app):
        super().__init__(master)
        self.main_app = main_app
        self.pack()
        self.setup_game()
        self.ai_script = AIScript()

    def setup_game(self):
        self.player_health = 100
        self.ai_health = 100
        self.player_energy = 5
        self.ai_energy = 5
        self.max_energy = 10
        self.turn = "player"

        self.player_moves = [
            Move("Quick Attack", 15, 2),
            Move("Power Strike", 30, 5),
            Move("Heal", -20, 3),
            Move("Recharge", 0, 0),
        ]

        self.ai_moves = [
            Move("Claw Swipe", 12, 2),
            Move("Heavy Slam", 28, 5),
            Move("Regenerate", -15, 3),
            Move("Recharge", 0, 0),
        ]

        self.health_label = tk.Label(self, text="")
        self.health_label.pack()

        self.ai_label = tk.Label(self, text="")
        self.ai_label.pack()

        self.buttons_frame = tk.Frame(self)
        self.buttons_frame.pack(pady=5)

        self.move_buttons = []
        for move in self.player_moves:
            btn = tk.Button(self.buttons_frame, text=f"{move.name} (Cost: {move.energy_cost})",
                            command=lambda m=move: self.player_move(m))
            btn.pack(side=tk.LEFT, padx=5)
            self.move_buttons.append(btn)

        self.log_box = tk.Text(self, height=12, width=60, state='disabled')
        self.log_box.pack(pady=10)

        self.update_labels()
        self.log("Battle started! Choose your move.")

    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.config(state='disabled')
        self.log_box.see(tk.END)

    def update_labels(self):
        self.health_label.config(text=f"Your Health: {max(self.player_health,0)} | Energy: {self.player_energy}/{self.max_energy}")
        self.ai_label.config(text=f"A.I. Health: {max(self.ai_health,0)} | Energy: {self.ai_energy}/{self.max_energy}")

    def disable_buttons(self):
        for btn in self.move_buttons:
            btn.config(state='disabled')

    def enable_buttons(self):
        for btn in self.move_buttons:
            btn.config(state='normal')

    def player_move(self, move):
        if move.energy_cost > self.player_energy:
            self.log(f"Not enough energy for {move.name}!")
            return

        self.apply_move("player", move)
        self.turn = "ai"
        self.end_turn()

    def apply_move(self, user, move):
        if user == "player":
            energy = self.player_energy
            health = self.player_health
            target_health = self.ai_health
        else:
            energy = self.ai_energy
            health = self.ai_health
            target_health = self.player_health

        if move.name.lower() == "recharge":
            if user == "player":
                self.player_energy = min(self.max_energy, self.player_energy + 3)
                self.log(f"You used Recharge and restored 3 energy.")
            else:
                self.ai_energy = min(self.max_energy, self.ai_energy + 3)
                self.log(f"A.I. used Recharge and restored 3 energy.")
            return

        if user == "player":
            self.player_energy -= move.energy_cost
        else:
            self.ai_energy -= move.energy_cost

        if move.damage < 0:
            heal_amount = -move.damage
            if user == "player":
                self.player_health = min(100, self.player_health + heal_amount)
                self.log(f"You used {move.name} and healed {heal_amount} HP.")
            else:
                self.ai_health = min(100, self.ai_health + heal_amount)
                self.log(f"A.I. used {move.name} and healed {heal_amount} HP.")
        else:
            if user == "player":
                self.ai_health -= move.damage
                self.log(f"You used {move.name} and dealt {move.damage} damage!")
            else:
                self.player_health -= move.damage
                self.log(f"A.I. used {move.name} and dealt {move.damage} damage!")

        self.player_health = max(0, self.player_health)
        self.ai_health = max(0, self.ai_health)

    def end_turn(self):
        self.update_labels()
        if self.player_health <= 0:
            self.log("You have been defeated by the A.I.!")
            self.disable_buttons()
            return
        if self.ai_health <= 0:
            self.log("You defeated the A.I.! Victory is yours!")
            self.disable_buttons()
            return

        self.enable_buttons()
        self.root_after_id = self.after(1000, self.ai_turn)

    def ai_turn(self):
        self.disable_buttons()
        action = self.ai_decide()
        move = next((m for m in self.ai_moves if m.name.lower() == action.lower()), None)
        if move is None:
            move = random.choice(self.ai_moves)

        if move.energy_cost > self.ai_energy:
            recharge_move = next((m for m in self.ai_moves if m.name.lower() == "recharge"), None)
            if recharge_move:
                move = recharge_move
            else:
                affordable_moves = [m for m in self.ai_moves if m.energy_cost <= self.ai_energy]
                if affordable_moves:
                    move = random.choice(affordable_moves)

        self.apply_move("ai", move)
        self.turn = "player"
        self.update_labels()
        if self.player_health <= 0 or self.ai_health <= 0:
            self.end_turn()
        else:
            self.log("Your move.")
            self.enable_buttons()

    def ai_decide(self):
        context = {
            "self_health": self.ai_health,
            "self_energy": self.ai_energy,
            "opponent_health": self.player_health,
            "opponent_energy": self.player_energy,
        }

        for rule in self.ai_script.rules:
            try:
                if eval(rule["condition"], {}, context):
                    return rule["action"]
            except Exception as e:
                print(f"Error in AI condition: {rule['condition']} -> {e}")
                continue

        return "Claw Swipe"
