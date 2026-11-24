def search_inventory(inventory, search_size):
    for clothing in inventory:
        if clothing["details"]["size"] == search_size:
            return clothing

    return None