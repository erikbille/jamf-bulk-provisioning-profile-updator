import jamf_api
import dicttoxml
from progressbar import ProgressBar
pbar = ProgressBar()


class ProvisioningProfile:
    def __init__(self, profile):
        self.id = profile["id"]
        self.name = profile["name"]
        self.display_name = profile["display_name"]
        self.uuid = profile["uuid"]


class MobileDeviceApp:
    def __init__(self, app):
        self.name = app["name"]
        self.bundle_id = app["bundle_id"]
        self.version = app["version"]
        self.provisioning_profile = app["provisioning_profile"]

    def asdict(self):
        return {"general":
                    {"name": f"{self.name}",
                     "bundle_id": self.bundle_id,
                     "version": self.version,
                     "provisioning_profile":
                         {"id": self.provisioning_profile.id,
                          "display_name": self.provisioning_profile.display_name,
                          "uuid": self.provisioning_profile.uuid},
                     }
                }


def main():
    # Initial user auth to JPS
    usr_session = jamf_api.jamf_auth()

    # Fetch and display all provisioning profiles
    proviprofiles = [ProvisioningProfile(profile) for profile in jamf_api.jamf_provisioning_profiles(usr_session)]
    print("\n[*] The following provisioning profiles are available in Jamf")
    print("-------------------------------------------")
    for profile in proviprofiles:
        print(f"""[*] Name: {profile.display_name}\n[*] UUID: {profile.uuid}\n[*] ID: {profile.id}""")
        print("-------------------------------------------")

    # User profile selection
    while True:
        selection = input("[?] Provide the ID of the provisioning profile you want to set all apps to:")
        if selection.isdigit():
            selected_profile = [profile for profile in proviprofiles if profile.id == int(selection)][0]
            if selected_profile:
                print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
                print("[*] You have selected the following provisioning profile:")
                print("-------------------------------------------")
                print(f"""[*] Name: {profile.display_name}\n[*] UUID: {profile.uuid}\n[*] ID: {profile.id}""")
                print("-------------------------------------------")
                break
            else:
                print("\n[!] The ID you selected is not valid. Please refer to the previous output.")

    # Fetch apps in Jamf
    apps = [app["id"] for app in jamf_api.jamf_mobiledeviceapps(usr_session)]
    print("\n\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    while True:
        print(
            f"[*] {len(apps)} Mobile device applications are available in Jamf. Do you wish set the previously selected "
            f"profile for all apps?")

        decision = input("[?] yes or no:")
        if decision == "yes":
            for i in pbar(apps):
                # Get full mobile decive object
                full_app = MobileDeviceApp(jamf_api.jamf_mobiledeviceapp(usr_session, i))
                full_app.provisioning_profile = selected_profile
                jamf_api.jamf_update_mobiledeviceapp(usr_session,
                                                     i,
                                                     dicttoxml.dicttoxml(full_app.asdict(),
                                                                         custom_root='mobile_device_application',
                                                                         attr_type=False)
                                                     )
            break

        elif decision == "no":
            print("\n\n[*] Script exiting. No changes has been made.")
            exit(1)
        else:
            print("\n[!] Invalid selection. Please type either yes or no")


if __name__ == '__main__':
    main()
