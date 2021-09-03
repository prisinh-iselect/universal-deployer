#!/usr/bin/env python3
"""
python3 deploy_cf_cloudhealth.py
Creates or Updates the CloudHealth roles in all the iSelect AWS accounts.
Deploys the role using the Cloudformation template from the 'aws-security-iam'
repo.

Authenticate to the iSelect 'AWS Master' account using the saml-admin role
using 'aws-azure-login'.
Usage:
    python3 test_access.py
"""
from iselect_access import iselect_session, iselect_accounts

obj = iselect_accounts()
print(f"Using '{obj._accounts_file}' file for accounts.")
count = 0
for account_id, attr in obj.accounts.items():
    print(account_id, attr)
    print(iselect_session(account_id).assumed_role_obj)
    count += 1
print(f"{count} Accounts tested ok.")
