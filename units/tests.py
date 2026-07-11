from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from units.models import Unit, UnitScope

User = get_user_model()


class UnitScopeModelTests(TestCase):

    def test_only_one_global_scope_can_exist(self):
        # Created by the data migration.
        self.assertEqual(UnitScope.objects.filter(user=None).count(), 1)

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
        self.scope = UnitScope.objects.get(user=None)

    def test_default_units_are_created_by_migration(self):
        self.assertTrue(
            Unit.objects.filter(scope=self.scope, name="Gram").exists()
        )
        self.assertTrue(
            Unit.objects.filter(scope=self.scope, name="Mililiter").exists()
        )

    def test_unit_names_must_be_unique_within_scope(self):
        with self.assertRaises(ValidationError):
            Unit.objects.create(
                scope=self.scope,
                name="Gram", # Already created by the migration.
            )

    def test_user_cannot_create_unit_with_same_name_as_global_unit(self):
        user = User.objects.create_user(
            username="other-user",
            password="password",
        )
        user_scope = UnitScope.objects.create(user=user)

        with self.assertRaises(ValidationError):
            Unit.objects.create(
                scope=user_scope,
                name="Gram", # Already exists in the global scope.
            )

    # TODO There should be some logic for when a global unit is created, and a user
    # has already defined one.

    # TODO Units should be hidden from a selecting menu for the user. So the user
    # doesn't get floated with a large amount of global units.