import boto3
import json
import os
import csv
from datetime import datetime

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

def load_service_config():
    # Get the absolute path of the JSON file
    current_directory = os.path.dirname(os.path.abspath(__file__))
    json_file_path = os.path.join(current_directory, 'service_config.json')

    # Load the service configuration from the JSON file
    with open(json_file_path) as config_file:
        service_config = json.load(config_file)

    return service_config

def list_enabled_services():
    org_client = boto3.client('organizations')
    service_config = load_service_config()

    # Create a paginator for the ListAWSServiceAccessForOrganization API
    paginator = org_client.get_paginator('list_aws_service_access_for_organization')
    page_iterator = paginator.paginate()

    # Create a list to store the enabled service objects
    service_objects = []

    # Iterate over the pages of results
    for page in page_iterator:
        # Extract the enabled services and their details from the page
        enabled_services = page['EnabledServicePrincipals']

        # Populate the list with the service objects
        for service in enabled_services:
            service_principal = service['ServicePrincipal']
            service_name = service_config.get(service_principal, 'Unknown')
            service_object = {
                service_principal: service_name
            }
            service_objects.append(service_object)

    # Create a dictionary with the list of service objects
    data = {
        'Enabled Services': service_objects
    }

    # Convert datetime objects to string representation
    data_serialized = json.dumps(data, indent=4, default=serialize_datetime)

    # Find the output folder path
    current_directory = os.getcwd()
    output_folder = os.path.join(current_directory, 'output')

    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Specify the output file paths
    json_file_path = os.path.join(output_folder, 'servicesEnabled', 'enabled_services.json')
    csv_file_path = os.path.join(output_folder, 'servicesEnabled', 'enabled_services.csv')

    # Write the enabled services to a JSON file
    with open(json_file_path, 'w') as file:
        file.write(data_serialized)

    print("JSON file generated successfully with enabled services.")

    # Convert JSON to CSV
    csv_data = []
    header = ["Service Principal", "Service Name"]
    csv_data.append(header)

    for service in service_objects:
        service_principal = next(iter(service))
        row = [service_principal, service_config.get(service_principal, 'Unknown')]
        csv_data.append(row)

    with open(csv_file_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(csv_data)

    print("CSV file generated successfully from JSON.")

