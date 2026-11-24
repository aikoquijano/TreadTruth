# ThreadTruth - Automation Engine

clothing_items = ["T-shirt", "Jeans", "Hoodie"]

water_limit = 2700  # Based on research about the approximate water needed for a cotton T-shirt

for item in clothing_items:
    if item == "T-shirt":
        water_used = 2700
    elif item == "Jeans":
        water_used = 7500
    else:
        water_used = 5000

    if water_used > water_limit:
        print(item, "has a high water impact.")
    else:
        print(item, "has a lower water impact.")
    