# from O365 import Account

# credentials = ('10124d50-7607-444e-8590-caa29d638259', 'T.l8Q~GctZxf4oeB0Qoemb5t.Grgu9IfDB2HWaYl')

# # Initialize the account with the specified credentials and tenant ID
# account = Account(credentials, auth_flow_type='credentials', tenant_id='f6460e3b-75d2-446f-844c-12959214fd5d')

# # Authenticate the account
# if account.authenticate():
#     print('Authenticated!')

#     # Access the inbox folder
#     mailbox = account.mailbox()
#     inbox = mailbox.inbox_folder()

#     # Retrieve messages
#     for message in inbox.get_messages():
#         print(message)

#     # Access the sent folder
#     sent_folder = mailbox.sent_folder()
#     print(sent_folder)
# else:
#     print('Authentication failed. Check your credentials.')


# import requests
 
# # Replace with your own values

# client_id = "10124d50-7607-444e-8590-caa29d638259 "

# client_secret = "T.l8Q~GctZxf4oeB0Qoemb5t.Grgu9IfDB2HWaYl"

# tenant_id = "f6460e3b-75d2-446f-844c-12959214fd5d"

# user_email = "epp@cmm.gr"
 
# token_url = f"https://login.microsoftonline.com/f6460e3b-75d2-446f-844c-12959214fd5d/oauth2/token"

# graph_api_url = "https://graph.microsoft.com/v1.0/me/messages"
 
# payload = {

#     "grant_type": "client_credentials",

#     "client_id": client_id,

#     "client_secret": client_secret,

#     "resource": "https://graph.microsoft.com",

# }
 
# response = requests.post(token_url, data=payload)
# access_token = response.json().get("access_token")

# headers = {
#     "Authorization": f"Bearer {access_token}",
# }

# # Customize your subject here
# subject_to_search = "MARLA_TRADING_Trades"

# params = {
#     "$filter": f"receivedDateTime ge 2024-08-01T00:00:00Z and subject eq '{subject_to_search}'",
# }

# response = requests.get(graph_api_url, headers=headers, params=params)
# emails = response.json()

# for email in emails.get("value", []):
#     print(f"Subject: {email.get('MARLA_TRADING_Trades')}")
#     print(f"Received: {email.get('receivedDateTime')}")
#     print("-" * 30)
#     print(emails)

import os
import requests
import json
from datetime import datetime,timedelta

client_id = '10124d50-7607-444e-8590-caa29d638259'
client_secret = 'T.l8Q~GctZxf4oeB0Qoemb5t.Grgu9IfDB2HWaYl'
tenant_id = 'f6460e3b-75d2-446f-844c-12959214fd5d'
specific_sender = 'marex-reporting-suite@marex.com'
download_directory = r'C:\Users\epp\OneDrive - LATSCO\Desktop\New folder'  # Change this to your desired directory

def get_access_token():
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default"
    }
    response = requests.post(url, data=payload)
    response_data = response.json()
    access_token = response_data['access_token']
    return access_token

def download_attachment(message_id, attachment_id, attachment_name, access_token):
    url = f"https://graph.microsoft.com/v1.0/users/epp@cmm.gr/messages/{message_id}/attachments/{attachment_id}/$value"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        file_path = os.path.join(download_directory, attachment_name)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        print(f"Attachment {attachment_name} downloaded successfully to {file_path}.")
    else:
        print("Error downloading attachment:")
        print(response.status_code)
        print(response.text)

def read_email():
    access_token = get_access_token()
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    url = f"https://graph.microsoft.com/v1.0/users/epp@cmm.gr/messages?$filter=from/emailAddress/address eq '{specific_sender}'"
    # response = requests.get(url, headers=headers)
    yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d')
    today = datetime.now().strftime('%Y-%m-%d')
    print(yesterday)
    print(today)
    yesterday_formatted = (datetime.now() - timedelta(1)).strftime('%Y%m%d')
    # print("Response Status Code:", response.status_code)
    # print("Response Text:", response.text)
    all_emails=[]
    while url:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            emails = data.get('value', [])
            all_emails.extend(emails)

            url = data.get('@odata.nextLink')
        else:
            print("Failed to retrieve emails:", response.status_code, response.text)
            break


# Your existing code to get emails
    for email in all_emails:
        received_date = email['receivedDateTime']
        if received_date.startswith(today):
            message_id = email.get('id')
            attachments_url = f"https://graph.microsoft.com/v1.0/users/epp@cmm.gr/messages/{message_id}/attachments"
            attachments_response = requests.get(attachments_url, headers=headers)
            if attachments_response.status_code == 200:
                attachments = attachments_response.json().get('value', [])
                if not attachments:
                    print("No attachments found.")
                else:
                    for attachment in attachments:
                        attachment_name = attachment.get('name')
                        print(f"Found attachment: {attachment_name}")
                        if attachment_name == f"MARLA_TRADING_Positions.{yesterday_formatted}.csv":
                            attachment_id = attachment.get('id')
                            download_url = f"https://graph.microsoft.com/v1.0/users/epp@cmm.gr/messages/{message_id}/attachments/{attachment_id}/$value"
                            download_response = requests.get(download_url, headers=headers)
                            if download_response.status_code == 200:
                                with open(attachment_name, 'wb') as file:
                                    file.write(download_response.content)
                                print(f"Downloaded {attachment_name}")
                            else:
                                print(f"Failed to download {attachment_name}")

read_email()

columns_to_keep = ['Open_position_date', 'Instrument_Code', 'Last_Traded_date', 'Market_Rate']
codes_to_keep = ['IMFY', 'ITHK', 'IMFZ', 'IGSR']

import pandas as pd
from datetime import datetime, timedelta

def filter_csv_columns(csv_file_path, output_file_path, columns_to_keep, codes_to_keep):
    # Read the CSV data into a pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Convert 'Open_position_date' and 'Last_Traded_date' to datetime
    df['Open_position_date'] = pd.to_datetime(df['Open_position_date'])
    df['Last_Traded_date'] = pd.to_datetime(df['Last_Traded_date'])

    # Get the current month and year
    current_year = datetime.now().year
    current_month = datetime.now().month

    # Calculate the previous month
    previous_month = current_month - 1 if current_month > 1 else 12
    previous_year = current_year if current_month > 1 else current_year - 1
    print(current_month)
    print(previous_month)

    # Filter rows based on 'Instrument_Code', excluding data from the previous month
    df_filtered = df[
        (df['Instrument_Code'].isin(codes_to_keep)) &
        (
            # (df['Open_position_date'].dt.year > current_year) |
            # ((df['Open_position_date'].dt.year == current_year) & (df['Open_position_date'].dt.month >= current_month)) |
            (df['Last_Traded_date'].dt.year > previous_year) |
            ((df['Last_Traded_date'].dt.year == previous_year) & (df['Last_Traded_date'].dt.month > previous_month))
        )
    ][columns_to_keep]

    # Drop duplicates based on the specified columns
    df_filtered.drop_duplicates(inplace=True)

    # Write the filtered data to a new CSV file
    df_filtered.to_csv(output_file_path, index=False)

    print(f"Filtered data saved to {output_file_path}")

# Get the current date and subtract one day
current_date_minus_one = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')

# Set the file paths with the current date minus one
csv_file_path = f'MARLA_TRADING_Positions.{current_date_minus_one}.csv'
output_file_path = f'filtered_marla_{current_date_minus_one}.csv'

# Call the function to filter the CSV columns and codes
filter_csv_columns(csv_file_path, output_file_path, columns_to_keep, codes_to_keep)

# Print a success message
print(f"CSV file has been filtered to only include the columns: {', '.join(columns_to_keep)}.")
print(f"Only rows with codes {', '.join(codes_to_keep)} in the 'Instrument_Code' column have been included.")
print(f"The filtered data has been saved to {output_file_path}.")