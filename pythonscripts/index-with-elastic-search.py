import os
import frontmatter
from elasticsearch import Elasticsearch, helpers
import markdown

# Initialize Elasticsearch client with authentication
es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "ripx=UG=JxKPHnCzAlGA"),  # Replace with your actual password
)


def get_data():
    books = []
    base_dir = "F:\\HugoBookSearchElastic\\content\\posts"

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    post = frontmatter.loads(
                        content
                    )  # Correct usage of frontmatter library with string
                    book_content = markdown.markdown(post.content)
                    books.append(
                        {
                            "_index": "books",
                            "_source": {
                                "title": post.get("title", "No Title"),
                                "author": post.get("author", "Unknown Author"),
                                "content": book_content,
                                "permalink": file_path,
                            },
                        }
                    )
                    print(
                        f"Prepared to index: {file_path}"
                    )  # Log each file being prepared for indexing
    return books


data = get_data()
print(f"Number of documents to index: {len(data)}")

# Attempt to create the index before indexing data
if not es.indices.exists(index="books"):
    es.indices.create(index="books")
    print("Index 'books' created.")

helpers.bulk(es, data)
print("Data indexed successfully.")
