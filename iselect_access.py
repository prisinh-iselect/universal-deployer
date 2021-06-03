import boto3
from typing import Any


class iselect_session:

    _role_session_name = "SecurityAssumeRoleSession"
    _role_name = "OrganizationAccountAccessRole"

    def __init__(self, account_id, role_name=""):
        self.aws_account = account_id
        if role_name:
            self._role_name = role_name
        self.session()
        self.cf_client()

    def session(self):
        sts_client = boto3.client("sts")
        self.assumed_role_obj = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{self.aws_account}:role/{self._role_name}",
            RoleSessionName=self._role_session_name,
        )

    def cf_client(self):
        creds = self.assumed_role_obj["Credentials"]
        self.cf_client = boto3.client(
            "cloudformation",
            aws_access_key_id=creds["AccessKeyId"],
            aws_secret_access_key=creds["SecretAccessKey"],
            aws_session_token=creds["SessionToken"],
        )


class iselect_accounts:

    _accounts_file = "active_accounts.txt"
    default_key = "ACTIVE"
    accounts: dict[str, Any] = dict()

    def __init__(self, accounts_file=""):
        if accounts_file:
            self._accounts_file = accounts_file
        self.load_accounts()

    def load_accounts(self):
        with open(self._accounts_file) as f:
            for line in f:
                self.accounts[line.strip()] = self.default_key
