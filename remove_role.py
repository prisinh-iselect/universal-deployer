#!/usr/bin/env python3
"""
python3 remove_role.py

Authenticate to the iSelect 'AWS Security' account using the saml-admin role
using 'aws-azure-login'.
Usage:
    python3 remove_role.py
"""
from botocore.exceptions import ClientError
from iselect_access import iselect_session, iselect_accounts

acnt_obj = iselect_accounts('active_accounts.txt')
print(f"Using '{acnt_obj._accounts_file}' file for accounts.")

count = 0
total = 0
for account_id, attr in acnt_obj.accounts.items():
    print(account_id, attr)
    session = iselect_session(account_id)
    client = session.client('iam')
    try:
        response = client.delete_role_policy(
            RoleName='OrganizationAccountAccessRole',
            PolicyName='AdministratorAccess'
        )
        del_rsp = client.delete_role(
            RoleName='OrganizationAccountAccessRole'
        )
        count += 1
    except ClientError as e:
        print(e)
    total += 1

print(f"{count} command of {total} run ok.")
