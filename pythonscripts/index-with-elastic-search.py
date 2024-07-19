import frontmatter
from elasticsearch import Elasticsearch, helpers
import os
import markdown

# Initialize Elasticsearch client with authentication
es = Elasticsearch(
    hosts=["http://localhost:9200"],
    basic_auth=("elastic", "ripx=UG=JxKPHnCzAlGA"),  # Replace with your actual password
)
clear_index = False

if clear_index and es.indices.exists(index="indexname"):
    es.indices.delete(index="indexname")
    print("Index 'indexname' cleared.")


def document_exists(es, index, id):
    try:
        es.get(index=index, id=id)
        return True
    except:
        return False


def get_data():
    indexname = []
    base_dir = "F:\\HugoBookSearchElastic\\content\\posts"

    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    post = frontmatter.loads(content)
                    book_content = markdown.markdown(post.content)
                    doc_id = os.path.splitext(os.path.basename(file_path))[0]
                    if not document_exists(es, "indexname", doc_id):
                        indexname.append(
                            {
                                "_index": "indexname",
                                "_id": doc_id,
                                "_source": {
                                    "title": post.get("title", "No Title"),
                                    "author": post.get("author", "Unknown Author"),
                                    "content": book_content,
                                    "url": post.get("url", "none"),
                                },
                            }
                        )
                        print(f"Prepared to index: {file_path}")
    return indexname


data = get_data()
print(f"Number of documents to index: {len(data)}")

if not es.indices.exists(index="indexname"):
    es.indices.create(index="indexname")
    print("Index 'indexname' created.")

helpers.bulk(es, data)
print("Data indexed successfully.")
