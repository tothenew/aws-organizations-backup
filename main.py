
from enabledAccounts import accountDetail
from enabledPolices import aiPolicies, backupPolicies, scpPolicies, tagPolicies, enabledPolicy
from enabledServices import enableService
from delegatedAdmin import delegatedAdmin


import click
@click.command()
@click.option('--account', '--a', is_flag=True, help='fetch account details')
@click.option('--service', '--s', is_flag=True, help='fetch services enabled')
@click.option('--policytype', '--p', is_flag=True, help='fetch policy type enabled')
@click.option('--delegated', '--d', is_flag=True, help='fetch delegated admin details')
@click.option('--policies', '--pol', type=str, default='', help='fetch specific policy and all policies')
@click.option('--all', '--al', is_flag=True, help='fetch all details')

def run_modules(account, service,policytype,delegated,policies,all):
    if account:
        click.echo("Getting account details...")
        account_module_function()
    
    if service:
        click.echo("Getting services enabled...")
        service_module_function()
    if policytype:
        click.echo("Getting Policy type enabled...")
        policytype_module_function()
    if delegated:
        click.echo("Getting delegated admin  details...")
        delegatedadmin_module_function()
    
    if policies:
        policies = policies.split(',')
        click.echo("Getting policy detail for: {}".format(', '.join(policies)))
        for policy in policies:
            policy = policy.strip()
            if policy == 'scp':
                click.echo("Getting SCP policies...")
                scp_policies_module_function()
            elif policy == 'tag':
                click.echo("Getting Tag policies...")
                tag_policies_module_function()
            elif policy == 'backup':
                click.echo("Getting Backup policies...")
                backup_policies_module_function()
            elif policy == 'ai':
                click.echo("Getting AI policies...")
                ai_policies_module_function()
            elif policy == 'All':
                click.echo("Getting All policies details...")
                scp_policies_module_function()
                tag_policies_module_function()
                backup_policies_module_function()
                ai_policies_module_function()
            else:
                click.echo(f"Unknown policy module: {policy}")



    if all:
        click.echo("Getting All details...")
        account_module_function()
        service_module_function()
        policytype_module_function()
        delegatedadmin_module_function()
        allpolicies_module_function()



def account_module_function():
    
    accountDetail.get_account_details()

def service_module_function():
    
    enableService.list_enabled_services()
    


def policytype_module_function():
    
    enabledPolicy.get_enabled_policy_types()

def delegatedadmin_module_function():
    
    delegatedAdmin.list_delegated_administrators()

def allpolicies_module_function():
    
    def main():
         aiPolicies.list_ai_policies()
         backupPolicies.list_backup_policies()
         scpPolicies.list_scp_policies()
         tagPolicies.list_tag_policies()
    main()

def scp_policies_module_function():
    
    scpPolicies.list_scp_policies()


def tag_policies_module_function():
    
    tagPolicies.list_tag_policies()
def backup_policies_module_function():
    
    backupPolicies.list_backup_policies()

def ai_policies_module_function():
    
   aiPolicies.list_ai_policies()


    
run_modules()

