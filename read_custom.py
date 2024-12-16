import csv
from io import StringIO
import pandas as pd

def parse_file_to_pandas(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    
    sections = content.split("\n\n")
    data = []
    
    for section in sections:
        if section.strip():
            lines = section.strip().split("\n")
            header = {}
            csv_data = []
            
            # Parsing the header
            for i, line in enumerate(lines):
                if ':' in line:
                    key, value = line.split(":", 1)
                    header[key.strip()] = value.strip()
                else:
                    break
            
            # Parsing the CSV part
            csv_part = "\n".join(lines[i:])
            csv_reader = csv.DictReader(StringIO(csv_part))
            for row in csv_reader:
                csv_data.append(row)
            
            # Convert csv_data to a pandas DataFrame
            df = pd.DataFrame(csv_data)
            
            data.append({
                'header': header,
                'csv': df
            })
    
    return data

if __name__ == "__main__":
    file_path = 'example.txt'
    parsed_data = parse_file_to_pandas(file_path)

    for section in parsed_data:
        print(f"Header: {section['header']}")
        print("CSV Data:")
        print(section['csv'])
        print("\n")
