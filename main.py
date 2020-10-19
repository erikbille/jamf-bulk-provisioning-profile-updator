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
    print("-------------------------------------------")
    for profile in proviprofiles:
        print(f"""Name: {profile.display_name}\nUUID: {profile.uuid}\nID: {profile.id}""")
        print("-------------------------------------------")

    while True:
        selection = input("Provide the ID of the provisioning profile you want to set all apps to?\n")
        if selection.isdigit():
            selected_profile = [profile for profile in proviprofiles if profile.id == int(selection)][0]
            if selected_profile:
                print("You have selected the following provisioning profile:")
                print("-------------------------------------------")
                print(f"""Name: {profile.display_name}\nUUID: {profile.uuid}\nID: {profile.id}""")
                print("-------------------------------------------")
                break
            else:
                print("\nThe ID you selected is not valid. Please refer to the previous output.")




if __name__ == '__main__':
    main()
