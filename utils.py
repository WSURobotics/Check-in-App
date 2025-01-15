
def extract_id(text: str) -> str:
    index = text.find("11")
    if index == -1:
        return ""
    return text[index:index + 8]