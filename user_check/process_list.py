import csv
from datetime import datetime


def save_to_csv(user_dicts, csv_name):
    with open(csv_name, "w") as out_csv:
        writer = csv.DictWriter(
            out_csv, fieldnames=["id", "email", "name", "updated_date", "is_deleted"]
        )
        writer.writeheader()

        for user in sorted(user_dicts, key=lambda u: u["id"]):
            display_name = (
                user["profile"]["display_name"]
                if "display_name" in user["profile"]
                else None
            )
            real_name_normalized = (
                user["profile"]["real_name_normalized"]
                if "real_name_normalized" in user["profile"]
                else None
            )

            writer.writerow(
                {
                    "id": user["id"],
                    "email": user["profile"]["email"]
                    if "email" in user["profile"]
                    else None,
                    "name": real_name_normalized or display_name,
                    "updated_date": datetime.utcfromtimestamp(user["updated"]),
                    "is_deleted": user["deleted"],
                }
            )
