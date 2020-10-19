import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import getpass
from datetime import datetime, timedelta

JPSURL = "https://erikbille.jamfcloud.com"


class UserSession:
    def __init__(self, *args):
        self.username = args
        self.password = args
        self.token = args
        self.token_exp_epoc = args


def jamf_auth():
    session = UserSession()
    session.username = input("Enter Jamf Pro username:")
    pwd = getpass.getpass("Enter Jamf Pro password:")

    while True:
        response = requests.post(f"{JPSURL}/api/auth/tokens",
                                 auth=HTTPBasicAuth(session.username, pwd),
                                 headers={'Accept': 'application/json',
                                          'Content-Type': 'application/json'})

        if response.status_code == 200:
            session.password = pwd
            session.token_exp_epoc = datetime.fromtimestamp(int(response.json()["expires"] / 1000)) + timedelta(hours=1)
            session.token = response.json()["token"]
            print(f"\nLogin successful. You session will expire at {session.token_exp_epoc} GMT +2")

            del pwd

            return session
        elif response.status_code == 401:
            print(f"\nThe password for {session.username} was incorrect. Please try again")
            pwd = getpass.getpass(f"Enter password for {session.username}:")

        else:
            print(f"\nHmm... Something is not right. We had an HTTP Error {response.status_code}. Please investigate.")
            exit(1)


def jamf_provisioning_profiles(session):
    response = requests.get(f"{JPSURL}/JSSResource/mobiledeviceprovisioningprofiles",
                            auth=HTTPBasicAuth(session.username, session.password),
                            headers={'Accept': 'application/json',
                                     'Content-Type': 'application/json'}).json()

    return response['mobile_device_provisioning_profiles']
