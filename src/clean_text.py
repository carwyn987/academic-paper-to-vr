from openai import OpenAI
from tqdm import tqdm
import os

def clean_page_content_map(text_dir: str, filename: str, page_content_map: dict[int,str], model: str) -> dict[int,str]:
    cleaned_page_content = dict()

    for page,content in tqdm(page_content_map.items(), desc=f"Generating cleaned content for {filename}"):
        
        if os.path.exists(os.path.join(text_dir, f"{filename}_{page}.txt")):
            with open(os.path.join(text_dir, f"{filename}_{page}.txt"), 'r') as f:
                cleaned_page_content[page] = f.read()
                print("Skipping text cleaning, already exists ...")
        else:
            cleaned_page_content[page] = clean_text(content, model)
            with open(os.path.join(text_dir, f"{filename}_{page}.txt"), 'w') as f:
                f.write(cleaned_page_content[page])

    return cleaned_page_content

def clean_text(text: str, model: str) -> str:

    client = OpenAI()

    """
    Will it be necessary to specify to remove any table and/or figure captions --> yes
    """
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "Do not give any context. \
             Do not reiterate the question, or ask for any follow up. \
             Only answer the prompts directly."},
            {
                "role": "user",
                "content": "Clean up the text below by removing errors, hanging \
                    numbers (such as page or figure numbers, header numbers, or section \
                    identifiers) that don't follow the sentence, and extraneous \
                    characters (like unnecessary slashes, dashes, or underscores). \
                    Convert algebraic expressions to text and ensure the content makes \
                    sense without adding new ideas. Remove in text links and citations. \
                    Remove any repeated or unnecessary headers or footers such as \
                    publication venue, and remove all tables and figures, as well as \
                    associated captions. Remove any weird characters, including list dots, \
                    etc. Return the updated text only, without adding extra content at \
                    the beginning or end. \n \
                    =============TEXT TO PROCESS BELOW================\n" + 
                    text
            }
        ]
    )

    return completion.choices[0].message.content