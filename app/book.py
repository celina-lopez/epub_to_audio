from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
import re
from app.utils import create_temp_file, cleanup
from app.ai import get_quote_genders
MAX_OUTPUT = 4096  # characters


def slice_text(text):
    return [text[i:i + MAX_OUTPUT] for i in range(0, len(text), MAX_OUTPUT)]


def convert_epub_to_text(file):
    contents = file.read()
    file_name = create_temp_file('epub')
    tmp_file = open(file_name, 'wb')
    tmp_file.write(contents)
    tmp_file.close()
    text = read_epub(file_name)
    cleanup(file_name)
    return text


def chapter_to_text(chapter):
    soup = BeautifulSoup(chapter.get_body_content(), "html.parser")
    text = [para.get_text() for para in soup.find_all("p")]
    return " ".join(text)


def read_epub(file_name):
    libro = epub.read_epub(file_name)
    items = list(libro.get_items_of_type(ITEM_DOCUMENT))
    text = ""
    for item in items:
        text += chapter_to_text(item)
    return text


def get_quotes(text):
    quotations = re.findall(r'"([^"]*)"', text)
    return quotations


def parse_content_quotes(content):
    quotations = get_quotes(content)
    gendered_quotations = get_quote_genders(content, quotations)


def merge_gendered_quotations(quotes):
    return {
        'M': [quote[0] for quote in quotes if quote[1] == 'M'],
        'F': [quote[0] for quote in quotes if quote[1] == 'F'],
    }


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ['epub']
