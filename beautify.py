import json

def beautify_json(filename):
    try:
        with open(filename, 'r') as file:
            # Read the JSON content from the file
            data = json.load(file)
        
        # Beautify (pretty-print) the JSON content
        beautified_json = json.dumps(data, indent=4, sort_keys=True)
        
        # Write the beautified JSON back to the file
        with open(filename, 'w') as file:
            file.write(beautified_json)
        
        print(f"Successfully beautified the JSON in {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
beautify_json('./Maricopa_County_Voting_Precincts_(2022-)_-5644063468020972726.geojson')
