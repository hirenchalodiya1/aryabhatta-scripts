from robobrowser import RoboBrowser
from decorator import with_login
from scrapper import transcript
from secrets import CREDENTIALS


@with_login
def main(browser, **kwargs):
    return transcript(browser)


RoBo = RoboBrowser(parser="html.parser")
results = {}
for username, password in CREDENTIALS:
    results[username] = main(username=username, password=password, browser=RoBo)
    import json

    print(f"{username} Sem 9 result")
    print(json.dumps(results[username][9]["result"], indent=4, sort_keys=True))
