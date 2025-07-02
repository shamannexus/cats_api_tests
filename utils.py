from tests.test_data import IMAGE_FIELDS, BREED_FIELDS


def validate_image_schema(image: dict):
    """
    Validates the structure of an image object
    Ensures:
    - Top-level image fields are present
    - At least one breed is included
    - Breed-level fields are present
    """
    for field in IMAGE_FIELDS:
        assert field in image, f"Missing image field: {field}"

    assert isinstance(image["breeds"], list) and image["breeds"], "Missing or empty 'breeds'"
    breed = image["breeds"][0]

    for field in BREED_FIELDS:
        assert field in breed, f"Missing breed field: {field}"


def get_first_breed_id(breeds_list):
    """
    Extracts the ID of the first breed from the list of breeds.
    """
    if not breeds_list:
        raise ValueError("Breed list is empty.")
    return breeds_list[0]["id"]
