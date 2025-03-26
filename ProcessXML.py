import xml.etree.ElementTree as ET
import csv
import os

def extract_active_units(file_path):
    """
    Extracts <Name> values from the given .xscsys (XML) file
    where the corresponding <Active> value is 'true', excluding names containing '_'.
    
    :param file_path: Path to the .xscsys file
    :return: List of active unit names
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            xml_content = file.read()
        
        root = ET.fromstring(xml_content)
        
        active_names = []
        for item in root.findall(".//BusinessUnit"):
            name_element = item.find("Name")
            active_element = item.find("Active")
            
            if name_element is not None and active_element is not None:
                name_text = name_element.text.strip()
                if active_element.text.strip().lower() == "true" and "_" not in name_text:
                    active_names.append(name_text)
        
        return active_names
    except ET.ParseError:
        print(f"Error: Invalid XML structure in {file_path}.")
        return []
    except FileNotFoundError:
        print(f"Error: File not found: {file_path}.")
        return []
    except Exception as e:
        print(f"Unexpected error in {file_path}: {e}")
        return []

def read_export_csv(file_path):
    """
    Reads export.csv and extracts relevant columns, filling missing values with 'N/A'.
    
    :param file_path: Path to export.csv
    :return: Dictionary mapping Carrier integration code to row data
    """
    data = {}
    try:
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                carrier_code = row.get("Carrier integration code", "N/A").strip()
                data[carrier_code] = {
                    "Carrier integration code": carrier_code,
                    "Carrier integration name": row.get("Carrier integration name", "N/A").strip(),
                    "DM id": row.get("DM id", "N/A").strip(),
                    "MPM id": row.get("MPM id", "N/A").strip()
                }
        return data
    except FileNotFoundError:
        print("Error: export.csv not found.")
        return {}
    except Exception as e:
        print(f"Unexpected error while reading export.csv: {e}")
        return {}

def process_multiple_files(directory, export_csv_path, output_csv):
    """
    Processes multiple .xscsys files, merges data with export.csv, and saves to a new CSV file.
    
    :param directory: Directory containing the .xscsys files
    :param export_csv_path: Path to export.csv
    :param output_csv: Path to the output CSV file
    """
    files = [f"DM0{i}.xscsys" for i in range(1, 6)]
    export_data = read_export_csv(export_csv_path)
    all_combined_data = []
    
    for file_name in files:
        file_path = os.path.join(directory, file_name)
        active_units = extract_active_units(file_path)
        file_name_without_ext = os.path.splitext("MPM4" + file_name)[0]
        
        for unit in active_units:
            matched_data = export_data.get(unit, {  # Lookup by Active Unit Name
                "Carrier integration code": "N/A",
                "Carrier integration name": "N/A",
                "DM id": "N/A",
                "MPM id": "N/A"
            })
            all_combined_data.append([
                matched_data["DM id"],
                matched_data["MPM id"],
                matched_data["Carrier integration code"],
                matched_data["Carrier integration name"],
                file_name_without_ext
            ])
    
    with open(output_csv, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["DM_ID", "MPM_ID","Carrier_Integration_Code","Carrier_Integration_Name","MPM4DM"])
        writer.writerows(all_combined_data)
    
    print(f"Data saved to {output_csv}")

if __name__ == "__main__":
    directory = r"C:\Users\DP_PC\Desktop\Chrome Extensions\XSC files"
    export_csv_path = r"C:\Users\DP_PC\Desktop\Chrome Extensions\XSC files\export.csv"
    output_csv = "data.csv"
    process_multiple_files(directory, export_csv_path, output_csv)
