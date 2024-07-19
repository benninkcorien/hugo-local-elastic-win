import subprocess

# Run Elasticsearch
subprocess.Popen(
    [
        r"C:\Program Files\ConEmu\ConEmu64.exe",
        "/cmd",
        "cmd",
        "/k",
        r"C:\elasticsearch-8.14.3\bin\elasticsearch.bat",
    ]
)

# Open a second command line window and run node server.js
subprocess.Popen(
    [
        r"C:\Program Files\ConEmu\ConEmu64.exe",
        "/cmd",
        "cmd",
        "/k",
        "cd /d F:\\HugoBookSearchElastic\\static\\js && node server.js",
    ]
)

# Open a third command line window and run hugo server
subprocess.Popen(
    [
        r"C:\Program Files\ConEmu\ConEmu64.exe",
        "/cmd",
        "cmd",
        "/k",
        "cd /d F:\\HugoBookSearchElastic && hugo server",
    ]
)
