import pytest
import requests
import logging
from http import HTTPStatus
from constants import ENDPOINTS
from utils import validate_image_schema

logger = logging.getLogger(__name__)


@pytest.mark.smoke
def test_get_random_image(auth_headers):
    """
    Smoke Test:
    Validates that a basic /images/search call returns a valid image.
    - Status code 200
    - Response is a non-empty list
    - First item has a valid 'url'
    """
    logger.info("Requesting random image with authentication")
    response = requests.get(ENDPOINTS["random_image"], headers=auth_headers)
    logger.info(f"Status: {response.status_code} | URL: {response.url}")

    assert response.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK} "
                                                   f"but got {response.status_code}")
    data = response.json()
    assert isinstance(data, list) and len(data) > 0, "Expected non-empty list of images"

    first_image = data[0]
    assert "url" in first_image and first_image["url"].startswith("http"), "Missing or invalid 'url' in image"

    logger.info(f"Random image retrieved successfully: {first_image['url']}")


@pytest.mark.smoke
def test_breed_image_schema(auth_headers):
    """
    Smoke Test:
    Validates the structure of breed image responses:
    - Image-level schema
    - Nested breed object fields
    """
    breed_id = "beng"
    params = {"breed_ids": breed_id, "limit": 5}

    logger.info(f"Requesting images for breed_id='{breed_id}'")
    response = requests.get(ENDPOINTS["random_image"], headers=auth_headers, params=params)
    logger.info(f"Status: {response.status_code} | URL: {response.url}")

    assert response.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK} "
                                                   f"but got {response.status_code}")
    images = response.json()
    assert isinstance(images, list) and len(images) > 0, "No images returned for the breed"

    for img in images:
        validate_image_schema(img)

    logger.info(f"Schema validation passed for {len(images)} images")

