#Plant knowledge database.
#Stores ideal environmental conditions for different plant types.


PLANT_DATABASE = {
    "Fern": {
        "temp": (18, 26),
        "moisture": (50, 80),
        "uv": (20, 60),
        "category": "Houseplant",
        "info": "Ferns prefer indirect light, high humidity, and consistently moist soil."
    },
    "Cactus": {
        "temp": (20, 35),
        "moisture": (10, 40),
        "uv": (60, 100),
        "category": "Houseplant",
        "info": "Cactus need bright sunlight and very little water."
    },
    # 🌸 FLOWERING PLANTS
    "Rose": {
        "temp": (15, 26),
        "moisture": (40, 60),
        "uv": (60, 90),
        "category": "Flowering Plant",
        "info": "Roses need plenty of sunlight and moderate watering. Avoid overwatering."
    },
    "Orchid": {
        "temp": (18, 30),
        "moisture": (50, 70),
        "uv": (20, 50),
        "category": "Flowering Plant",
        "info": "Orchids prefer indirect light and careful watering. Do not soak roots."
    },
    "Petunia": {
        "temp": (16, 28),
        "moisture": (40, 60),
        "uv": (60, 90),
        "category": "Flowering Plant",
        "info": "Petunias thrive in full to partial sunlight and need regular watering but well-drained soil."
    },
    "Lavender": {
        "temp": (15, 30),
        "moisture": (20, 40),
        "uv": (70, 100),
        "category": "Flowering Plant",
        "info": "Lavender prefers dry soil and lots of sunlight. Do not overwater."
    },

    # 🍓 FRUITS
    "Strawberry": {
        "temp": (15, 26),
        "moisture": (50, 70),
        "uv": (60, 90),
        "category": "Fruit",
        "info": "Strawberries need full sun and consistent watering but not soggy soil."
    },
    "Blueberry": {
        "temp": (16, 30),
        "moisture": (60, 80),
        "uv": (50, 80),
        "category": "Fruit",
        "info": "Blueberries prefer acidic soil, steady moisture, and plenty of sunlight."
    },
    "Tomato": {
        "temp": (18, 30),
        "moisture": (50, 70),
        "uv": (70, 100),
        "category": "Fruit",
        "info": "Tomatoes need lots of sunlight, warm temperatures, and regular watering."
    },

    # 🥕 VEGETABLES
    "Carrot": {
        "temp": (10, 24),
        "moisture": (40, 70),
        "uv": (50, 80),
        "category": "Vegetable",
        "info": "Carrots grow best in cooler temperatures with loose soil and moderate watering."
    },
    "Lettuce": {
        "temp": (10, 22),
        "moisture": (60, 80),
        "uv": (40, 70),
        "category": "Vegetable",
        "info": "Lettuce prefers cooler weather, partial sunlight, and consistent moisture."
    }
}


def get_plant_types():
    """Return list of available plant types."""
    return list(PLANT_DATABASE.keys())


def get_plant_info(plant_type: str):
    """Return full data for a plant type."""
    return PLANT_DATABASE.get(plant_type)


def get_ranges(plant_type: str):
    """Return temp, moisture, uv ranges."""
    plant = get_plant_info(plant_type)
    if not plant:
        return None

    return plant["temp"], plant["moisture"], plant["uv"]