import pytest
import logging
from config import BASE_URL, HEADERS


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)


@pytest.fixture(scope="session")
def auth_headers():
    return HEADERS


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL
