import boto3
from typing import Any


class iselect_session:

    _role_session_name = "SecurityAssumeRoleSession"
    _role_name = "SecurityAccountAccessRole"
    # ignore 'security' and 'audit' accounts. Changes need to be done manually
    # to these accounts.
    _ignore_account_ids = ['831840826019', '179730087721']

    def __init__(self, account_id, role_name=""):
        self.aws_account = account_id
        if(self.aws_account not in self._ignore_account_ids):
            self.session()
        if role_name:
            self._role_name = role_name

    def session(self):
        sts_client = boto3.client("sts")
        self.assumed_role_obj = sts_client.assume_role(
            RoleArn=f"arn:aws:iam::{self.aws_account}:role/{self._role_name}",
            RoleSessionName=self._role_session_name,
        )

    def client(self, boto_service='cloudformation'):
        if(self.aws_account in self._ignore_account_ids):
            self.client = boto3.client(boto_service)
        else:
            creds = self.assumed_role_obj["Credentials"]
            self.client = boto3.client(
                boto_service,
                aws_access_key_id=creds["AccessKeyId"],
                aws_secret_access_key=creds["SecretAccessKey"],
                aws_session_token=creds["SessionToken"],
            )
        return self.client


class iselect_accounts:

    _accounts_file = "test_accounts.txt"
    default_key = "ACTIVE"
    accounts: dict[str, Any] = dict()

    def __init__(self, accounts_file=""):
        """
        Accepts accounts_file argument. Pass the name of the file including the
        whole path, if not in the same directory.
        """
        if accounts_file:
            self._accounts_file = accounts_file
        self.load_accounts()

    def load_accounts(self):
        with open(self._accounts_file) as f:
            for line in f:
                self.accounts[line.strip()] = self.default_key
