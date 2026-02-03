import re
from langchain_community.document_loaders import PyPDFLoader

def load_resume(path):
    loader = PyPDFLoader(path)
    return loader.load()

def sanitize_text(text):
    patterns = [
        r"name\s*:.*",
        r"gender\s*:.*",
        r"age\s*:.*",
        r"address\s*:.*",
        r"college\s*:.*"
    ]
    for p in patterns:
        text = re.sub(p, "", text, flags=re.I)
    return text
