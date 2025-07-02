# Shared test data for parametrization
BREEDS_TEST_DATA = [
    ("abys", 5),
    ("aege", 10),
    ("abob", 15),
    ("acur", 20),
    ("asho", 3),
    ("awir", 7),
    ("amau", 9),
    ("amis", 8),
    ("bali", 6),
    ("bamb", 10),
    ("invalid_breed", 5),
    ("abys", "ten"),
    ("abys", 1000),
    ("", 5),
]

IMAGE_FIELDS = ["id", "url", "width", "height", "breeds"]

BREED_FIELDS = [
    "id", "name", "origin", "description", "life_span", "temperament",
    "intelligence", "hypoallergenic", "adaptability", "affection_level",
    "dog_friendly", "energy_level", "shedding_level", "social_needs",
    "vocalisation"
]
