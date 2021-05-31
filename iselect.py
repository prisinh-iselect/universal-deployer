import boto3
from typing import Any


class iselect_session():

    _role_session_name = "SecurityAssumeRoleSession"
    _role_name = "OrganizationAccountAccessRole"

    def __init__(self, account_id):
        self.aws_account = account_id
        self.session()

    def session(self):
        sts_client = boto3.client('sts')
        self.assumed_role_obj = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{self.aws_account}:role/{self._role_name}",
            RoleSessionName=self._role_session_name
        )


class iselect_accounts():

    _accounts_file = 'active_accounts.txt'
    default_key = "ACTIVE"
    accounts: dict[str, Any] = dict()

    def __init__(self):
        self.load_accounts()

    def load_accounts(self):
        with open(self._accounts_file) as f:
            for line in f:
                self.accounts[line.strip()] = self.default_key
