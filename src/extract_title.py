

def extract_title(markdown):
    if "#" not in markdown:
        raise Exception("No title symbol in markdown file")
    return markdown.split("#")[1].strip()