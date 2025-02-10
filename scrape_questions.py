import requests
from bs4 import BeautifulSoup
import gspread
import pandas as pd
import re
from google.oauth2.service_account import Credentials

# 🔹 STEP 1: Scrape Questions from Website
def scrape_questions(url):
    response = requests.get(url)
    if response.status_code != 200:
        print("❌ Failed to fetch webpage!")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    questions_data = []
    
    all_questions = soup.find_all("strong")  # Extracts questions
    year_pattern = re.compile(r'\[(.*?) (\d{4})\]$')  # Detects [Exam 1992] format

    for i in range(len(all_questions)):
        question_text = all_questions[i].get_text().strip()
        year = ""

        # Extract year if present in [Exam Year] format
        year_match = year_pattern.search(question_text)
        if year_match:
            year = year_match.group(2)  # Extracts the year (e.g., 1992)
            question_text = year_pattern.sub("", question_text).strip()  # Removes [Exam 1992] from the question

        # Extract options, correct answer, and explanation
        options = []
        correct_answer = None
        explanation = None
        difficulty = "Medium"  # Default difficulty
        topic = "Indian Constitution"  # Default topic
        
        next_elements = all_questions[i].find_all_next("p", limit=5)  # Look for next 5 paragraphs
        for elem in next_elements:
            text = elem.get_text().strip()
            
            if text.startswith(("A.", "B.", "C.", "D.")):  # Option detection
                options.append(text[2:].strip())
            
            elif "Correct Answer:" in text:  # Detects correct answer
                correct_answer = text.split(":")[-1].strip()
            
            elif "Explanation:" in text:  # Detects explanation
                explanation = text.split(":", 1)[-1].strip()
                break  # Stop at first explanation

        # Ensure 4 options exist
        while len(options) < 4:
            options.append("")

        questions_data.append([question_text] + options + [correct_answer, year, difficulty, topic, explanation])

    return questions_data

# 🔹 STEP 2: Authenticate Google Sheets
def authenticate_google_sheets(sheet_url):
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet

# 🔹 STEP 3: Upload Data to Google Sheets
def upload_to_google_sheets(sheet, questions):
    headers = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer", "Year", "Difficulty", "Topic", "Explanation"]
    
    df = pd.DataFrame(questions, columns=headers)

    sheet.clear()
    sheet.append_row(headers)
    sheet.insert_rows(df.values.tolist(), 2)
    
    print(f"✅ Uploaded {len(questions)} questions to Google Sheets!")

# 🔹 STEP 4: Run Everything
if __name__ == "__main__":
    URL = "https://www.studylikeapro.com/p/complete-mcqs-on-indian-constitution.html"
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1wOlGx6t_wJs-PyhcWhX4ostwYzmSWl9dvnspGOT93f0/edit?usp=sharing"

    print("🔄 Scraping questions from website...")
    scraped_questions = scrape_questions(URL)

    print(f"📋 Extracted {len(scraped_questions)} questions.")

    print("🔄 Connecting to Google Sheets...")
    sheet = authenticate_google_sheets(SHEET_URL)

    print("📤 Uploading data to Google Sheets...")
    upload_to_google_sheets(sheet, scraped_questions)

    print("🚀 Done! Check your Google Sheet.")
