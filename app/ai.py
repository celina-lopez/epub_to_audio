import openai
import os
from dotenv import load_dotenv
import os
import json

load_dotenv(dotenv_path='.env')
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_quote_genders(content, quotations):
    messages = [
        {"role": "system",
            "content": """
            You are trying to find out the gender of each quote from the text. I will first list the quotes.
            Please put the format as follows:
            [["quote1", "F"], ["quote2", "M"], ["quote3", "M"]]
          """,
         },
        {"role": "user",
            "content": """
            Here are the quote: {}
            Here is the content: {}
            """.format(quotations, content)},
    ]
    response = client.chat.completions.create(
        model='gpt-3.5-turbo', messages=messages)
    return json.loads(response.choices[0].message.content)
