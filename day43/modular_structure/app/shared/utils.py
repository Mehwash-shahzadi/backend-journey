# app/shared/utils.py
def slugify(text: str) -> str:
    return text.lower().replace(" ", "-")