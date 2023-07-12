# AWS Organizations Backup

## Introduction

AWS Organizations is a service provided by Amazon Web Services (AWS) that allows you to centrally manage and govern multiple AWS accounts. It provides a way to organize your accounts into a hierarchical structure and apply policies across the organization.

 #### About AWS Organizations Backup

 


AWS Organizations Backup is a tool designed to capture and backup important details of your AWS Organization. It allows you to retrieve and store information such as:

- Retrieve account details.
- Enabled services & policies.
- AI, SCP, Backup & Tag Policies.
- Fetch Delegated Administrator configuration.


  
## Permissions Required 

To run the scripts and access the required resources, make sure the user or role executing the code has the necessary permissions. You have two options:

   1. Use the built-in "AWSOrganizationsReadOnlyAccess" policy.
   2. Create a custom IAM policy with the required permissions.

If you choose to create a custom policy, refer to the provided JSON document for the required permissions.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "organizations:DescribeOrganization",
                "organizations:ListAccounts",
                "organizations:ListAWSServiceAccessForOrganization",
                "organizations:ListRoots",
                "organizations:ListPolicies",
                "organizations:DescribePolicy",
                "organizations:ListTargetsForPolicy",
                "organizations:ListDelegatedAdministrators",
                "organizations:ListDelegatedServicesForAccount"
            ],
            "Resource": "*"
        }
    ]
}

```

## Getting Started


Check out the following GIF to see the complete procedure of getting AWS Organizations Backup. 

![GIF](https://github.com/sahil121-12/aws-organizations-backup/blob/integration/File1.gif)


To use this project, follow these steps:

1. Clone the repository to your local machine.

```bash
git clone https://github.com/sahil121-12/aws-organizations-backup
cd aws-organizations-backup
```
2. Install the required dependencies listed in `requirement.txt`.
            
```bash
pip3 install -r requirement.txt
```


3. Execute `main.py` to run the project. Choose one of the following options:

    - To retrieve all details:
    ```bash
         python3 main.py --all 
    ```
    - To retrieve Account details:
    ```bash
         python3 main.py --account
    ```
     - To retrieve enabled Organization Services:
    ```bash
         python3 main.py --service
    ```
     - To retrieve enabled Policy Types:
    ```bash
         python3 main.py --policytype
    ```
     - To retrieve policy documents for SCP, AI, Backup & Tag Policies:
    ```bash
         python3 main.py --policies scp
    ``` 
    ```bash
         python3 main.py --policies tag,ai
    ```
     - To retrieve delegated admin details :
    ```bash
         python3 main.py --delegated
    ```

4. Check the `output` directory for the generated results.



