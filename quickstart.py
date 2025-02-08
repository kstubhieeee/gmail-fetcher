import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "credentials.json", SCOPES
                )
                creds = flow.run_local_server(port=0)
            except FileNotFoundError:
                print("Error: The 'credentials.json' file was not found.")
                print("Please download it from the Google Cloud Console and place it in the same directory as this script.")
                return
        
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId='me', q='from:onlinelearner01learn@gmail.com').execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
        else:
            print("Messages:")
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id']).execute()
                print('Message snippet: %s' % msg['snippet'])

    except HttpError as error:
        # Handle errors from Gmail API
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()