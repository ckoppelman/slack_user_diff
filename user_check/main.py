import os
import os.path
import json
import shutil
import pathlib
from datetime import datetime

from user_check import get_list, process_list, diff_csvs

LOG_THRESHOLD = int(os.environ["LOG_THRESHOLD"])

PATH_TO_CREDS = os.environ["CREDENTIALS_PATH"]

CURRENT_RUN = datetime.utcnow().isoformat()

pathlib.Path("data/processed").mkdir(parents=True, exist_ok=True)
pathlib.Path("data/raw").mkdir(parents=True, exist_ok=True)
pathlib.Path("data/diff").mkdir(parents=True, exist_ok=True)

CURRENT_RUN_STATIC_PATH = "data/processed/current.csv"
PREV_RUN_STATIC_PATH = "data/processed/prev.csv"

SLACK_TEAM_NAME = os.environ["SLACK_TEAM_NAME"]

data = get_list.get_user_list(PATH_TO_CREDS, SLACK_TEAM_NAME)

with open("data/raw/" + CURRENT_RUN + ".json", "w") as out:
    out.write(json.dumps(data))

process_list.save_to_csv(data["members"], "data/processed/" + CURRENT_RUN + ".csv")

if os.path.isfile(CURRENT_RUN_STATIC_PATH):
    os.rename(CURRENT_RUN_STATIC_PATH, PREV_RUN_STATIC_PATH)

shutil.copy("data/processed/" + CURRENT_RUN + ".csv", CURRENT_RUN_STATIC_PATH)


if os.path.isfile(PREV_RUN_STATIC_PATH) and os.path.isfile(CURRENT_RUN_STATIC_PATH):
    csv_diff, change_dict, num_changed, deleted_rows = diff_csvs.compare_csvs(
        PREV_RUN_STATIC_PATH,
        CURRENT_RUN_STATIC_PATH,
        "id",
        ignore_fields=["updated_date"],
        treat_as_delete=["is_deleted"],
    )
    with open("data/diff/" + CURRENT_RUN + ".diff.json", "w") as diff_file:
        diff_file.write(json.dumps(csv_diff))

    print(f"{num_changed} changes since last run.")
    if num_changed >= LOG_THRESHOLD:
        print(json.dumps(change_dict, indent=4, sort_keys=True))

    print(f"Deleted/deactivated row ids:\n   {deleted_rows}")
