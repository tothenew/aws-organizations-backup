import boto3
import json
import os
import csv

def get_account_details():
    client = boto3.client('organizations')

    organization_info = client.describe_organization()
    master_account_id = organization_info['Organization']['MasterAccountId']

    # Set the input parameters
    params = {
        'MaxResults': 10  # Update the MaxResults value to a lower value within the range
    }

    # Create a paginator for the list_accounts API
    paginator = client.get_paginator('list_accounts')
    page_iterator = paginator.paginate(**params)

    # Create a list to store the account details
    account_details = []

    # Iterate over the pages of results
    for page in page_iterator:
        # Iterate over the accounts and extract the details
        for account in page['Accounts']:
            account_id = account['Id']
            account_name = account['Name']
            account_email = account['Email']
            account_status = account['Status']
            account_joined_method = account['JoinedMethod']

            # Determine the account type
            account_type = ''
            if account_id == master_account_id:
                account_type = 'Master Account'
            elif account_joined_method == 'INVITED':
                account_type = 'Invited'
            elif account_joined_method == 'CREATED':
                account_type = 'Created'
            else:
                account_type = 'Unknown'

            # Create a dictionary for the account details
            account_info = {
                'account-id': account_id,
                'account-name': account_name,
                'account-email': account_email,
                'account-type': account_type
            }

            # Add the account details to the list
            account_details.append(account_info)

    # Find the output folder path
    current_directory = os.getcwd()
    output_folder = os.path.join(current_directory, 'output')

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the output file paths
    account_details_folder = os.path.join(output_folder, 'accountDetails')
    json_file = os.path.join(account_details_folder, 'account_details.json')
    csv_file = os.path.join(account_details_folder, 'account_details.csv')

    # Create the Account details folder if it doesn't exist
    if not os.path.exists(account_details_folder):
        os.makedirs(account_details_folder)

    # Wrap the account details dictionary with the key "Account Details"
    data = {
        'Account Details': account_details
    }

    # Write the account details to a JSON file
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print("JSON file generated successfully with account details.")

    # Convert JSON to CSV
    with open(json_file, 'r') as json_file:
        data = json.load(json_file)

    csv_data = []
    header = data['Account Details'][0].keys() if data['Account Details'] else []
    csv_data.append(header)

    for item in data['Account Details']:
        row = [item[key] for key in header]
        csv_data.append(row)

    with open(csv_file, 'w', newline='\n') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    print("CSV file generated successfully from JSON.")


