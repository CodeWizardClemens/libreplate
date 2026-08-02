from typing import Callable, Optional, TypeAlias

import pytest
from body_metrics.services import sync_default_body_metrics
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser
from nutrients.services import sync_default_nutrients
from rest_framework.test import APIClient
from units.services import sync_default_units

User = get_user_model()

UserFactory: TypeAlias = Callable[[Optional[str]], AbstractBaseUser]
AuthenticatedClient: TypeAlias = tuple[APIClient, AbstractBaseUser]


@pytest.fixture
def setup_default_data(db) -> None:
    sync_default_units()
    sync_default_nutrients()
    sync_default_body_metrics()


@pytest.fixture
def create_user(db) -> UserFactory:
    """
    Returns a factory function for creating test users.

    Usage:
        user = create_user(username="alice")

    Multiple users can be created by calling the factory repeatedly:
        user1 = create_user()
        user2 = create_user(username="bob")
    """
    User = get_user_model()

    def factory(username: Optional[str] = None) -> AbstractBaseUser:
        username = username or f"testuser_{User.objects.count() + 1}"

        return User.objects.create_user(
            username=username,
            email=f"{username}@example.com",
            password="password123",
        )

    return factory


@pytest.fixture
def authenticated_client(create_user: UserFactory) -> AuthenticatedClient:
    user = create_user(username="food_test_user")

    client = APIClient()
    client.force_authenticate(user=user)

    return client, user
