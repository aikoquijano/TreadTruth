# ThreadTruth - Sequence Logic

garment_id = "SHIRT-L-BLUE"

# Use indexes to get information from the garment ID
category = garment_id[0:5]
size = garment_id[6]
color = garment_id[8:12]

print("Garment ID:", garment_id)
print("Category:", category)
print("Size:", size)
print("Color:", color)

# Iterate through the garment ID
print("Scanning garment ID:")

for character in garment_id:
    print(character)