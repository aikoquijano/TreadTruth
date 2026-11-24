from search_engine import search_inventory

clothing_inventory = [
    {
        "item": "T-shirt",
        "details": {
            "size": "M",
            "water": 2700,
            "carbon": 2.5
        }
    },
    {
        "item": "Jeans",
        "details": {
            "size": "L",
            "water": 7500,
            "carbon": 10
        }
    },
    {
        "item": "Hoodie",
        "details": {
            "size": "S",
            "water": 5000,
            "carbon": 6
        }
    }
]

print("Welcome to ThreadTruth")
print("Available sizes: S, M, L")

try:
    search_size = input("Enter a size to search for: ").upper()

    if search_size not in ["S", "M", "L"]:
        raise ValueError

    result = search_inventory(clothing_inventory, search_size)

    if result:
        print("Item found:", result["item"])
        print("Size:", result["details"]["size"])
        print("Water impact:", result["details"]["water"], "liters")
        print("Carbon impact:", result["details"]["carbon"], "kg")
    else:
        print("No clothing item found with that size.")

except ValueError:
    print("Warning: Please enter a valid size (S, M, or L).")