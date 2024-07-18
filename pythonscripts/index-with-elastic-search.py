from elasticsearch import Elasticsearch, helpers
import glob
import os
import markdown
import frontmatter

# Initialize Elasticsearch client with authentication
es = Elasticsearch(
    hosts=["http://localhost:9200"],
    http_auth=(
        "elastic",
        "ripx=UG=JxKPHnCzAlGA",
    ),
)


def get_data():
    books = []
    for file in glob.glob("content/books/**/*.md", recursive=True):
        with open(file, "r", encoding="utf-8") as f:
            content = f.read()
            md = frontmatter.loads(content)
            book_content = markdown.markdown(md.content)
            books.append(
                {
                    "_index": "books",
                    "_source": {
                        "title": md.get("title", "No Title"),
                        "author": md.get("author", "Unknown Author"),
                        "content": book_content,
                        "summary": md.get("description", ""),
                        "permalink": file,
                    },
                }
            )
    return books


data = get_data()
helpers.bulk(es, data)
print("Data indexed successfully.")
