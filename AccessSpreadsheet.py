from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os.path

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEETID= "1ow5o_vwY-JV6lip8RhVg6Rv-qIOf7oaiU30GQiie4m0"

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # result = sheet.values().get(spreadsheetId=SPREADSHEETID,
        #                             range='Sheet1!A1:C5').execute()
        # values = result.get('values', [])
        # if not values:
        #     print('No data found.')
        # else:
        #     for row in values:
        #         print(f'{row[0]}, {row[1]}')

        for row in range(1,6):
            num1 = int(sheet.values().get(spreadsheetId=SPREADSHEETID,range=f'Sheet1!A{row}').execute().get("values")[0][0])
            num2 = int(sheet.values().get(spreadsheetId=SPREADSHEETID,range=f'Sheet1!B{row}').execute().get("values")[0][0])
            print(f'{num1} + {num2} = {num1+num2}')

            sheet.values().update(spreadsheetId=SPREADSHEETID, range=f"Sheet1!C{row}",valueInputOption="USER_ENTERED", body={"values":[[f'{num1+num2}']]}).execute()
            sheet.values().update(spreadsheetId=SPREADSHEETID, range=f"Sheet1!D{row}",valueInputOption="USER_ENTERED", body={"values":[["DONE"]]}).execute()
            
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()
