from constant import BASE_URL


def _get_semester_info(tr):
    td = tr.find_all("td")[0]
    return td.find_all("b")[0].text


def _course_result(tr):
    tds = tr.find_all("td")
    return {
        'course_code': tds[0].text,
        'course_name': tds[1].text,
        'credit': int(tds[3].text),
        'grade': tds[4].text
    }


def _scrap_table(table):
    trs = table.find_all("tr")
    semester = _get_semester_info(trs[1])
    result = []
    for tr in trs[2:]:
        result.append(_course_result(tr))
    return semester, result


POINT_SCHEME = {
    "A": 10,
    "B": 8,
    "C": 6,
    "D": 4,
    "F": 0
}


def _semester_aggregate_info(result):
    credits_earned = 0
    points_earned = 0
    for subject in result:
        credits_earned += subject["credit"]
        points_earned += POINT_SCHEME.get(subject["grade"], 0) * subject["credit"]
    total_points = credits_earned * 10
    sgpa = points_earned / total_points * 10

    return {
        'credits_earned': credits_earned,
        'points_earned': points_earned,
        'total_points': total_points,
        'sgpa': f"{sgpa:.2f}"
    }


def _get_aggregate_info(result):
    total_points = 0
    total_earned_points = 0
    total_credits = 0
    for key, value in result.items():
        try:
            _ = int(key)  # check it's semester number
            total_credits += value["aggregate_info"]["credits_earned"]
            total_earned_points += value["aggregate_info"]["points_earned"]
            total_points += value["aggregate_info"]["total_points"]
        except:
            pass
    cgpa = total_earned_points / total_points
    return {
        'total_points': total_points,
        'total_earned_points': total_earned_points,
        'total_credits': total_credits,
        'cgpa': f"{cgpa:.2f}"
    }


def transcript(browser):
    url = f"{BASE_URL}/transcript.do"
    browser.open(url)

    tables = browser.find_all("table")

    _transcript = {}
    semester_number = 1
    for table in tables[:-3]:
        sem, result = _scrap_table(table)
        _transcript[str(semester_number)] = {
            "semester": sem,
            "result": result,
            "aggregate_info": _semester_aggregate_info(result)
        }
        semester_number += 1

    _transcript["aggregate"] = _get_aggregate_info(_transcript)

    return _transcript
