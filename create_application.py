from util import get_smapply_instance
from util.file import read_from_csv, write_to_csv
import logging
import sys
import traceback
import re, json
from datetime import datetime

smapply = get_smapply_instance()
DEFAULT_PROGRAM_ID = smapply.default_program_id   

def get_user(**kwargs):
    kwargs =  {k.lower(): v for k, v in kwargs.items()}
    
    email = kwargs['email']

    global smapply
    logging.debug(f"Looking up user '{email}'")
    
    user = smapply.call_api(f"users/?email={email}",
                            method="GET")


    if not user:
        logging.warning(f"Could not find user with email '{email}'")
        return

    if len(user) == 1:
        user = user[0]

    return user

def create_user(**kwargs):
    kwargs =  {k.lower(): v for k, v in kwargs.items()}
    
    active = kwargs['active']
    custom_fields = kwargs['custom_fields']
    email = kwargs['email']
    first_name = kwargs['first_name']
    language_preference = kwargs['language_preference']
    last_name = kwargs['last_name']
    roles = kwargs['roles']
    timezone = kwargs['timezone']    
    
    global smapply
    logging.debug(f"Starting creation of user")

    post_fields = {"custom_fields":custom_fields,
                   "email":email,
                   "first_name":first_name,
                   "language_preference":language_preference,
                   "last_name":last_name,
                   "roles":roles,
                   "timezone":timezone,}

    user = smapply.call_api("users/",
                            method="POST",
                            post_fields=post_fields)

    if not user:
        logging.warning(f"Could not create user")
        return
    logging.info(f"User '{first_name} {last_name}' successfully created.")
    return user


def create_application(**kwargs):
    kwargs =  {k.lower(): v for k, v in kwargs.items()}

    if 'applicant' in kwargs:
        applicant = kwargs['applicant']

    elif 'email' in kwargs:
        email = kwargs['email']
        user = get_user(email=email)
        if not user or 'id' not in user:
            logging.warning(f"Could not create application for user:{email}")
            return
        applicant = user['id']
    else:
        raise KeyError("email or applicant_id")

    if 'program' in kwargs:
        program = kwargs['program']
    else:
        program = DEFAULT_PROGRAM_ID
    
    global smapply
    logging.debug(f"Starting creation of application for applicant:{applicant}")
    
    post_fields = {"applicant":applicant,
                   "program":program,
                   }


    application = smapply.call_api("applications/", method="POST",
                                   post_fields=post_fields)
    

    if not application:
        if 'email' in kwargs:
            logging.warning(f"Could not create application for applicant:{email}")
            return [email, "failed"]
        else:
            logging.warning(f"Could not create application for applicant:{applicant}")
            return [applicant, "failed"]


    if 'email' in kwargs:
        logging.info(f"Application successfully created for applicant:{email}")
        return [email, "success"]
    else:
        logging.info(f"Application successfully created for applicant:{applicant}")
        return [email, "success"]


if __name__ == "__main__":
    if len(sys.argv) > 1:
        _input = read_from_csv(sys.argv[1], data_has_headers=True)
    else:
        _input = [{
            "email":input("email: ")}]

    output = [["email", "status"]]
    for row in _input:
        try:
            user = create_application(**row)
            output.append(user)
        except KeyError as e:
            logging.error("Missing input value: {}".format(e))
            continue
        except Exception as e:
            traceback.print_exc()
            logging.error("Unexpected error occured: {}:{}".format(type(e).__name__, e))
            logging.warning("{} failed".format(row))
            continue

    if len(output) > 1:
            write_to_csv(datetime.now().strftime('new-applications-%Y%m%d-%H%M%S.csv'), output)
        
    input("press enter to close...")
