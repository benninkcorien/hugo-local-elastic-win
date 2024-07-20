import subprocess

# ! Change everything into the correct paths below

# Run Elasticsearch -- Change this to your ElasticSearch location
subprocess.Popen(
    [
        "cmd",
        "/k",
        r"C:\elasticsearch-8.14.3\bin\elasticsearch.bat",
    ]
)

# Open a second command line window and run node server.js
subprocess.Popen(
    [
        "cmd",
        "/k",
        "cd /d F:\\HugoBookSearchElasticGithub\\static\\js && node server.js",
    ]
)

# Open a third command line window and run hugo server
subprocess.Popen(
    [
        "cmd",
        "/k",
        "cd /d F:\\HugoBookSearchElasticGithub && hugo server",
    ]
)
