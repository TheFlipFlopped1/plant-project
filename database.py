#Plant knowledge database. Stores ideal environmental conditions for different plant types.


PLANT_DATABASE = {
    "Fern": {
        "temp": (64, 79),
        "moisture": (50, 80),
        "uv": (20, 60),
        "category": "Houseplant",
        "info": "Ferns prefer indirect light, high humidity, and consistently moist soil."
    },
    "Cactus": {
        "temp": (68, 95),
        "moisture": (10, 40),
        "uv": (60, 100),
        "category": "Houseplant",
        "info": "Cactus need bright sunlight and very little water."
    },
    "Rose": {
        "temp": (59, 79),
        "moisture": (40, 60),
        "uv": (60, 90),
        "category": "Flowering Plant",
        "info": "Roses need plenty of sunlight and moderate watering."
    },
    "Orchid": {
        "temp": (64, 86),
        "moisture": (50, 70),
        "uv": (20, 50),
        "category": "Flowering Plant",
        "info": "Orchids prefer indirect light and careful watering."
    },
    "Petunia": {
        "temp": (60, 82), 
        "moisture": (40, 60),
        "uv": (60, 90),
        "category": "Flowering Plant",
        "info": "Petunias thrive in full to partial sunlight."
    },
    "Lavender": {
        "temp": (59, 86), 
        "moisture": (20, 40),
        "uv": (70, 100),
        "category": "Flowering Plant",
        "info": "Lavender prefers dry soil and lots of sunlight."
    },
    "Strawberry": {
        "temp": (59, 79), 
        "moisture": (50, 70),
        "uv": (60, 90),
        "category": "Fruit",
        "info": "Strawberries need full sun and consistent watering."
    },
    "Blueberry": {
        "temp": (60, 86), 
        "moisture": (60, 80),
        "uv": (50, 80),
        "category": "Fruit",
        "info": "Blueberries prefer acidic soil and steady moisture."
    },
    "Tomato": {
        "temp": (64, 86), 
        "moisture": (50, 70),
        "uv": (70, 100),
        "category": "Fruit",
        "info": "Tomatoes need lots of sunlight and warm temperatures."
    },
    "Carrot": {
        "temp": (50, 75), 
        "moisture": (40, 70),
        "uv": (50, 80),
        "category": "Vegetable",
        "info": "Carrots grow best in cooler temperatures."
    },
    "Lettuce": {
        "temp": (50, 72), 
        "moisture": (60, 80),
        "uv": (40, 70),
        "category": "Vegetable",
        "info": "Lettuce prefers cooler weather and partial sunlight."
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