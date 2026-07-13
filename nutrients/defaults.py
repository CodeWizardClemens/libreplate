from pydantic import BaseModel
from typing import Optional


class NutrientSchema(BaseModel):
    name: str
    description: Optional[str] = None
    abbreviation: Optional[str] = None

    show_in_diary_total: bool = False
    show_in_diary_meal: bool = False
    show_in_food_edit: bool = False
    show_in_recipe: bool = False
    show_in_foods: bool = False
    show_in_goal_edit: bool = False

    usda_nutrient_number: Optional[str] = None
    order: int = 0


def nutrient_everywhere(**kwargs):
    return NutrientSchema(
        show_in_diary_total=True,
        show_in_diary_meal=True,
        show_in_food_edit=True,
        show_in_recipe=True,
        show_in_foods=True,
        show_in_goal_edit=True,
        **kwargs,
    )


def nutrient_recipe_food_edit(**kwargs):
    return NutrientSchema(
        show_in_food_edit=True,
        show_in_recipe=True,
        **kwargs,
    )


DEFAULT_NUTRIENTS = [
    nutrient_everywhere(
        name="Energy",
        description="Energy provided by food.",
        abbreviation=None,
        usda_nutrient_number="1008",
        order=1,
    ),
    nutrient_everywhere(
        name="Fat",
        description="Total fat content.",
        abbreviation=None,
        usda_nutrient_number="1004",
        order=2,
    ),
    nutrient_recipe_food_edit(
        name="Saturated Fat",
        description="Saturated fatty acids.",
        abbreviation="Sat fat",
        usda_nutrient_number="1258",
        order=3,
    ),
    nutrient_everywhere(
        name="Carbohydrates",
        description="Total carbohydrate content.",
        abbreviation="Carbs",
        usda_nutrient_number="1005",
        order=4,
    ),
    nutrient_recipe_food_edit(
        name="Sugar",
        description="Total sugars.",
        abbreviation=None,
        usda_nutrient_number="2000",
        order=5,
    ),
    nutrient_recipe_food_edit(
        name="Fiber",
        description="Dietary fiber content.",
        abbreviation=None,
        usda_nutrient_number="1079",
        order=6,
    ),
    nutrient_everywhere(
        name="Protein",
        description="Total protein content.",
        abbreviation=None,
        usda_nutrient_number="1003",
        order=7,
    ),
    nutrient_recipe_food_edit(
        name="Sodium",
        description="Sodium content.",
        abbreviation=None,
        usda_nutrient_number="1093",
        order=8,
    ),
    NutrientSchema(name="Cholesterol", description="Cholesterol content.", usda_nutrient_number="1253"),
    NutrientSchema(name="Water", description="Water content.", usda_nutrient_number="1051"),
    NutrientSchema(name="Alcohol", description="Alcohol content.", usda_nutrient_number="1018"),
    NutrientSchema(name="Caffeine", description="Caffeine content.", usda_nutrient_number="1057"),
    NutrientSchema(name="Theobromine", description="Theobromine content.", usda_nutrient_number="1058"),
    NutrientSchema(name="Calcium", description="Calcium content.", usda_nutrient_number="1087"),
    NutrientSchema(name="Iron", description="Iron content.", usda_nutrient_number="1089"),
    NutrientSchema(name="Magnesium", description="Magnesium content.", usda_nutrient_number="1090"),
    NutrientSchema(name="Phosphorus", description="Phosphorus content.", usda_nutrient_number="1091"),
    NutrientSchema(name="Potassium", description="Potassium content.", usda_nutrient_number="1092"),
    NutrientSchema(name="Zinc", description="Zinc content.", usda_nutrient_number="1095"),
    NutrientSchema(name="Copper", description="Copper content.", usda_nutrient_number="1098"),
    NutrientSchema(name="Selenium", description="Selenium content.", usda_nutrient_number="1103"),
    NutrientSchema(name="Retinol", description="Retinol content.", usda_nutrient_number="1105"),
    NutrientSchema(name="Vitamin A, RAE", description="Vitamin A activity equivalents.", usda_nutrient_number="1106"),
    NutrientSchema(name="Beta Carotene", description="Beta carotene content.", usda_nutrient_number="1107"),
    NutrientSchema(name="Alpha Carotene", description="Alpha carotene content.", usda_nutrient_number="1108"),
    NutrientSchema(name="Vitamin E", description="Alpha-tocopherol content.", usda_nutrient_number="1109"),
    NutrientSchema(name="Vitamin D", description="Vitamin D (D2 + D3) content.", usda_nutrient_number="1114"),
    NutrientSchema(name="Beta Cryptoxanthin", description="Beta cryptoxanthin content.", usda_nutrient_number="1120"),
    NutrientSchema(name="Lycopene", description="Lycopene content.", usda_nutrient_number="1122"),
    NutrientSchema(name="Lutein + Zeaxanthin", description="Lutein and zeaxanthin content.", usda_nutrient_number="1123"),
    NutrientSchema(name="Vitamin C", description="Total ascorbic acid content.", usda_nutrient_number="1162"),
    NutrientSchema(name="Thiamin", description="Vitamin B1 content.", usda_nutrient_number="1165"),
    NutrientSchema(name="Riboflavin", description="Vitamin B2 content.", usda_nutrient_number="1166"),
    NutrientSchema(name="Niacin", description="Vitamin B3 content.", usda_nutrient_number="1167"),
    NutrientSchema(name="Vitamin B6", description="Vitamin B6 content.", usda_nutrient_number="1175"),
    NutrientSchema(name="Folate", description="Total folate content.", usda_nutrient_number="1177"),
    NutrientSchema(name="Vitamin B12", description="Vitamin B12 content.", usda_nutrient_number="1178"),
    NutrientSchema(name="Choline", description="Total choline content.", usda_nutrient_number="1180"),
    NutrientSchema(name="Vitamin K", description="Phylloquinone content.", usda_nutrient_number="1185"),
    NutrientSchema(name="Folic Acid", description="Folic acid content.", usda_nutrient_number="1186"),
    NutrientSchema(name="Folate, Food", description="Naturally occurring folate.", usda_nutrient_number="1187"),
    NutrientSchema(name="Folate, DFE", description="Dietary folate equivalents.", usda_nutrient_number="1190"),
    NutrientSchema(name="Added Vitamin E", description="Added vitamin E content.", usda_nutrient_number="1242"),
    NutrientSchema(name="Added Vitamin B12", description="Added vitamin B12 content.", usda_nutrient_number="1246"),
    NutrientSchema(name="Butyric Acid (4:0)", description="4-carbon saturated fatty acid.", usda_nutrient_number="1259"),
    NutrientSchema(name="Caproic Acid (6:0)", description="6-carbon saturated fatty acid.", usda_nutrient_number="1260"),
    NutrientSchema(name="Caprylic Acid (8:0)", description="8-carbon saturated fatty acid.", usda_nutrient_number="1261"),
    NutrientSchema(name="Capric Acid (10:0)", description="10-carbon saturated fatty acid.", usda_nutrient_number="1262"),
    NutrientSchema(name="Lauric Acid (12:0)", description="12-carbon saturated fatty acid.", usda_nutrient_number="1263"),
    NutrientSchema(name="Myristic Acid (14:0)", description="14-carbon saturated fatty acid.", usda_nutrient_number="1264"),
    NutrientSchema(name="Palmitic Acid (16:0)", description="16-carbon saturated fatty acid.", usda_nutrient_number="1265"),
    NutrientSchema(name="Stearic Acid (18:0)", description="18-carbon saturated fatty acid.", usda_nutrient_number="1266"),
    NutrientSchema(name="Oleic Acid (18:1)", description="Monounsaturated fatty acid.", usda_nutrient_number="1268"),
    NutrientSchema(name="Linoleic Acid (18:2)", description="Omega-6 fatty acid.", usda_nutrient_number="1269"),
    NutrientSchema(name="Linolenic Acid (18:3)", description="Omega-3 fatty acid.", usda_nutrient_number="1270"),
    NutrientSchema(name="Arachidonic Acid (20:4)", description="Polyunsaturated fatty acid.", usda_nutrient_number="1271"),
    NutrientSchema(name="DHA (22:6 n-3)", description="Docosahexaenoic acid.", usda_nutrient_number="1272"),
    NutrientSchema(name="Palmitoleic Acid (16:1)", description="Monounsaturated fatty acid.", usda_nutrient_number="1275"),
    NutrientSchema(name="Parinaric Acid (18:4)", description="Polyunsaturated fatty acid.", usda_nutrient_number="1276"),
    NutrientSchema(name="Gadoleic Acid (20:1)", description="Monounsaturated fatty acid.", usda_nutrient_number="1277"),
    NutrientSchema(name="EPA (20:5 n-3)", description="Eicosapentaenoic acid.", usda_nutrient_number="1278"),
    NutrientSchema(name="Erucic Acid (22:1)", description="Monounsaturated fatty acid.", usda_nutrient_number="1279"),
    NutrientSchema(name="DPA (22:5 n-3)", description="Docosapentaenoic acid.", usda_nutrient_number="1280"),
    NutrientSchema(name="Total Monounsaturated Fatty Acids", description="Total MUFA content.", usda_nutrient_number="1292"),
    NutrientSchema(name="Total Polyunsaturated Fatty Acids", description="Total PUFA content.", usda_nutrient_number="1293"),
]