import os
import json
import dictdiffer
from datetime import datetime


def _write_in_last_fetched(result):
    with open('last-fetched.json', 'w') as f:
        json.dump(result, f)


def _write_diff(diffs):
    if not os.path.exists('changes'):
        os.makedirs('changes')
    now = datetime.now()
    with open(f'changes/{datetime.date(now)}-{now.hour}-{now.minute}-{now.second}.txt', 'w') as f:
        for diff in diffs:
            f.write(str(diff))


def check_diff(result):
    last_checked_result = {}
    if os.path.exists('last-fetched.json'):
        with open('last-fetched.json', 'r') as f:
            last_checked_result = json.load(f)

    diffs = list(dictdiffer.diff(last_checked_result, result))
    if diffs:
        _write_diff(diffs)

    _write_in_last_fetched(result)

    return diffs
