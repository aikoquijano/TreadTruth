# ThreadTruth - Nested Data

clothing_inventory = [
    {
        "item": "T-shirt",
        "details": {
            "water": 2700,
            "carbon": 2.5,
            "waste": 0.2
        }
    },
    {
        "item": "Jeans",
        "details": {
            "water": 7500,
            "carbon": 10,
            "waste": 0.5
        }
    },
    {
        "item": "Hoodie",
        "details": {
            "water": 5000,
            "carbon": 6,
            "waste": 0.4
        }
    }
]

for clothing in clothing_inventory:
    print("Item:", clothing["item"])

    for category, value in clothing["details"].items():
        print(category, ":", value)

    print("--------------------")