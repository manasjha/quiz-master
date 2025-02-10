import gspread
from google.oauth2.service_account import Credentials

# Google Sheets API setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
CREDS = Credentials.from_service_account_file("credentials.json", scopes=SCOPE)
client = gspread.authorize(CREDS)

# Open the Google Sheet
SHEET_ID = "1wOlGx6t_wJs-PyhcWhX4ostwYzmSWl9dvnspGOT93f0"  # Replace with your actual Google Sheets ID
SHEET_NAME = "Sheet1"  # Change if your sheet has a different name
sheet = client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

def count_questions_without_answers():
    """Count how many questions do not have an answer (Column F is empty)."""
    data = sheet.get_all_values()  # Get all rows from the sheet
    total_questions = 0
    questions_without_answer = 0

    for i, row in enumerate(data[1:412]):  # Skip header and stop at row 412
        if row[0].strip():  # Column A (Question) is not empty
            total_questions += 1
            if len(row) < 6 or not row[5].strip():  # Column F (Answer) is empty
                questions_without_answer += 1

    return {
        "Total Questions": total_questions,
        "Questions Without Answer": questions_without_answer
    }

if __name__ == "__main__":
    result = count_questions_without_answers()
    print(f"Total Questions: {result['Total Questions']}")
    print(f"Questions Without Answer: {result['Questions Without Answer']}")
