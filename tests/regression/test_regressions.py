import pytest
import requests
from constants import ENDPOINTS
from http import HTTPStatus
import logging
from utils import validate_image_schema
from tests.test_data import BREEDS_TEST_DATA
logger = logging.getLogger(__name__)


@pytest.mark.regression
def test_get_breeds_list(auth_headers):
    """
    Validates that the /breeds endpoint returns a list of breed objects
    and each has a 'name' field.
    """
    logger.info("Requesting list of all breeds")
    response = requests.get(ENDPOINTS["breeds"], headers=auth_headers)
    logger.info(f"Status: {response.status_code} | URL: {response.url}")

    assert response.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK} "
                                                   f"but got {response.status_code}")
    breeds = response.json()
    assert isinstance(breeds, list), "Expected list of breeds"
    assert any("name" in breed for breed in breeds), "No 'name' field in any breed"


@pytest.mark.parametrize("breed_id, limit", BREEDS_TEST_DATA)
@pytest.mark.regression
def test_get_images_for_breed_with_limit(auth_headers, breed_id, limit):
    """
    Sends a request to fetch images for a given breed ID and limit.
    Verifies:
    - If response is 200 for valid inputs
    - If returned list length matches the limit
    - If returned breed matches expected
    - Added checks for negative tests
    """
    logger.info(f"Testing breed_id='{breed_id}' with limit='{limit}'")

    params = {"limit": limit, "breed_ids": breed_id}
    response = requests.get(ENDPOINTS["random_image"], headers=auth_headers, params=params)
    logger.info(f"Status: {response.status_code} | URL: {response.url}")

    if (
        isinstance(limit, int)
        and isinstance(breed_id, str)
        and breed_id
        and breed_id != "invalid_breed"
        and limit <= 20
    ):
        assert response.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK}, "
                                                       f"but got {response.status_code}")

        images = response.json()
        assert isinstance(images, list), "Response is not a list"
        assert len(images) > 0, "Expected at least 1 image"
        assert len(images) <= limit, f"Expected ≤ {limit} images, but got {len(images)}"

        for img in images:
            assert "breeds" in img and img["breeds"], "Image missing breed info"
            assert img["breeds"][0]["id"] == breed_id, \
                f"Expected breed_id '{breed_id}' but got '{img['breeds'][0]['id']}'"

            validate_image_schema(img)
    else:
        assert response.status_code == HTTPStatus.BAD_REQUEST, (f"Expected status code {HTTPStatus.BAD_REQUEST}, "
                                                                f"but got {response.status_code}")

        try:
            images = response.json()
        except ValueError:
            logger.warning(f"Failed to decode JSON response: {response.text}", )
            images = []

        if isinstance(images, list):
            logger.warning(f"Edge case input: got {len(images)} images", )
            assert len(images) <= 100, f"Too many images returned: {len(images)}"


@pytest.mark.regression
def test_get_bengal_images_with_detailed_validation(auth_headers):
    """
    Validates structure and key fields returned for Bengal breed images.
    Checks:
    - Response status
    - Image fields (url, width, height)
    - Breed details (name, origin, intelligence, hypoallergenic, etc.)
    """
    breed_id = "beng"
    params = {"limit": 1, "breed_ids": breed_id}

    response = requests.get(ENDPOINTS["random_image"], headers=auth_headers, params=params)
    logger.info(f"Status: {response.status_code} | URL: {response.url}")

    assert response.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK} "
                                                   f"but got {response.status_code}")
    data = response.json()
    assert isinstance(data, list) and len(data) == 1, f"Expected 1 image, got {len(data)}"

    image = data[0]
    logger.info("Image ID: %s", image.get("id"))

    validate_image_schema(image)
    breed = image.get("breeds", [])[0]

    # here used data get from API, and considered as stable, not changeable data
    assert breed["id"] == "beng", f"Expected breed ID 'beng', got {breed['id']}"
    assert breed["name"] == "Bengal"
    assert breed["origin"] == "United States"
    assert breed["intelligence"] == 5
    assert breed["hypoallergenic"] == 1
    assert "temperament" in breed
    assert "description" in breed
    assert "wikipedia_url" in breed


@pytest.mark.regression
def test_limit_restricted_without_auth():
    """
    Validates that unauthenticated requests to /images/search cannot return more than 10 images,
    even if 'limit=20' is specified.
    """
    limit_requested = 20
    max_expected = 10
    params = {"limit": limit_requested}

    logger.info(f"Sending unauthenticated request with limit={limit_requested}")
    response = requests.get(ENDPOINTS["random_image"], params=params)
    logger.info(f"Status: {response.status_code} | URL: {response.url}")

    assert response.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK} "
                                                   f"but got {response.status_code}")
    data = response.json()
    assert isinstance(data, list), "Expected list in response"
    assert len(data) <= max_expected, (
        f"Expected ≤ {max_expected} images without API key, got {len(data)}"
    )

    logger.info(f"Returned {len(data)} images as expected without API key")


@pytest.mark.regression
def test_unauthorized_access_with_invalid_api_key():
    """
    Smoke Test:
    Sends a request with an invalid API key to verify the server returns 401 Unauthorized
    """
    headers = {
        "x-api-key": "invalid_key_123456"
    }
    params = {"limit": 1}

    logger.info("Sending request with invalid API key to /images/search")
    response = requests.get(ENDPOINTS["random_image"], headers=headers, params=params)
    logger.info(f"Status: {response.status_code} | URL: {response.url}")

    assert response.status_code == HTTPStatus.UNAUTHORIZED, (f"Expected status code {HTTPStatus.UNAUTHORIZED}, "
                                                             f"but got {response.status_code}")
