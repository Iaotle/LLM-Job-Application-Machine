#!/usr/bin/env python3

from __future__ import annotations
import os
import json

# Define the properties to add with None (null in JSON)
props = ['website', 'careers_page', 'address', 'sector']

# Directory containing the JSON files
directory = './companies'

# Iterate through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith('.json'):
        filepath = os.path.join(directory, filename)
        
        try:
            # Open and load the JSON file
            with open(filepath, 'r') as f:
                data = json.load(f)

            # Add default properties initialized to None if not already present
            for prop in props:
                if prop not in data:
                    data[prop] = None

            # Write the updated JSON back to the file
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=4)

            # print(f"Updated: {filename}")  # Confirm the update for each file

        except json.JSONDecodeError as e:
            print(f"Error decoding JSON in file {filename}: {e}")
        except Exception as e:
            print(f"An error occurred while processing {filename}: {e}")

print("Finished processing JSON files.")
