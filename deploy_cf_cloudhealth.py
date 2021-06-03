#!/usr/bin/env python3
"""
python3 deploy_cf_cloudhealth.py
Creates or Updates the CloudHealth roles in all the iSelect AWS accounts.
Deploys the role using the Cloudformation template from the 'aws-security-iam'
repo.

Authenticate to the iSelect 'AWS Master' account using the saml-admin role
using 'aws-azure-login'.
Usage:
    python3 deploy_cf_cloudhealth.py
"""
from botocore.exceptions import ClientError
from typing import Any

from iselect_access import iselect_session, iselect_accounts


CF_TEMPLATE = ("/Users/prisinh/workspace/iselect/aws-security-iam/ansible/"
               "roles/cloudhealth/files/cloudhealth-iselect-role.json")
PARAM: list[dict[str, Any]] = [{}]
TAGS = [
    {
        "Key": "User",
        "Value": "aws.operations.ops@iselect.com.au",
    },
    {
        "Key": "Description",
        "Value": "CloudHealth IAM Read Only Role. Provided by Optus.",
    },
    {
        "Key": "Repository",
        "Value": "https://github.com/iselect-services/aws-security-iam.git",
    },
    {
        "Key": "Project",
        "Value": "Security",
    },
]


def deploy_stack(
    boto_client,
    name: str,
    body: str,
    param: list[dict[str, Any]],
    tags: list[dict[str, str]],
) -> bool:
    """Deploy a Cloudformation stack
    Keyword arguments:
    """
    args = {
        "StackName": name,
        "TemplateBody": body,
        "Parameters": param,
        "Capabilities": [
            "CAPABILITY_NAMED_IAM",
        ],
        "Tags": tags,
    }
    try:
        response = boto_client.update_stack(**args)
        print(response)
        return True
    except ClientError as e:
        if(e.response['Error']['Code'] == "ValidationError"):
            print(f"Stack exists, error with Validation : {e}")
            return False
        else:
            print(f"Error with Update: {e}\nTry creating.")
    try:
        response = boto_client.create_stack(**args)
        print(response)
        return True
    except ClientError as e:
        print(f"{e}\n")
        return False


# Section that gets all the necessary information for CF deployment and deploys
# to all iSelect accounts
with open(CF_TEMPLATE) as f:
    cf_body = f.read()

for account_id, attr in iselect_accounts("test_accounts.txt").accounts.items():
    print(account_id, attr)
    session = iselect_session(account_id)
    deploy_stack(
        session.cf_client,
        "security-iam-cloudhealth-role",
        cf_body,
        PARAM,
        TAGS
    )
    print(f"Deployed stack to account {account_id}\n=======")
