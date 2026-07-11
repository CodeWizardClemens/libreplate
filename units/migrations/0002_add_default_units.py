from django.db import migrations


def create_default_units(apps, schema_editor):
    UnitScope = apps.get_model("units", "UnitScope")
    Unit = apps.get_model("units", "Unit")

    global_scope, _ = UnitScope.objects.get_or_create(
        user=None
    )

    default_units = [
        {
            "name": "Gram",
            "abbreviation": "g",
            "description": "SI unit of mass",
        },
        {
            "name": "Mililiter",
            "abbreviation": "ml",
            "description": "SI unit of volume",
        },
        {
            "name": "Piece",
            "abbreviation": "",
            "description": "A single piece of something."
        },
        {
            "name": "Scoop",
            "abbreviation": "",
            "description": "A single scoop of something."
        },
    ]

    for unit in default_units:
        Unit.objects.get_or_create(
            scope=global_scope,
            name=unit["name"],
            defaults={
                "abbreviation": unit["abbreviation"],
                "description": unit["description"],
            },
        )


def remove_default_units(apps, schema_editor):
    Unit = apps.get_model("units", "Unit")
    Unit.objects.filter(
        scope__user=None
    ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("units", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_default_units,
            reverse_code=remove_default_units,
        ),
    ]