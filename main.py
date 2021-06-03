from robobrowser import RoboBrowser
from decorator import with_login
from scrapper import transcript
from secrets import CREDENTIALS
from diff import check_diff
from sendmail import send_mail


@with_login
def main(browser, **kwargs):
    return transcript(browser)


RoBo = RoboBrowser(parser="html.parser")
results = {}
try:
    for username, password in CREDENTIALS:
        print(f'{username}: Transcript being fetched')
        results[username] = main(username=username, password=password, browser=RoBo)

    diffs = check_diff(results)
    if diffs:
        text = ""
        for d in diffs:
            text += f"{d}\n\n"
        send_mail("Transcript got updated in Aryabhatta", text)
    else:
        print("No difference")
except Exception as e:
    send_mail("Error in Aryabhatta Script", str(e))
