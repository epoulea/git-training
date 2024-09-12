import csv
from datetime import datetime, timedelta
import pandas as pd
import xml.etree.ElementTree as ET

# Define the CSV file path
current_date_minus_one = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')
csv_file_path = f'filtered_marla_{current_date_minus_one}.csv'

# Define the function to calculate difference in months
def difference_in_months(date1_str, date2_str):
    date_format = "%Y-%m-%d"
    date1 = datetime.strptime(date1_str, date_format)
    date2 = datetime.strptime(date2_str, date_format)
    year_diff = date2.year - date1.year
    month_diff = date2.month - date1.month
    total_months = year_diff * 12 + month_diff
    # if total_months % 3 == 0 and date2 > datetime(2025, 1, 31):
    #     return int(total_months/3),'MON'
    # else:
    return total_months, 'MON'

data=[]    

with open(csv_file_path, mode='r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the header row
    for row in csv_reader:
        date1 = row[0]  # Assuming date1 is in column A
        date2 = row[2]
        print(date1)
        print(date2)
        number, type = difference_in_months(date1, date2)
        print(f"Difference in months between {date1} and {date2}: {row[1]}+{number}{type}")

        # Replace specific strings in row[1] as per user request
        replacements = {
            "IMFY": "RDM_0.5FO",
            "ITHK": "RDM_0.1GO",
            "IMFZ": "SIN_0.5FO",
            "IGSR": "SIN_0.1GO"

        }
        for key, value in replacements.items():
            if key in row[1]:
                row[1] = row[1].replace(key, value)

        # Calculate the total number
        if number > 0:
            total_num = row[1] + "+" + str(number) + type
        else:
            total_num = row[1] + "+" + "CURMON"

        print(f"Total number: {total_num}")
        
        # Append the processed data to the list
        data.append([total_num, row[0], row[3]])


# Create a DataFrame from the list
df = pd.DataFrame(data, columns=['CMSRouteId', 'ArchiveDate', 'RouteAverage'])


# Print the DataFrame
print(df)

# Save the DataFrame to a CSV file
csv_file = f'filtered_marla_{current_date_minus_one}_new.csv'
df.to_csv(csv_file, index=False)

# Print a success message
print(f"DataFrame saved to {csv_file}")


def csv_to_xml(csv_file_path, xml_file_path, date_format="%Y-%m-%dT%H:%M:%S%z"):
    with open(csv_file_path, 'r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        root = ET.Element("RoutesUpdate")
        root.set("xmlns:xsi", "http://www.w3.org/2001/XMLSchema-instance")
        root.set("xmlns", "http://schemas.veson.com/2005/MarketDataImport")
        root.set("xmlns:imosmsg", "http://schemas.veson.com/2005/ImosMsg")
        root.set("Market", "Platts")
        root.set("Action", "Update")
        root.set("IsBunkerMarket", "Y")
    # with open(csv_file_path, 'r') as csv_file:
    #     csv_reader = csv.DictReader(csv_file)
    #     root = ET.Element("RoutesUpdate")
        for row in csv_reader:
            item = ET.Element("RouteUpdate")
            root.append(item)

            for key, value in row.items():
                field = ET.SubElement(item, key)
                # Check if the key is 'Last_trade_Date' and the value is not empty
                if key == 'ArchiveDate' and value:
                    # Parse the date from the format 'dd/mm/yyyy'
                    date_obj = datetime.strptime(value, '%Y-%m-%d')
                    # Convert the date to the format 'yyyy-mm-ddT00:00:00+00:00'
                    transposed_date = date_obj.strftime(date_format)
                    field.text = transposed_date
                else:
                    field.text = value

        tree = ET.ElementTree(root)
        tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)

# Set the file paths
csv_file_path = f'filtered_marla_{current_date_minus_one}_new.csv'
xml_file_path = f'output_marla_{current_date_minus_one}.xml'

# Call the function to convert CSV to XML and transpose the date
csv_to_xml(csv_file_path, xml_file_path)

# Print a success message
print(f"CSV data from {csv_file_path} has been successfully converted to XML and saved to {xml_file_path}.")



