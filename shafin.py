import gspread
from oauth2client.service_account import ServiceAccountCredentials


scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets"]

# Add your service account key file
creds = ServiceAccountCredentials.from_json_keyfile_name('black-media-386619-0e541c4ee39e.json', scope)

# Authorize the client
client = gspread.authorize(creds)

# Open the spreadsheet by its URL with the 'gid' parameter
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1bOPtxYV2xsDtBWfj8EhQniRMEafk6mBUr_DoD9et5is/edit?gid=152194846#gid=152194846'
spreadsheet = client.open_by_url(spreadsheet_url)

# Select the specific worksheet by ID (you can use the index if you want to access other sheets)
worksheet = spreadsheet.get_worksheet_by_id(152194846)  # This ensures the correct sheet is selected

# Get all values
data = worksheet.get_all_values()

# Print the data
for row in data:
    print(row)
