import requests
from bs4 import BeautifulSoup
import gspread
import pandas as pd
import re
from google.oauth2.service_account import Credentials

# 🔹 STEP 1: Get Only Polity Section Links
def get_polity_section_links(main_url):
    response = requests.get(main_url)
    if response.status_code != 200:
        print("❌ Failed to fetch main page!")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    section_links = []

    for link in soup.find_all("a", href=True):
        title = link.get_text(strip=True)
        if "Polity" in title or "Indian Constitution" in title:  # Filters only Polity-related sections
            full_link = requests.compat.urljoin(main_url, link["href"])
            section_links.append((full_link, title))

    return section_links

# 🔹 STEP 2: Scrape Questions from Each Section
def scrape_questions(url, topic):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"❌ Failed to fetch {url}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    questions_data = []
    
    question_divs = soup.find_all("div", class_="form-control", id=lambda x: x and x.startswith("siteName"))
    answer_divs = soup.find_all("div", class_="form-control", id=lambda x: x and x.startswith("siteUrl"))

    for q_div, a_div in zip(question_divs, answer_divs):
        question_text = q_div.get_text(separator=" ").strip()

        # Extract options using regex
        options = re.findall(r"\([A-D]\) (.+?)(?=\s*\([A-D]\)|$)", question_text)
        
        # Extract correct answer and explanation
        answer_text = a_div.get_text(separator=" ").strip()
        correct_answer_match = re.search(r"Correct Answer:\s*\[(.*?)\]\s*(.+)", answer_text)
        explanation_match = re.search(r"Explanation:\s*(.+)", answer_text)

        correct_answer = correct_answer_match.group(2).strip() if correct_answer_match else ""
        explanation = explanation_match.group(1).strip() if explanation_match else ""

        # Extract year if available
        year_match = re.search(r'\[(.*?) (\d{4})\]', question_text)
        year = year_match.group(2) if year_match else ""

        # Default difficulty and topic
        difficulty = "Medium"
        
        # Ensure 4 options exist
        while len(options) < 4:
            options.append("")

        questions_data.append([question_text] + options + [correct_answer, year, difficulty, topic, explanation])

    return questions_data

# 🔹 STEP 3: Authenticate Google Sheets
def authenticate_google_sheets(sheet_url):
    creds = Credentials.from_service_account_file("credentials.json", scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
    client = gspread.authorize(creds)
    sheet = client.open_by_url(sheet_url).sheet1
    return sheet

# 🔹 STEP 4: Upload Data to Google Sheets
def upload_to_google_sheets(sheet, questions):
    headers = ["Question", "Option A", "Option B", "Option C", "Option D", "Correct Answer", "Year", "Difficulty", "Topic", "Explanation"]
    
    df = pd.DataFrame(questions, columns=headers)

    sheet.clear()
    sheet.append_row(headers)
    sheet.insert_rows(df.values.tolist(), 2)
    
    print(f"✅ Uploaded {len(questions)} questions to Google Sheets!")

# 🔹 STEP 5: Run Everything
if __name__ == "__main__":
    MAIN_URL = "https://www.studylikeapro.com/p/complete-mcqs-on-indian-constitution.html"
    SHEET_URL = "https://docs.google.com/spreadsheets/d/1wOlGx6t_wJs-PyhcWhX4ostwYzmSWl9dvnspGOT93f0/edit?usp=sharing"

    print("🔄 Fetching Polity section links...")
    sections = get_polity_section_links(MAIN_URL)

    all_questions = []
    for section_url, topic in sections:
        print(f"🔄 Scraping section: {topic} ({section_url})")
        section_questions = scrape_questions(section_url, topic)
        all_questions.extend(section_questions)

    print(f"📋 Extracted {len(all_questions)} total questions.")

    print("🔄 Connecting to Google Sheets...")
    sheet = authenticate_google_sheets(SHEET_URL)

    print("📤 Uploading data to Google Sheets...")
    upload_to_google_sheets(sheet, all_questions)

    print("🚀 Done! Check your Google Sheet.")
