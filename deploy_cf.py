import boto3

from iselect import iselect_session, iselect_accounts


for account_id, attr in iselect_accounts().accounts.items():
    print(account_id, attr)
    creds = iselect_session(account_id).assumed_role_obj['Credentials']
    print(creds)
    cf_client = boto3.client(
        'cloudformation',
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken']
    )

    break


#
#
#
# sts_client = boto3.client('sts')
#
# # Call the assume_role method of the STSConnection object and pass the role
# # ARN and a role session name.
# assumed_role_object = sts_client.assume_role(
#     RoleArn="arn:aws:iam::account-of-role-to-assume:role/name-of-role",
#     RoleSessionName="AssumeRoleSession1"
# )
#
# # From the response that contains the assumed role, get the temporary
# # credentials that can be used to make subsequent API calls
# credentials = assumed_role_object['Credentials']
#
# # Use the temporary credentials that AssumeRole returns to make a
# # connection to Amazon S3
# s3_resource = boto3.resource(
#     's3',
#     aws_access_key_id=credentials['AccessKeyId'],
#     aws_secret_access_key=credentials['SecretAccessKey'],
#     aws_session_token=credentials['SessionToken'],
# )
#
# # Use the Amazon S3 resource object that is now configured with the
# # credentials to access your S3 buckets.
# for bucket in s3_resource.buckets.all():
#     print(bucket.name)
