import os, sqlite3, win32crypt, json, sys, base64, shutil
from Crypto.Cipher import AES
from datetime import datetime, timedelta


# platform_table maps the name of user's OS to a platform code
platform_table = {
        'darwin': 0,
        'cygwin': 1,
        'win32': 1,
        }

# it supports MacOS, and Windows platforms.
try:
    user_platformcode = platform_table[sys.platform]
except KeyError:
    class NotAvailableOS(Exception):
        pass
    raise NotAvailableOS("It does not support your OS.")


def get_chrome_and_brave_datetime(chromedate):
    return datetime(1601, 1, 1) + timedelta(microseconds=chromedate)


def get_username() -> str:
    """
    Get username based on their local computers
    """
    platform_code = user_platformcode
    cwd_path = os.getcwd()
    cwd_path_list = []
    # if it is a macOS
    if platform_code == 1:
        cwd_path_list = cwd_path.split('/')
    # if it is a windows
    elif platform_code == 2:
        cwd_path_list = cwd_path.split('\\')
    # if it is a linux
    else:
        cwd_path_list = cwd_path.split('/')
    return cwd_path_list[2]


def get_database_paths() -> dict:
    """
    Get paths to the database of browsers and store them in a dictionary.
    It returns a dictionary: its key is the name of browser in str and its value is the path to database in str.
    """
    platform_code = user_platformcode
    browser_path_dict = dict()
    browser_filename_dict = dict()
    # if it is a macOS
    if platform_code == 0:
        cwd_path = os.getcwd()
        cwd_path_list = cwd_path.split('/')
        # it creates string paths to broswer databases
        abs_safari_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Safari', 'Local State.db')
        abs_chrome_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'Google/Chrome', 'Local State')
        abs_brave_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'BraveSoftware/Brave-Browser/', 'Local State')
        chrome_filename = "ChromeData.db"
        brave_filename = "BraveData.db"
        safari_filename = "SafariData.db"
        # check whether the databases exist
        if os.path.exists(abs_safari_path):
            browser_path_dict['safari'] = abs_safari_path
            browser_filename_dict['safari'] = safari_filename
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
            browser_filename_dict['chrome'] = chrome_filename
        if os.path.exists(abs_brave_path):
            browser_path_dict['brave'] = abs_brave_path
            browser_filename_dict['brave'] = brave_filename

    # if it is a windows
    if platform_code == 1:
        homepath = os.path.expanduser("~")
        abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Local State')
        abs_brave_path = os.path.join(homepath, 'AppData', 'Local', 'BraveSoftware', 'Brave-Browser', 'User Data', 'Local State')
        # it creates string paths to broswer databases
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
            browser_filename_dict['chrome'] = chrome_filename
        if os.path.exists(abs_chrome_path):
            browser_path_dict['brave'] = abs_brave_path
            browser_filename_dict['brave'] = brave_filename

    return browser_path_dict, browser_filename_dict



def get_encryption_key():
    
    local_state_path = get_database_paths()

    with open(local_state_path, "r", encoding="utf-8") as f:
        local_state = f.read()
        local_state = json.loads(local_state)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]

    return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]


def decrypt_password(password, key):
    
    key = get_encryption_key()

    try:
        iv = password[3:15]
        password = password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)

        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(password, None, None, None, 0)[1])

        except:
            return ""


def get_passwords(key) -> dict:
    """
        Get user's browser login info by using sqlite3 module to connect to the dabase.
        It returns a dictionary: its key is a name of browser in str and its value is a list of
        tuples, each tuple contains six elements, including origin url, action url, username, password, creation date & last used date. 
        Example
        -------
        >>> import browserpasswords as bp
        >>> dict_obj = bp.get_passwords()
        >>> dict_obj.keys()
        >>> dict_keys(['safari', 'chrome', 'firefox'])
        >>> dict_obj['safari'][0]
        >>> ("Origin URL: https://mail.protonmail.com/login",
            "Action URL: https://mail.protonmail.com/",
            "Username: klymroman@protonmail.com",
            "Password: MyPassword",
            "Creation date: 2015-09-18 09:35:16.013583",
            "Last Used: 2021-06-07 12:02:40.661260",
            "==================================================")
    """

    key = get_encryption_key()

    db_path, filename = get_database_paths()

    shutil.copyfile(db_path, filename)

    db = sqlite3.connect(filename)
    cursor = db.cursor()

    cursor.execute(
        "select origin_url, action_url, username_value, password_value, date_created, date_last_used from logins order by date_created")

    browser_passwords = {}

    for row in cursor.fetchall():
        origin_url = row[0]
        action_url = row[1]
        username = row[2]
        password = decrypt_password(row[3], key)
        date_created = row[4]
        date_last_used = row[5]
        if username or password:
            browser_passwords.append(f"Origin URL: {origin_url}")
            browser_passwords.append(f"Action URL: {action_url}")
            browser_passwords.append(f"Username: {username}")
            browser_passwords.append(f"Password: {password}")
        else:
            continue
        if date_created != 86400000000 and date_created:
            browser_passwords.append(f"Creation date: {str(get_chrome_and_brave_datetime(date_created))}")
        if date_last_used != 86400000000 and date_last_used:
            browser_passwords.append(f"Last Used: {str(get_chrome_and_brave_datetime(date_last_used))}")
        browser_passwords.append("="*50)

    cursor.close()
    db.close()
    try:
        os.remove(filename)
    except:
        pass

    return browser_passwords