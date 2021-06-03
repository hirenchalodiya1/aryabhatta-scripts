from robobrowser import RoboBrowser
from decorator import with_login
from scrapper import transcript
from secrets import CREDENTIALS
from diff import check_diff


@with_login
def main(browser, **kwargs):
    return transcript(browser)


RoBo = RoboBrowser(parser="html.parser")
results = {}
for username, password in CREDENTIALS:
    print(f'{username}: Transcript being fetched')
    results[username] = main(username=username, password=password, browser=RoBo)

diffs = check_diff(results)
if diffs:
    for d in diffs:
        print(d)
else:
    print("no difference")
