# habits/tests/conftest.py
import os
import django
import pytest
from django.conf import settings


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

    if not settings.configured:
        django.setup()


@pytest.fixture(autouse=True)
def enable_db_access_for_all_tests(db):
    """Даем доступ к БД всем тестам"""
    pass