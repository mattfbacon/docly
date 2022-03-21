# docly

This was the first place submission at the Branham 2022 Hackathon.

## Setup, Installation, Usage

### Google API Setup

Create a new project in the Google Cloud Console. Make sure to enable the following APIs:

- Google Docs
- Google Drive
- Cloud Vision

(For cloud vision it is necessary to link a credit card to the account. This can be done in the Billing section. If you are a new user you get a 90 day free trial so we did not pay anything.)

In the Credentials section of the project, create a service account for Cloud Vision and an OAuth client ID for Docs and Drive. In the OAuth client, add yourself as a test user, and add both `http://localhost` and `http://localhost:1234` as authorized origins (the kind for the client, not the server).

Download the service account key to `server/key.json`. Replace the OAuth client ID in `client/src/App.jsx` with yours.

### Set Up and Build Client

```bash
cd client
yarn install
yarn build
```

### Set Up and Run Server

```bash
cd server
pipenv shell
# in the subshell:
pipenv install
GOOGLE_APPLICATION_CREDENTIALS="$(realpath key.json)" python backend.py
```

### Use the Application

Navigate to `http://localhost:1234`. Log in with Google, then take an image, then submit. Open the created Google Doc link to see your result!
