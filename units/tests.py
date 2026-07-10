from datetime import timedelta
from uuid import UUID

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.test import TestCase
from django.utils import timezone

from your_app.models import Unit, UnitScope


User = get_user_model()


class UnitScopeModelTests(TestCase):

    def test_only_one_global_scope_can_exist(self):
        UnitScope.objects.create()
        with self.assertRaises(IntegrityError):
            UnitScope.objects.create()

    def test_user_can_have_only_one_scope(self):
        user = User.objects.create_user(
            username="test-user",
            password="password",
        )

        UnitScope.objects.create(user=user)
        with self.assertRaises(IntegrityError):
            UnitScope.objects.create(user=user)


class UnitModelTests(TestCase):
    def setUp(self):
        self.scope = UnitScope.objects.create()

    def test_unit_names_must_be_unique_within_scope(self):
        Unit.objects.create(
            scope=self.scope,
            name="Meter",
        )

        with self.assertRaises(IntegrityError):
            Unit.objects.create(
                scope=self.scope,
                name="Meter",
            )

    def test_same_unit_name_allowed_in_different_scopes(self):
        other_scope = UnitScope.objects.create()

        first = Unit.objects.create(
            scope=self.scope,
            name="Meter",
        )

        second = Unit.objects.create(
            scope=other_scope,
            name="Meter",
        )

        self.assertEqual(first.name, second.name)
        self.assertNotEqual(first.scope, second.scope)
