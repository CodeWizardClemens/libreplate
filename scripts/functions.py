SCRIPT_FUNCTIONS = {
    "add_food_to_diary": {
        "name": "Add food to diary",
        "fields": [
            {"name": "food_id", "type": "food", "label": "Food"},
            {"name": "amount", "type": "integer", "label": "Amount", "default": 1},
            {
                "name": "meal",
                "type": "choice",
                "label": "Meal",
                "choices": ["breakfast", "lunch", "dinner", "snack"],
            },
            {
                "name": "for",
                "type": "choice",
                "label": "For",
                "choices": ["today", "tomorrow", "next_7_days", "in_4_days"],
            },
            {
                "name": "starting",
                "type": "choice",
                "label": "Starting",
                "choices": ["now", "next_monday", "next_sunday"],
            },
        ],
    }
}
