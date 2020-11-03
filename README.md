# jamf-bulk-provisioning-profile-updator
A script to apply any provisioning profile present in Jamf to all in-house mobile device apps in Jamf.

If required to update expiering provisionoing profiles in Jamf, this tool aims to simplify the process by removing the bulk of the GUI-work required.
Intended workflow:

1. Upload the new provisioning profile to Jamf
2. Run the script and follow the prompts

The scipt will ask what profile to apply and will then move on to applying it to all mobile device apps in Jamf.

This script was written for a jamf instance where only in-house apps are present, but can be adapted to add more granularity and checks if required.
