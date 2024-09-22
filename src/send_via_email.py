import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import csv
from datetime import datetime, timedelta
import xml.etree.ElementTree as ET
import os

# Define the CSV file path
current_date_minus_one = (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')

# Load the filtered_marla file
filtered_marla = pd.read_csv(f'filtered_marla_{current_date_minus_one}.csv')

# Drop the 'open_position_date' column
filtered_marla.drop(columns=['Open_position_date'], inplace=True)

# Define the mapping for renaming
rename_mapping = {
    "IMFY": "RDM_0.5FO",
    "ITHK": "RDM_0.1GO",
    "IMFZ": "SIN_0.5FO",
    "IGSR": "SIN_0.1GO"
}

api_token = os.getenv('API_TOKEN')

# Rename the values in the 'instrument_code' column
filtered_marla['Instrument_Code'] = filtered_marla['Instrument_Code'].replace(rename_mapping)

# Convert 'last_traded_date' to datetime format
filtered_marla['Last_Traded_date'] = pd.to_datetime(filtered_marla['Last_Traded_date'])

# Convert 'last_traded_date' to the first date of the month
filtered_marla['Last_Traded_date'] = filtered_marla['Last_Traded_date'].apply(lambda x: x.replace(day=1))

# Filter dates starting from 2024
filtered_marla = filtered_marla[filtered_marla['Last_Traded_date'] >= '2024-01-01']

# Sort the DataFrame by 'Last_Traded_date' and 'Instrument_Code' in ascending order
filtered_marla.sort_values(by=['Last_Traded_date', 'Instrument_Code'], ascending=[True, True], inplace=True)

# Save the modified file with date in the filename
modified_file_path = f'filtered_marla_modified_{current_date_minus_one}.csv'
filtered_marla.to_csv(modified_file_path, index=False)

def send_email(subject, body, to_emails, attachment_path):
    from_email = "epp@cmm.gr"
    from_password = "Eur0b#nk2324!!"
    smtp_server = "smtp.office365.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = ", ".join(to_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment = open(attachment_path, "rb")
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= " + attachment_path)
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(from_email, from_password)
    text = msg.as_string()
    server.sendmail(from_email, to_emails, text)
    server.quit()

# Example usage with date in subject
subject_date = (datetime.now() - timedelta(days=2)).strftime('%Y%m%d')
send_email(
    subject=f"Bunker Curves {subject_date}",
    body="Please find the modified file for the daily bunker curves.",
    to_emails=["epoulea@lmm.gr"],
    attachment_path=modified_file_path
)