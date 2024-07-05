import csv

# Read the CSV file in binary mode and strip the BOM
with open('/Users/prasanth/Desktop/GhostInACell/Dataset/2023_0113/right/burst_ds.csv', 'rb') as f:
    data = f.read()
    if data[:3] == b'\xef\xbb\xbf':
        data = data[3:]

# Read the CSV data
reader = csv.reader(data.decode().splitlines())
rows = [row for row in reader]

# Create a new list to store the output
output = []

# Iterate over each row in the input
for values in rows:
    # Convert the values to integers, ignoring blank cells
    values = [int(v) for v in values if v]
    
    # Create a new list of 600 elements, all set to 0
    row_output = [0] * 600
    
    # Set the values at the specified positions to 1
    for v in values:
        row_output[v - 1] = 1
    
    # Add the row to the output
    output.append(row_output)

# Write the output to a new CSV file
with open('/Users/prasanth/Desktop/GhostInACell/Dataset/2023_0113/right/burst_ds_remapped.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(output)
