import pytest
import requests
from constants import ENDPOINTS
from utils import get_first_breed_id
from http import HTTPStatus
import logging

logger = logging.getLogger(__name__)


@pytest.mark.e2e
def test_get_random_image_for_breed(auth_headers):
    """
    E2E Test:
    - Retrieves breed list
    - Selects the first breed
    - Fetches a random image for that breed
    - Validates that the breed info in the image matches the one requested
    """
    logger.info("Requesting list of all breeds")
    breed_resp = requests.get(ENDPOINTS["breeds"], headers=auth_headers)
    logger.info(f"Breeds response status: {breed_resp.status_code}", )
    assert breed_resp.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK} "
                                                     f"but got {breed_resp.status_code}")

    breeds = breed_resp.json()
    logger.info(f"Number of breeds retrieved:{len(breeds)}" )
    breed_id = get_first_breed_id(breeds)
    logger.info(f"Selected first breed id: {breed_id}")

    logger.info(f"Requesting random image for breed '{breed_id}'")
    image_resp = requests.get(f"{ENDPOINTS['random_image']}?breed_ids={breed_id}", headers=auth_headers)
    logger.info(f"Image response status: {image_resp.status_code} | URL:{image_resp.url}")
    assert image_resp.status_code == HTTPStatus.OK, (f"Expected status code {HTTPStatus.OK} "
                                                     f"but got {image_resp.status_code}")

    data = image_resp.json()
    assert data, "Response data is empty"
    assert "breeds" in data[0], "No breed info in the first image"
    assert data[0]["breeds"][0]["id"] == breed_id, (
        f"Expected breed id '{breed_id}', but got '{data[0]['breeds'][0]['id']}'"
    )
    logger.info("Breed ID in image matches requested breed ID")
