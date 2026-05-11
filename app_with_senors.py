#app_with_senors.py code of gui with real sensor integration using arduino serial communication
import tkinter as tk
import random
from database import get_plant_info
from arduino_serial import ArduinoReader

arduino = ArduinoReader("COM5", 9600)

# =========================================================
# PLANT CLASS
# Stores all information about a single plant
# Includes:
# - identity (name, type, emoji)
# - notes written by user
# - health history (NEW: used for charting over time)
# =========================================================
class Plant:
    def __init__(self, name, plant_type, emoji):
        self.name = name
        self.type = plant_type
        self.emoji = emoji
        self.notes = ""
        self.health_history = []
        self.tick = 0

    def get_data(self):
        # This calls the method in the arduino object we created at the top of the script
        return arduino.get_data()


# =========================================================
# MODEL
# Holds all plant objects in memory
# =========================================================
class PlantModel:
    def __init__(self):
        self.plants = []

    def add(self, plant):
        self.plants.append(plant)

    def remove(self, plant):
        if plant in self.plants:
            self.plants.remove(plant)


# =========================================================
# UI TEXT HELPERS
# Converts raw sensor values into readable text
# =========================================================
def temp_feedback(v):
    fahrenheit = (v * 9/5) + 32
    return f"🌡 Temperature: {round(fahrenheit, 1)}°F"


def moisture_feedback(v):
    readable_moisture = 100 - v  # assuming sensor gives 0 for wet and 100 for dry
    return f"💧 Moisture: {readable_moisture}%"


def uv_feedback(v):
    light_pct = round((v / 1023) * 100)  # convert 0-1023 to 0-100%
    return f"☀️ Light Level: {light_pct}%"


# =========================================================
# HEALTH SCORE SYSTEM
# Converts sensor values into a single 0–100 score
# Used for chart + analytics
# =========================================================
def calculate_health_score(plant, data):
    info = get_plant_info(plant.type)
    if not info:
        return 0

    def score(value, range_tuple):
        low, high = range_tuple

        # completely outside safe range
        if value < low or value > high:
            return 0

        # near edges = warning level
        if abs(value - low) < 3 or abs(value - high) < 3:
            return 60

        # fully healthy range
        return 100

    current_mositure = 100 - data["moisture"]  # convert to 0% = dry, 100% = wet
    current_light = round((data["uv"] / 1023) * 100)  # convert to 0-100%
    current_temp_f = (data["temp"] * 9/5) + 32  # convert to Fahrenheit for scoring

    temp_score = score(current_temp_f, info["temp"])
    moisture_score = score(current_mositure, info["moisture"])
    uv_score = score(current_light, info["uv"])

    return int((temp_score + moisture_score + uv_score) / 3)


# =========================================================
# HEALTH STATUS SYSTEM
# Returns:
# - status label
# - color
# - explanation of what is wrong
# =========================================================
def get_health_status(plant, data):
    info = get_plant_info(plant.type)

    if not info:
        return "Unknown", "gray", "No plant data available"

    readable_moisture = 100 - data["moisture"]  # convert to 0% = dry, 100% = wet
    readable_light = round((data["uv"] / 1023) * 100)  # convert to 0-100%
    current_temp_f = (data["temp"] * 9/5) + 32  # convert to Fahrenheit for checking
    issues = []

    def check(value, range_tuple, name):
        low, high = range_tuple

        if value < low:
            issues.append(f"{name} too low ({value} < {low})")
            return "bad"

        if value > high:
            issues.append(f"{name} too high ({value} > {high})")
            return "bad"

        if abs(value - low) < 3:
            issues.append(f"{name} slightly low")
            return "warn"

        if abs(value - high) < 3:
            issues.append(f"{name} slightly high")
            return "warn"

        return "good"

    results = [
        check(current_temp_f, info["temp"], "Temperature"),
        check(readable_moisture, info["moisture"], "Moisture"),
        check(readable_light, info["uv"], "Light Level")
    ]

    if "bad" in results:
        return "🔴 Needs Attention", "#ef4444", " | ".join(issues)

    if "warn" in results:
        return "🟡 Warning", "#f59e0b", " | ".join(issues)

    return "🟢 Healthy", "#10b981", "All values in safe range"


# =========================================================
# HEALTH CHART (VISUAL ANALYTICS)
# Shows plant health over time using:
# - colored zones (red/yellow/green)
# - line graph
# - axis labels
# =========================================================
class HealthChart:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, height=160, bg="white", highlightthickness=0)
        self.canvas.pack(fill="x", pady=10)

    def draw(self, history, plant):
        from database import get_plant_info

        self.canvas.delete("all")

        if len(history) < 1:
            self.canvas.create_text(250, 80, text="No data yet", fill="gray")
            return

        info = get_plant_info(plant.type)
        if not info:
            return

        width = 500
        height = 120
        max_points = 30

        data = history[-max_points:]

        # axis
        self.canvas.create_text(20, 10, text="100", fill="gray")
        self.canvas.create_text(20, 60, text="50", fill="gray")
        self.canvas.create_text(20, 110, text="0", fill="gray")

        self.canvas.create_line(30, 10, 500, 10, fill="#f3f4f6")
        self.canvas.create_line(30, 60, 500, 60, fill="#f3f4f6")
        self.canvas.create_line(30, 110, 500, 110, fill="#f3f4f6")

        step_x = width / max(len(data), 1)

        def check(value, range_tuple):
            low, high = range_tuple

            if value < low or value > high:
                return "bad"
            if abs(value - low) < 3 or abs(value - high) < 3:
                return "warn"
            return "good"

        for i, item in enumerate(data):
            x = 30 + i * step_x
            score = item["score"]
            y = 120 - (score / 100 * 110)

            d = item.get("data", {})
            # CONVERT TO PERCENTAGES/FAHRENHEIT FOR COLOR LOGIC
            c_temp = (d.get("temp", 0) * 9/5) + 32
            c_moist = 100 - d.get("moisture", 0)
            c_light = round((d.get("uv", 0) / 1023) * 100)

            results = [
                check(c_temp, info["temp"]),
                check(c_moist, info["moisture"]),
                check(c_light, info["uv"])
            ]

            if "bad" in results:
                color = "#ef4444"
            elif "warn" in results:
                color = "#f59e0b"
            else:
                color = "#10b981"

            self.canvas.create_rectangle(
                x - 4, y,
                x + 4, 120,
                fill=color,
                outline=""
            )


# =========================================================
# PLANT CARD (LEFT LIST ITEM)
# Clickable plant selector
# =========================================================
class PlantCard:
    def __init__(self, parent, plant, controller):
        self.plant = plant
        self.controller = controller

        self.frame = tk.Frame(parent, bg="#f9fafb")

        self.label = tk.Label(
            self.frame,
            text=f"{plant.emoji} {plant.name}",
            bg="#f9fafb",
            font=("Arial", 11),
            anchor="w"
        )

        self.label.pack(fill="x", padx=10, pady=8)

        self.frame.bind("<Button-1>", self.click)
        self.label.bind("<Button-1>", self.click)

        self.frame.bind("<Enter>", self.hover)
        self.label.bind("<Enter>", self.hover)

        self.frame.bind("<Leave>", self.leave)
        self.label.bind("<Leave>", self.leave)

        self.frame.pack(fill="x", padx=10, pady=5)

    def click(self, _):
        self.controller.select(self.plant)

    def hover(self, _):
        self.frame.configure(bg="#e0f2fe")
        self.label.configure(bg="#e0f2fe")

    def leave(self, _):
        self.frame.configure(bg="#f9fafb")
        self.label.configure(bg="#f9fafb")


# =========================================================
# MAIN VIEW (UI LAYOUT)
# =========================================================
class PlantView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.root.title("Plant Dashboard")
        self.root.geometry("900x520")
        self.root.configure(bg="#f3f4f6")

        self.current_plant = None

        self.temp_label = None
        self.moisture_label = None
        self.uv_label = None
        self.status_label = None
        self.reason_label = None
        self.notes_box = None
        self.chart = None

        self.build()
        self.render_selected()
        self.auto_refresh()

    def auto_refresh(self):
        self.update_live_data()
        self.root.after(3000, self.auto_refresh)

    def build(self):
        self.container = tk.Frame(self.root, bg="#f3f4f6")
        self.container.pack(fill="both", expand=True, padx=15, pady=15)

        self.left = tk.Frame(self.container, bg="white")
        self.left.pack(side="left", fill="y", padx=(0, 10))

        tk.Label(self.left, text="🌱 My Plants",
                 bg="white", font=("Arial", 16, "bold")).pack(pady=10)

        self.filter_var = tk.StringVar(value="All")

        options = ["All", "Houseplant", "Flowering Plant", "Fruit", "Vegetable"]

        tk.OptionMenu(
            self.left,
            self.filter_var,
            *options,
            command=self.controller.set_filter
        ).pack(fill="x", padx=10, pady=5)

        tk.Button(self.left, text="+ Add Plant",
                  bg="#10b981", fg="white",
                  command=self.controller.open_add_plant).pack(fill="x", padx=10, pady=5)

        tk.Button(self.left, text="Delete Plant",
                  bg="#ef4444", fg="white",
                  command=self.controller.delete_selected).pack(fill="x", padx=10, pady=5)

        self.list_frame = tk.Frame(self.left, bg="white")
        self.list_frame.pack(fill="both", expand=True)

        self.right = tk.Frame(self.container, bg="#f3f4f6")
        self.right.pack(side="right", fill="both", expand=True)

        self.detail = tk.Frame(self.right, bg="white",
                               padx=30, pady=30,
                               bd=2, relief="groove")
        self.detail.pack(fill="both", expand=True, padx=20, pady=20)

        self.refresh()

    def refresh(self):
        for w in self.list_frame.winfo_children():
            w.destroy()

        plants = self.controller.model.plants
        f = self.controller.filter_type

        if f != "All":
            plants = [
                p for p in plants
                if get_plant_info(p.type)
                and get_plant_info(p.type)["category"] == f
            ]

        if not plants:
            tk.Label(self.list_frame, text="No plants yet 🌱",
                     bg="white", fg="#6b7280").pack(pady=20)
        else:
            for plant in plants:
                PlantCard(self.list_frame, plant, self.controller)

    def update_live_data(self):
        if not self.controller.selected:
            return

        plant = self.controller.selected
        data = plant.get_data()

        status, color, reason = get_health_status(plant, data)

        if self.status_label:
            self.status_label.config(text=status, fg=color)

        if self.reason_label:
            self.reason_label.config(text=reason)

        if self.temp_label:
            self.temp_label.config(text=temp_feedback(data["temp"]))

        if self.moisture_label:
            self.moisture_label.config(text=moisture_feedback(data["moisture"]))

        if self.uv_label:
            self.uv_label.config(text=uv_feedback(data["uv"]))

        score = calculate_health_score(plant, data)

        plant.tick += 1
        plant.health_history.append({"time": plant.tick, "score": score, "data": data})

        if len(plant.health_history) > 50:
            plant.health_history.pop(0)

        if self.chart:
            self.chart.draw(plant.health_history, plant)

    def render_selected(self):
        for w in self.detail.winfo_children():
            w.destroy()

        plant = self.controller.selected
        self.current_plant = plant

        if not plant:
            tk.Label(self.detail, text="Select a plant to see information",
                    bg="white", fg="gray", font=("Arial", 14)).pack(pady=50)
            return

        data = plant.get_data()
        info = get_plant_info(plant.type)

        tk.Label(self.detail, text=f"{plant.emoji} {plant.name}",
                 font=("Arial", 26, "bold"),
                 bg="white").pack(pady=10)

        status, color, reason = get_health_status(plant, data)

        self.status_label = tk.Label(self.detail, text=status,
                                     fg=color, bg="white",
                                     font=("Arial", 14, "bold"))
        self.status_label.pack(pady=5)

        self.reason_label = tk.Label(self.detail, text=reason,
                                     bg="white", fg="#6b7280",
                                     wraplength=500)
        self.reason_label.pack(pady=5)

        tk.Frame(self.detail, bg="#e5e7eb", height=2).pack(fill="x", pady=10)

        self.temp_label = tk.Label(self.detail, bg="white")
        self.temp_label.pack()

        self.moisture_label = tk.Label(self.detail, bg="white")
        self.moisture_label.pack()

        self.uv_label = tk.Label(self.detail, bg="white")
        self.uv_label.pack()

        tk.Frame(self.detail, bg="#e5e7eb", height=2).pack(fill="x", pady=10)

        if info:
            tk.Label(self.detail, text="🌿 Care Info",
                     bg="white", font=("Arial", 16, "bold")).pack()

            tk.Label(self.detail, text=info["info"],
                     bg="white", wraplength=600,
                     justify="left").pack(pady=5)

        tk.Label(self.detail, text="📝 Notes",
                 bg="white", font=("Arial", 16, "bold")).pack()

        self.notes_box = tk.Text(self.detail, height=5, width=50)
        self.notes_box.pack()
        self.notes_box.insert("1.0", plant.notes)

        def save_notes():
            plant.notes = self.notes_box.get("1.0", tk.END).strip()

        tk.Button(self.detail, text="Save Notes",
                  bg="#3b82f6", fg="white",
                  command=save_notes).pack(pady=5)

        tk.Label(self.detail, text="📊 Health History",
                 bg="white", font=("Arial", 16, "bold")).pack(pady=(15, 5))

        self.chart = HealthChart(self.detail)


# =========================================================
# CONTROLLER
# =========================================================
class PlantController:
    def __init__(self, root):
        self.model = PlantModel()
        self.selected = None
        self.filter_type = "All"
        self.view = PlantView(root, self)

    def select(self, plant):
        self.selected = plant
        self.view.render_selected()
        self.view.refresh()

    def delete_selected(self):
        if self.selected:
            self.model.remove(self.selected)
            self.selected = None
            self.view.refresh()

    def set_filter(self, value):
        self.filter_type = value
        self.view.refresh()

    def open_add_plant(self):
        win = tk.Toplevel(self.view.root)
        win.title("Add Plant")
        win.geometry("300x200")

        tk.Label(win, text="Plant Name").pack()
        entry = tk.Entry(win)
        entry.pack()

        types = ["Fern", "Cactus", "Rose", "Orchid",
                 "Petunia", "Lavender",
                 "Strawberry", "Blueberry",
                 "Tomato", "Carrot", "Lettuce"]

        selected = tk.StringVar(value=types[0])
        tk.OptionMenu(win, selected, *types).pack()

        def add():
            name = entry.get().strip()
            if not name:
                return

            emoji = {
                "Fern": "🌿", "Cactus": "🌵",
                "Rose": "🌹", "Orchid": "🌸",
                "Petunia": "🌺", "Lavender": "💜",
                "Strawberry": "🍓", "Blueberry": "🫐",
                "Tomato": "🍅", "Carrot": "🥕",
                "Lettuce": "🥬"
            }[selected.get()]

            self.model.add(Plant(name, selected.get(), emoji))
            win.destroy()
            self.view.refresh()

        tk.Button(win, text="Add",
                  bg="#10b981", fg="white",
                  command=add).pack(pady=10)


# =========================================================
# START PROGRAM
# =========================================================
if __name__ == "__main__":
    root = tk.Tk()
    PlantController(root)
    root.mainloop()