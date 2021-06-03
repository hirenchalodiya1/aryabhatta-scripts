from constant import BASE_URL


def _login(browser, username, password):
    url = f"{BASE_URL}/"
    browser.open(url)
    form = browser.get_form()
    form['userid'] = username
    form['password'] = password
    browser.submit_form(form)


def _logout(browser):
    url = f"{BASE_URL}/logout.do"
    browser.open(url)


def with_login(func):
    def wrapper(*args, **kwargs):
        # checks
        browser = kwargs.get('browser', None)
        assert browser is not None, f"Provide driver in function {func.__name__} as browser=<browser_obj>"
        username = kwargs.get('username', None)
        assert username is not None, f"Provide username in function {func.__name__} as username=<username>"
        password = kwargs.get('password', None)
        assert password is not None, f"Provide password in function {func.__name__} as password=<password>"
        # login
        _login(browser, username, password)
        # do stuff
        ret = func(*args, **kwargs)
        # logout
        _logout(browser)
        return ret

    return wrapper
