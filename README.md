# SMApply API

This repo contains an API library to connect to the SM Apply API and do the following actions:
 - Create applications

## Getting Started

### Prerequisites

* Python 3.6 or later - [found here](http://www.python.org/getit/)
* You will also need a [SM Apply Access token](https://connect.smapply.io/pages/authentication.html)

### Setting up the config files

In the `config/` folder there is a config files:

#### **smapply.cfg**

This file is used to set up your credentials to SM Apply. To be able to connect to SM Apply, you will need the base URL to the SM Apply instance, as well as a Access Token. 

1. **URL = *https://example.smapply.com***

   * This is the URL to your SM Apply site

2. **BEARER = *access_token***

   * This will be the [SM Apply Access token](https://connect.smapply.io/pages/authentication.html).

3. **DEFAULT_PROGRAM_ID = *12345***

   * This is the ID of the program you want to be the default program users are enrolled in.

*Remember that your Access Token should be protected the same way you protect a password.*

---

## Running a python script

Most of the scripts in this repo can be run alone, or with an input file as the first argument of the script.

Also, on Windows, by default python scripts can be run by double clicking on them or by dragging an input file onto the script.

To give a script an input file in command line, the input looks like this:
```
python standing_deferred.py input.csv
```
or, if you have python2 installed as well as python3
```
python3 standing_deferred.py input.csv
```

---

## Create Application script (create_application.py)

The **create_application.py** script takes in a user and creates an application for that user of a particular program. If no program ID is given, it will default to the `DEFAULT_PROGRAM_ID` field found in the `smapply.cfg` file. 

### Running the script

**smapply.py** can be run stand-alone or with an input file.
```
python smapply.py input.csv
```

An example input file would look something like this:
```
email,program
example1@email.com,123
example2@email.com,456
example3@email.com,789
```
or, if you wanted to use the `DEFAULT_PROGRAM_ID`:
```
email
example1@email.com
example2@email.com
example3@email.com
```

What the script does is attempt to find the user_id of a given email address. If it finds it, it then attempts to create an application for a given program.

## Authors

* **Tyler Cinkant** - [lannro](https://github.com/lannro)