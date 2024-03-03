import gspread
from google.oauth2.service_account import Credentials


def authenticate():
    SCOPES = [
        "https://www.googleapis.com/auth/spreadsheets",
        # "https://www.googleapis.com/auth/drive",
    ]
    CRED_FILE = "service_account.json"
    creds = Credentials.from_service_account_file(CRED_FILE, scopes=SCOPES)
    return gspread.authorize(creds)
