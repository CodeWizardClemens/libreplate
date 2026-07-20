from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from units.models import HiddenUnit, Unit, UnitScope

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
        self.assertTrue(Unit.objects.filter(scope=self.scope, name="Gram").exists())
        self.assertTrue(
            Unit.objects.filter(scope=self.scope, name="Mililiter").exists()
        )

    def test_unit_names_must_be_unique_within_scope(self):
        with self.assertRaises(ValidationError):
            Unit.objects.create(
                scope=self.scope,
                name="Gram",  # Already created by the migration.
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
                name="Gram",  # Already exists in the global scope.
            )


class HiddenUnitModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="Fred",
            password="password",
        )
        self.scope = UnitScope.objects.get(user=None)
        self.gram = Unit.objects.get(
            scope=self.scope,
            name="Gram",
        )

    def test_user_can_hide_unit_only_once(self):
        HiddenUnit.objects.create(
            user=self.user,
            unit=self.gram,
        )

        with self.assertRaises(IntegrityError):
            HiddenUnit.objects.create(
                user=self.user,
                unit=self.gram,
            )

    def test_hidden_units_are_excluded_from_visible_units_queryset(self):
        # Create another global unit that is not hidden.
        liter = Unit.objects.create(
            scope=self.scope,
            name="Liter",
        )

        # Hide only Gram.
        HiddenUnit.objects.create(
            user=self.user,
            unit=self.gram,
        )

        visible_units = Unit.objects.exclude(
            hidden_by_users__user=self.user,
        )

        self.assertNotIn(self.gram, visible_units)
        self.assertIn(liter, visible_units)
