import gspread # python library to interact with Google Sheets
from oauth2client.service_account import ServiceAccountCredentials # authenticate with a service account
 


class GoogleSheetSaver:
    def __init__(self, creds_file, sheet_name):
        # https://spreadsheets.google.com/feeds → Permission to read/write Google Sheets data.
        # https://www.googleapis.com/auth/drive → Permission to access Google Drive
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"] #defines permissions are needed (read/write Google Sheets + Drive). 

        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_file, scope) # load credentials from JSON key file
        client = gspread.authorize(creds) # authenticated Google Sheets client


        self.sheet = client.open(sheet_name).sheet1 # First sheet
    
    def ensure_headers(self):
        """Ensure the first row contains correct headers."""

        headers = ["Car Name", "City", "Price", "Year", "Mileage", "Fuel", "Engine", "Transmission"]
        first_row = self.sheet.row_values(1)

        if first_row != headers:  
            if first_row:  
                self.sheet.delete_row(1)  # remove wrong/old header
            self.sheet.insert_row(headers, 1)  # add correct header

    def save_cars(self, names, cities, prices, specs):
        """Save scraped car data into Google Sheet"""

        self.ensure_headers()
        rows = []
        for i in range(len(names)):
            row = [
                names[i] if i < len(names) else "",
                cities[i] if i < len(cities) else "",
                prices[i] if i < len(prices) else "",
                specs[i]["year"] if i < len(specs) else "",
                specs[i]["mileage"] if i < len(specs) else "",
                specs[i]["fuel"] if i < len(specs) else "",
                specs[i]["engine"] if i < len(specs) else "",
                specs[i]["transmission"] if i < len(specs) else "",
            ]
            rows.append(row)

        

        # insert all rows at once
        self.sheet.append_rows(rows)


       