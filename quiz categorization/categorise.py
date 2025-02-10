import pandas as pd
import PyPDF2
import torch
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer, util

# Download NLTK tokenizer
nltk.download('punkt')

# Load BERT model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Step 1: Extract Chapter Text from PDF
def extract_chapters_from_pdf(pdf_path):
    with open(pdf_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        text = [page.extract_text() for page in reader.pages if page.extract_text()]
    return text

# Load Laxmikanth PDF
pdf_path = "Indian_Polity_Laxmi-Kant-6th-Edition-.pdf"
chapters = extract_chapters_from_pdf(pdf_path)

# Step 2: Break Chapters into Paragraphs for Better Matching
all_paragraphs = []
chapter_mapping = []
for chapter_index, chapter in enumerate(chapters):
    paragraphs = sent_tokenize(chapter)  # Split into sentences
    for para in paragraphs:
        all_paragraphs.append(para)
        chapter_mapping.append(chapter_index)  # Map each paragraph to its chapter

# Step 3: Encode Paragraphs with BERT
paragraph_embeddings = model.encode(all_paragraphs, convert_to_tensor=True)

# Step 4: Load Questions from Google Sheets CSV
df = pd.read_csv("questions.csv")  # Export Google Sheets to CSV first

# Step 5: Find Closest Chapter for Each Question
def find_best_match(question):
    question_embedding = model.encode(question, convert_to_tensor=True)
    scores = util.pytorch_cos_sim(question_embedding, paragraph_embeddings)[0]
    
    # Get top 3 closest matches instead of just one
    top_matches = torch.topk(scores, 3)
    
    best_chapter_indices = [chapter_mapping[i.item()] for i in top_matches.indices]
    best_chapter_index = max(set(best_chapter_indices), key=best_chapter_indices.count)  # Most frequent among top 3

    return best_chapter_index

df["Predicted Chapter"] = df["Question"].apply(find_best_match)

# Step 6: Save Back to CSV (To Upload to Google Sheets)
df.to_csv("categorized_questions.csv", index=False)
print("✅ Categorization complete. Upload 'categorized_questions.csv' to Google Sheets.")
