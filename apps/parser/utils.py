import re


def slugify_uri(uri: str) -> str:
    return re.sub(r'[./]', '-', uri).strip('-')
