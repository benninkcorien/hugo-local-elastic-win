import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import datetime
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter

# Download necessary NLTK data files
nltk.download("punkt")
nltk.download("stopwords")
nltk.download("wordnet")

# Variables
shortauthor = "dickfrancis"
epub_path = r"D:\Dropbox (Personal)\Calibre\Calibre Leesboeken\Dick Francis\Straight (1498)\Straight - Dick Francis.epub"
output_dir = rf"F:\HugoBookSearchElastic\content\posts\{shortauthor}"
categories = "[Mystery, Suspense, Adult]"

lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words("english"))

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the EPUB file
book = epub.read_epub(epub_path)
book_title = book.get_metadata("DC", "title")[0][0]
book_author = book.get_metadata("DC", "creator")[0][0]
today_date = datetime.date.today().strftime("%Y-%m-%d")
min_length = 200


# Function to create frontmatter for markdown file
def create_frontmatter(document_title, tags, theurl):
    tags_str = ", ".join([f'"{tag}"' for tag, _ in tags])
    return f"""---
author: ["{book_author}"]
title: "{book_title} - {document_title}"
date: "{today_date}"
description: "{book_author} - {book_title}"
tags: [{tags_str}]
categories: {categories}
url: {theurl}
---

"""


# Function to sanitize filenames
def sanitize_filename(filename):
    return re.sub(r'[\\/*?:"<>|]', "", filename)


# Function to get the top words from text
def get_top_words(text, top_n=25):
    tokens = word_tokenize(text)
    lemmatized_tokens = [
        lemmatizer.lemmatize(token.lower())
        for token in tokens
        if token.isalpha() and token.lower() not in stop_words
    ]
    word_freq = Counter(lemmatized_tokens)
    return word_freq.most_common(top_n)


# Function to generate URL
def generate_url(shortauthor, sanitized_title, document_title):
    sanitized_document_title = sanitize_filename(
        document_title.replace(" ", "-").lower()
    )
    return f"/{shortauthor}/{sanitized_title}-{sanitized_document_title}"


# Generate markdown files for each document item in the EPUB
print("Available document items in the EPUB:")
for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    item_name = item.get_name()
    print(item_name)

    document_title = os.path.basename(item_name)

    # Extract text content
    soup = BeautifulSoup(item.content, "html.parser")
    document_content = soup.get_text()

    # Skip if content is less than 200 characters
    if len(document_content) < min_length:
        continue

    # Remove multiple blank lines
    document_content = re.sub(r"\n\s*\n", "\n", document_content)
    top_words = get_top_words(document_content)

    # Sanitize and create the output filename
    sanitized_title = sanitize_filename(book_title)
    theurl = generate_url(shortauthor, sanitized_title, document_title)
    frontmatter = create_frontmatter(document_title, top_words, theurl)
    markdown_content = frontmatter + document_content
    output_file = os.path.join(
        output_dir, f"{sanitized_title}-{sanitize_filename(document_title)}.md"
    )

    with open(output_file, "w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

print(f"Markdown files have been generated in the {output_dir} directory.")
