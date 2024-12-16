import csv
from io import StringIO
import pandas as pd

def parse_file(file_path):
    data = []
    current_section = {'header': {}, 'csv': []}
    in_csv = False
    
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue

            # Check if the line is part of the header
            if ':' in line:
                if in_csv:
                    # If already in CSV mode and a header is encountered, store current section and reset
                    if current_section['csv']:
                        df = pd.DataFrame(csv.DictReader(StringIO("\n".join(current_section['csv']))))
                        current_section['csv'] = df
                    data.append(current_section)
                    current_section = {'header': {}, 'csv': []}
                    in_csv = False
                
                key, value = line.split(":", 1)
                current_section['header'][key.strip()] = value.strip()
            
            else:
                # Treat the line as part of the CSV data
                in_csv = True
                current_section['csv'].append(line)

    # Add the last section if there is any remaining data
    if current_section['csv']:
        df = pd.DataFrame(csv.DictReader(StringIO("\n".join(current_section['csv']))))
        current_section['csv'] = df
        data.append(current_section)
    
    return data

if __name__ == "__main__":
    file_path = 'example.txt'
    parsed_data = parse_file(file_path)

    for section in parsed_data:
        print(f"Header: {section['header']}")
        print("CSV Data:")
        print(section['csv'])
        print("\n")
