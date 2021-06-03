#!/usr/bin/env python3
"""
python3 deploy_cf_org_access.py
Creates or Updates the Admin Access role from the Security account in all the
iSelect AWS accounts.
Deploys the role using the Cloudformation template from the 'aws-security-iam'
repo.

Authenticate to the iSelect 'AWS Master' account using the saml-admin role
using 'aws-azure-login'.
Usage:
    python3 deploy_cf_org_access.py
"""
from botocore.exceptions import ClientError
from typing import Any

from iselect_access import iselect_session, iselect_accounts


CF_TEMPLATE = (
    "/Users/prisinh/workspace/iselect/aws-security-iam/ansible/"
    "roles/org/files/sec-org-access.yaml"
)
CF_POLICY = (
    "/Users/prisinh/workspace/iselect/aws-security-iam/ansible/"
    "roles/org/files/policy.json"
)
PARAM: list[dict[str, Any]] = [{}]
TAGS = [
    {
        "Key": "User",
        "Value": "aws.operations.ops@iselect.com.au",
    },
    {
        "Key": "Description",
        "Value": "Security IAM Audit Admin Stack",
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
    stack_policy: str,
    tags: list[dict[str, str]],
) -> bool:
    """Deploy a Cloudformation stack
    Try to create the stack first. If that fails then the assumption is that
    the stack might already exists, hence try to update next.
    An update might fail as well, but sometimes that is desired as boto3
    returns an exception even when there is no update required to the stack.

    Keyword arguments:
    """
    args = {
        "StackName": name,
        "TemplateBody": body,
        "Parameters": param,
        "Capabilities": [
            "CAPABILITY_NAMED_IAM",
        ],
        "StackPolicyBody": stack_policy,
        "Tags": tags,
    }
    try:
        args["EnableTerminationProtection"] = True
        response = boto_client.create_stack(**args)
        print(response)
        return True
    except ClientError as e:
        print(f"{e}\n")
    try:
        args.pop("EnableTerminationProtection")
        response = boto_client.update_stack(**args)
        print(response)
        return True
    except ClientError as e:
        if(e.response['Error']['Code'] == "ValidationError"):
            print(f"Stack exists, error with Validation : {e}")
        else:
            print(f"Error with Update: {e}")
        return False


# This section gets all the necessary information for CF deployment and deploys
# to all iSelect accounts
with open(CF_TEMPLATE) as f:
    cf_body = f.read()

with open(CF_POLICY) as p:
    cf_policy = p.read()

for account_id, attr in iselect_accounts("test_accounts.txt").accounts.items():
    print(account_id, attr)
    session = iselect_session(account_id)
    deploy_stack(
        session.cf_client,
        "security-iam-audit-role",
        cf_body,
        PARAM,
        cf_policy,
        TAGS,
    )
    print(f"Deployed stack to account {account_id}\n=======")
