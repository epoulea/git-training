import requests
from datetime import datetime, timedelta
import os

# Define the API endpoint and token
api_url = "https://api.veslink.com/v1/imosmessaging/queue"
api_token = os.getenv('API_TOKEN')

# Get today's date minus one day
yesterday_date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

# Generate the filename with yesterday's date
filename = f"output_marla_{yesterday_date}.xml"
# Read the XML file content
with open(filename, "r") as xml_file:
    xml_content = xml_file.read()

# Set the headers with the API token
headers = {
    "Authorization": f"Bearer {api_token}",
    "Content-Type": "application/xml"
}

# Make the API request to post the XML data
response = requests.post(api_url, data=xml_content, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    print("XML data successfully posted to the API.")
else:
    print(f"Error posting XML data. Status code: {response.status_code}")
