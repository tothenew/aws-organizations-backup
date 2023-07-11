import boto3
import json
import os
import csv

def get_enabled_policy_types():
    # Create an Organizations client
    client = boto3.client('organizations')

    # Create a paginator for listing roots
    paginator = client.get_paginator('list_roots')

    # Set the pagination parameters
    pagination_config = {'MaxItems': 1}  # Update the MaxItems value as desired

    # Retrieve the list of roots
    response_iterator = paginator.paginate(PaginationConfig=pagination_config)

    # Create a dictionary to store enabled policy types
    enabled_policy_types = {'Enabled Policy': {}}

    # Iterate over the pages of roots
    for response in response_iterator:
        roots = response['Roots']
        for root in roots:
            policy_types = root['PolicyTypes']
            for policy_type in policy_types:
                policy_type_name = policy_type['Type']
                policy_type_status = policy_type['Status']

                if policy_type_status == 'ENABLED':
                    enabled_policy_types['Enabled Policy'][policy_type_name] = 'enabled'

    # Convert the output to JSON format
    output_json = json.dumps(enabled_policy_types, indent=4)

    # Convert JSON to CSV
    csv_data = []
    header = ['Policy Type', 'Status']
    csv_data.append(header)

    for policy_type, status in enabled_policy_types['Enabled Policy'].items():
        row = [policy_type, status]
        csv_data.append(row)

    # Specify the output folder path
    current_directory = os.getcwd()
    output_folder = os.path.join(current_directory, 'output', 'policiesEnabled')

    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Save the JSON output to a file
    json_file_path = os.path.join(output_folder, 'enabled_policy_types.json')
    with open(json_file_path, 'w') as file:
        file.write(output_json)

    print("JSON file generated successfully with enabled policy types.")

    # Save the CSV output to a file
    csv_file_path = os.path.join(output_folder, 'enabled_policy_types.csv')
    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    print("CSV file generated successfully from JSON.")

# Call the function to get en
