

import tkinter as tk
import random


class Plant:
    def __init__(self, name, emoji):
        self.name = name
        self.emoji = emoji

    def get_data(self):
        return {
            "temp": random.randint(10, 35),
            "moisture": random.randint(10, 90),
            "uv": random.randint(0, 100)
        }


def status(value, low, high):
    if value < low:
        return "LOW", "#e74c3c"   # red
    elif value > high:
        return "HIGH", "#e74c3c"  # red
    return "GOOD", "#2ecc71"      # green


#feedback functions
def temp_feedback(value, state):
    if state == "LOW":
        return f"🌡 Temperature too low ({value}°C) — move to warmer area."
    if state == "HIGH":
        return f"🌡 Temperature too high ({value}°C) — move to shade."
    return f"🌡 Temperature is good ({value}°C)."


def moisture_feedback(value, state):
    if state == "LOW":
        return f"💧 Soil too dry ({value}%) — water the plant."
    if state == "HIGH":
        return f"💧 Soil too moist ({value}%) — DO NOT water."
    return f"💧 Soil moisture is good ({value}%)."


def uv_feedback(value, state):
    if state == "LOW":
        return f"☀️ UV too low ({value}) — needs more light."
    if state == "HIGH":
        return f"☀️ UV too high ({value}) — reduce sunlight exposure."
    return f"☀️ UV level is good ({value})."


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("🌱 Smart Plant System")
        self.root.configure(bg="#ecfdf5")
        self.root.geometry("800x450")

        self.plants = [
            Plant("Fern", "🌿"),
            Plant("Cactus", "🌵"),
            Plant("Flower", "🌸"),
            Plant("Bonsai", "🪴")
        ]

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="🌱 Smart Plant Dashboard",
            font=("Arial", 18, "bold"),
            bg="#ecfdf5"
        )
        title.pack(pady=10)

        container = tk.Frame(self.root, bg="#ecfdf5")
        container.pack(fill="both", expand=True)

        #left panel
        left = tk.Frame(container, bg="#d1fae5", width=220)
        left.pack(side="left", fill="y")

        tk.Label(
            left,
            text="My Plants",
            bg="#d1fae5",
            font=("Arial", 14, "bold")
        ).pack(pady=10)

        for plant in self.plants:
            tk.Button(
                left,
                text=f"{plant.emoji} {plant.name}",
                bg="white",
                relief="flat",
                font=("Arial", 12),
                command=lambda p=plant: self.show_plant(p)
            ).pack(pady=6, fill="x", padx=10)

        #rignt panel
        self.right = tk.Frame(container, bg="white")
        self.right.pack(side="right", fill="both", expand=True)

        tk.Label(
            self.right,
            text="Select a plant 🌱",
            font=("Arial", 14),
            bg="white"
        ).pack(pady=40)

    def show_plant(self, plant):
        data = plant.get_data()

        t_s, t_c = status(data["temp"], 18, 26)
        m_s, m_c = status(data["moisture"], 40, 70)
        u_s, u_c = status(data["uv"], 30, 70)

        for widget in self.right.winfo_children():
            widget.destroy()

        #title
        tk.Label(
            self.right,
            text=f"{plant.emoji} {plant.name}",
            font=("Arial", 20, "bold"),
            bg="white"
        ).pack(pady=10)

        #status colors

        tk.Label(
            self.right,
            text=temp_feedback(data["temp"], t_s),
            fg=t_c,
            bg="white",
            font=("Arial", 11),
            wraplength=500,
            justify="left"
        ).pack(pady=6)

        tk.Label(
            self.right,
            text=moisture_feedback(data["moisture"], m_s),
            fg=m_c,
            bg="white",
            font=("Arial", 11),
            wraplength=500,
            justify="left"
        ).pack(pady=6)

        tk.Label(
            self.right,
            text=uv_feedback(data["uv"], u_s),
            fg=u_c,
            bg="white",
            font=("Arial", 11),
            wraplength=500,
            justify="left"
        ).pack(pady=6)


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()