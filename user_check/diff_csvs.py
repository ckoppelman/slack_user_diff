from collections import defaultdict

from csv_diff import load_csv, compare


def compare_csvs(prev_path, curr_path, key, ignore_fields=[]):
    csv_diff = compare(
        load_csv(open(prev_path), key=key), load_csv(open(curr_path), key=key)
    )

    changed = defaultdict(list)
    changed_rows = 0

    for change in csv_diff["changed"]:
        changed_fields = change["changes"].keys()
        counted = False
        for field in changed_fields:
            if field not in ignore_fields:
                if not counted:
                    changed_rows += 1
                    counted = True
                changed[field].append(change["key"])

    changed_rows += len(csv_diff["removed"])

    return csv_diff, changed, changed_rows
