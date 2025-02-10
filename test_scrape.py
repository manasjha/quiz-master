import requests
from bs4 import BeautifulSoup

URL = "https://www.studylikeapro.com/p/complete-mcqs-on-indian-constitution.html"

print("🔄 Fetching webpage...")
response = requests.get(URL)

if response.status_code != 200:
    print("❌ Failed to fetch webpage!")
else:
    print("✅ Page loaded successfully!")
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Print first 1000 characters of the page to check structure
    print(soup.prettify()[:1000])
