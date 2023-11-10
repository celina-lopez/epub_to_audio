from ebooklib import epub, ITEM_DOCUMENT
from bs4 import BeautifulSoup
from utils import create_temp_file, cleanup

MAX_OUTPUT = 4096  # characters


def slice_text(text):
    return [text[i:i + MAX_OUTPUT] for i in range(0, len(text), MAX_OUTPUT)]


async def convert_epub_to_text(file):
    contents = await file.read()
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


def allowed_file(file_name):
    return '.' in file_name and \
           file_name.rsplit('.', 1)[1].lower() in ['epub']
