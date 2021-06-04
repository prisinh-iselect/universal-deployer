from iselect_access import iselect_session, iselect_accounts

count = 0
for account_id, attr in iselect_accounts().accounts.items():
    print(account_id, attr)
    print(iselect_session(account_id).assumed_role_obj)
    count += 1
print(f"{count} Accounts tested ok.")
