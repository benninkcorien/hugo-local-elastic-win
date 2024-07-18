import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
import os
import datetime

# Variables
epub_path = r"D:\Dropbox (Personal)\Calibre\Calibre Leesboeken\D.D. Black\The Bones at Point No Point (A Thom (1893)\The Bones at Point No Point (A - D.D. Black.epub"
output_dir = r"F:\HugoBookSearch\pythonscripts\markdown"
categories = "[Mystery, Suspense, Thriller]"
# min_length = 100 #(skips too  many chapters)
# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the EPUB file
book = epub.read_epub(epub_path)
book_title = book.get_metadata("DC", "title")[0][0]
book_author = book.get_metadata("DC", "creator")[0][0]
today_date = datetime.date.today().strftime("%Y-%m-%d")


# Function to create frontmatter for markdown file
def create_frontmatter(chapter_number):
    return f"""---
author: ["{book_author}"]
title: "{book_title} - Chapter {chapter_number}"
date: "{today_date}"
description: "{book_author} - {book_title}"
tags: ["markdown", "syntax", "code", "gist"]
categories: {categories}
---

"""


def sanitize_filename(filename):
    return filename.replace(" ", "").replace("(", "").replace(")", "")


# Extract chapters and generate markdown files
chapter_number = 1
for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
    soup = BeautifulSoup(item.content, "html.parser")

    # Assuming chapters have <h1> tags
    if soup.find("h1"):
        chapter_content = soup.get_text().strip()

        # if len(chapter_content) < min_length:
        #     continue

        frontmatter = create_frontmatter(chapter_number)
        markdown_content = frontmatter + chapter_content

        # Sanitize and create the output filename
        sanitized_title = sanitize_filename(book_title)
        output_file = os.path.join(
            output_dir, f"{sanitized_title}-chapter-{chapter_number}.md"
        )
        with open(output_file, "w", encoding="utf-8") as md_file:
            md_file.write(markdown_content)

        chapter_number += 1

print(f"Markdown files have been generated in the {output_dir} directory.")
