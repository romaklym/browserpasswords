# 🔑🔓🖥️ Browser Passwords

browserpasswords is a simple Python module that extracts browser login info from a user's local computer and writes the data to csv files.

Platforms: Linux, MacOS, and Windows.
Suported Browsers: Google Chrome, Brave and Safari. 

## 📦 Installation
```sh
$ python3 -m pip install browserpasswords
```

or 

```sh
$ git clone https://github.com/romaklym/browserpasswords
```


## ✅ Overview
### 🔨 Functions:
- get_passwords() -> dict
- get_database_paths() -> dict
- get_username() -> str


#### 🔍 Example:
```python
Example

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
```

### 📈 The Description of browserpasswords

```
NAME

    browserpasswords

FUNCTIONS

    get_passwords() -> dict
        Get user's browser login info by using sqlite3 module to connect to the dabase.
        It returns a dictionary: its key is a name of browser in str and its value is a list of tuples, each tuple contains six elements, including
        origin url, action url, username, password, creation date & last used
        date. 
    
    get_database_paths() -> dict
        Get paths to the database of browsers and store them in a dictionary.
        It returns two dictionaries: first & second file keys is the name of
        browser in str and value of the first is the path to database in str
        value of the second is the name of database file.
    
    get_username() -> str
        Get username based on their local computers
```

### 🐛 Issue Report 

If you find issues or bugs report them to:
- https://github.com/romaklym/browserpasswords

