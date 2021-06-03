from robobrowser import RoboBrowser
from decorator import with_login
from scrapper import transcript
from secrets import CREDENTIALS
from diff import check_diff
from sendmail import send_mail
import argparse
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument('--sendMail', type=str, dest="send_mail", default=None, nargs="*")
parser.add_argument('--sendAll', action='store_true', dest="send_all", default=False)
options = parser.parse_args(sys.argv[1:])



@with_login
def main(browser, **kwargs):
    return transcript(browser)


RoBo = RoboBrowser(parser="html.parser")
results = {}
try:
    for username, password in CREDENTIALS:
        print(f'{username}: Transcript being fetched')
        results[username] = main(username=username, password=password, browser=RoBo)

    if options.send_mail:
        for u in options.send_mail:
            txt = json.dumps(results.get(u, {}), indent=4, sort_keys=True)
            send_mail("Your Transcript", txt, targets=[f"{u}@iitj.ac.in"])
        sys.exit()

    if options.send_all:
        for u in results.keys():
            txt = json.dumps(results.get(u, {}), indent=4, sort_keys=True)
            send_mail("Your Transcript", txt, targets=[f"{u}@iitj.ac.in"])
        sys.exit()

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
