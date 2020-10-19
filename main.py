import jamf_api


class ProvisioningProfile:
    def __init__(self, profile):
        self.id = profile["id"]
        self.name = profile["name"]
        self.display_name = profile["display_name"]
        self.uuid = profile["uuid"]


def main():
    # Initial user auth to JPS
    usr_session = jamf_api.jamf_auth()

    # Fetch and display all provisioning profiles
    proviprofiles = [ProvisioningProfile(profile) for profile in jamf_api.jamf_provisioning_profiles(usr_session)]
    print("\nThe following provisioning profiles are available in Jamf")
    for profile in proviprofiles:
        print(f"""Name: {profile.display_name}\nUUID: {profile.uuid}\nID: {profile.id}""")
        print("-------------------------------------------")

    while True:
        if input("Provide the ID of the provisioning profile you want to set all apps to?").isdigit():




if __name__ == '__main__':
    main()
