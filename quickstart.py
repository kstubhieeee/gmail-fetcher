import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
import email

SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
   
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
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
        
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
       
        service = build("gmail", "v1", credentials=creds)
        results = service.users().messages().list(userId='me', q='from:onlinelearner01learn@gmail.com').execute()
        messages = results.get('messages', [])

        if not messages:
            print("No messages found.")
        else:
            print("Messages:")
            for message in messages:
                msg = service.users().messages().get(userId='me', id=message['id'], format='full').execute()
                
                subject = None
                for header in msg['payload']['headers']:
                    if header['name'] == 'Subject':
                        subject = header['value']
                
                body = ''
                if 'data' in msg['payload']['parts'][0]['body']:
                    body = base64.urlsafe_b64decode(msg['payload']['parts'][0]['body']['data']).decode('utf-8')
                else:
                    body = base64.urlsafe_b64decode(msg['payload']['body']['data']).decode('utf-8')

                is_read = 'UNREAD' not in msg['labelIds']

                print(f"Subject: {subject}")
                print(f"Body: {body}")
                print(f"Read/Unread: {'Read' if is_read else 'Unread'}")
                print("--------------------------------------------------")

    except HttpError as error:
        
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()
