# Twilio Flex SSO Setup Guide

This guide walks through adding Twilio Flex as a SAML application in your identity provider (IdP). You will need administrator access to your IdP.

## Information from Twilio Flex
- **Entity ID:** `urn:flex:JQ9668343b2b51f296bf788f89201c9947`
- **ACS URL:** `https://login.flex.us1.twilio.com/login/callback?connection=JQ9668343b2b51f296bf788f89201c9947`

## Steps
1. **Create a new SAML application** in your IdP dashboard.
2. **Enter the Flex details** when prompted:
   - Entity ID as above.
   - Assertion Consumer Service (ACS) URL as above.
   - Name ID format: email address.
3. **Configure attribute mappings** so that the SAML assertion includes the following mandatory attributes:
   - `full name`
   - `email`
   - `Flex role` (values: `agent`, `supervisor`, or `administrator`)
4. **Download your IdP metadata** or copy the following values which Flex needs:
   - X.509 certificate
   - Single sign-on URL
   - Default redirect URL (optional)
   - Trusted URLs (optional)
5. **Provide the IdP values** in the Flex SSO settings page of the Twilio Console.
6. **Assign users** to this application in your IdP so they can log in to Flex.

## Next Steps
- Test SSO login by accessing Flex through the IdP.
- If issues arise, check that clock skew between the IdP and Flex is minimal and that attribute names match exactly.

For more detail see Twilio's official documentation on [Configuring SSO for Flex](https://www.twilio.com/docs/flex/admin-guide/setup/single-sign-on).
