import json
import slack_sdk


def _get_token(path_to_creds, team_name):
    with open(path_to_creds) as f:
        creds = json.load(f)
        return [
            cred["token"] for cred in creds.values() if cred["team_domain"] == team_name
        ][0]


def get_user_list(path_to_creds, team_name):
    client = slack_sdk.WebClient(token=_get_token(path_to_creds, team_name))
    res = client.api_call(api_method="users.list")

    return res.data
