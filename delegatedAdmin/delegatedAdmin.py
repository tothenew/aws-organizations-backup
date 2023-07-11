import boto3
import json
import os
import csv

def list_delegated_administrators():
    # Create an Organizations client
    client = boto3.client('organizations')

    # Create a list to store the delegated administrators and their associated services
    delegated_admins = []

    # Paginator for list_delegated_administrators API
    paginator = client.get_paginator('list_delegated_administrators')

    # Set the pagination parameters
    pagination_config = {'MaxItems': 10}
    page_iterator = paginator.paginate(PaginationConfig=pagination_config)

    # Iterate through each page of delegated administrators
    for page in page_iterator:
        admins = page['DelegatedAdministrators']

        # Iterate through each delegated administrator in the page
        for admin in admins:
            account_id = admin['Id']
            account_name = admin['Name']

            delegated_services_response = client.list_delegated_services_for_account(AccountId=account_id)

            # Extract the service names from the response
            service_names = [service['ServicePrincipal'] for service in delegated_services_response['DelegatedServices']]

            # Create a dictionary for the delegated administrator and associated services
            admin_data = {
                'Delegated Administrator Account ID': account_id,
                'Delegated Administrator Account Name': account_name,
                'Services': ', '.join(service_names)
            }

            delegated_admins.append(admin_data)

    # Specify the output file paths
    output_folder = os.path.join(os.getcwd(), 'output')
    json_file_path = os.path.join(output_folder, 'delegatedAdmin', 'delegated_admin.json')
    csv_file_path = os.path.join(output_folder, 'delegatedAdmin', 'delegated_admin.csv')

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Create the delegatedAdmin folder if it doesn't exist
    delegated_admin_folder = os.path.join(output_folder, 'delegatedAdmin')
    if not os.path.exists(delegated_admin_folder):
        os.makedirs(delegated_admin_folder)

    # Write the data to a JSON file
    with open(json_file_path, 'w') as json_file:
        json.dump(delegated_admins, json_file, indent=4)

    print("JSON file generated successfully with delegated administrators and their associated services.")

    # Write the data to a CSV file
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Delegated Administrator Account ID', 'Delegated Administrator Account Name', 'Services']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write the data rows
        for admin in delegated_admins:
            writer.writerow(admin)

    print("CSV file generated successfully with delegated administrators and their associated services.")

