import tkinter as tk
import random

class BattleGame:
    def __init__(self, root):
        self.root = root
        self.root.title("A.I. Battle Interface")
        self.setup_game()

    def setup_game(self):
        # Player & AI stats
        self.player_health = 100
        self.ai_health = 100
        self.player_energy = 3
        self.ai_energy = 3
        self.turn = "player"

        # Labels
        self.health_label = tk.Label(self.root, text=f"Your Health: {self.player_health} | Energy: {self.player_energy}")
        self.health_label.pack()

        self.ai_label = tk.Label(self.root, text=f"A.I. Health: {self.ai_health} | Energy: {self.ai_energy}")
        self.ai_label.pack()

        # Buttons
        self.attack_button = tk.Button(self.root, text="Attack (-1 energy)", command=self.player_attack)
        self.attack_button.pack(pady=2)

        self.defend_button = tk.Button(self.root, text="Defend", command=self.player_defend)
        self.defend_button.pack(pady=2)

        self.recharge_button = tk.Button(self.root, text="Recharge (+1 energy)", command=self.player_recharge)
        self.recharge_button.pack(pady=2)

        # Log box
        self.log_box = tk.Text(self.root, height=10, width=50, state='disabled')
        self.log_box.pack(pady=10)

        self.log("Game started! Your move.")

    def log(self, message):
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.config(state='disabled')
        self.log_box.see(tk.END)

    def update_labels(self):
        self.health_label.config(text=f"Your Health: {self.player_health} | Energy: {self.player_energy}")
        self.ai_label.config(text=f"A.I. Health: {self.ai_health} | Energy: {self.ai_energy}")

    def end_turn(self):
        self.update_labels()
        if self.player_health <= 0:
            self.log("You have been defeated by the A.I.")
            self.disable_buttons()
            return
        if self.ai_health <= 0:
            self.log("You defeated the A.I.! Victory is yours.")
            self.disable_buttons()
            return

        self.root.after(1000, self.ai_turn)

    def disable_buttons(self):
        self.attack_button.config(state='disabled')
        self.defend_button.config(state='disabled')
        self.recharge_button.config(state='disabled')

    def player_attack(self):
        if self.player_energy <= 0:
            self.log("Not enough energy to attack!")
            return
        damage = random.randint(10, 20)
        self.ai_health -= damage
        self.player_energy -= 1
        self.log(f"You attacked the A.I. for {damage} damage.")
        self.turn = "ai"
        self.end_turn()

    def player_defend(self):
        self.log("You prepare to defend.")
        self.player_energy += 1  # Defending gives energy passively
        self.turn = "ai"
        self.end_turn()

    def player_recharge(self):
        self.player_energy += 1
        self.log("You recharged 1 energy.")
        self.turn = "ai"
        self.end_turn()

    def ai_turn(self):
        if self.ai_health <= 0:
            return

        action = self.ai_decide()
        if action == "attack" and self.ai_energy > 0:
            damage = random.randint(10, 20)
            self.player_health -= damage
            self.ai_energy -= 1
            self.log(f"A.I. attacked you for {damage} damage.")
        elif action == "defend":
            self.log("A.I. defended and gained 1 energy.")
            self.ai_energy += 1
        elif action == "recharge":
            self.ai_energy += 1
            self.log("A.I. recharged 1 energy.")
        else:
            self.log("A.I. hesitated.")

        self.turn = "player"
        self.update_labels()
        self.log("Your move.")

    def ai_decide(self):
        if self.ai_energy >= 1 and self.player_health <= 30:
            return "attack"
        if self.ai_energy == 0:
            return "recharge"
        if self.ai_health <= 30:
            return random.choice(["defend", "recharge"])
        return random.choice(["attack", "defend", "recharge"])

# Start the game
if __name__ == "__main__":
    root = tk.Tk()
    game = BattleGame(root)
    root.mainloop()
