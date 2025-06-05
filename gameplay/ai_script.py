import json
import os

class AIScript:
    def __init__(self, filename="ai_profile.json"):
        self.rules = []
        self.name = "DefaultAI"
        if os.path.exists(filename):
            try:
                with open(filename, "r") as f:
                    data = json.load(f)
                    self.name = data.get("name", "CustomAI")
                    self.rules = data.get("rules", [])
            except Exception as e:
                print(f"Failed to load AI script: {e}")
        else:
            print("AI script file not found. Using default behavior.")
