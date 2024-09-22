from openai import OpenAI
from tqdm import tqdm

def clean_page_content_map(filename: str, page_content_map: dict[int,str]) -> dict[int,str]:
    cleaned_page_content = dict()

    for page,content in tqdm(page_content_map.items(), desc=f"Generating cleaned content for {filename}"):
        cleaned_page_content[page] = clean_text(content)
        break

    return cleaned_page_content

def clean_text(text: str) -> str:

    client = OpenAI()

    """
    Will it be necessary to specify to remove any table and/or figure captions
    """
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a processor. You take input, follow \
             instructions, and give output. Do not give any context. Just do as is asked. \
             Do not reiterate the question, or ask for any follow up."},
            {
                "role": "user",
                "content": "Take the text below, and return it back to me after cleaning \
                            up any text errors. If there are hanging numbers, such as page \
                            or figure numbers, that do not follow the rest of the sentence, \
                            remove them. Remove any extraneous characters such as unnecessary \
                            slashes, dashes, underscores, etc. Clean up the text. Make sure \
                            that the content makes sense, but do not make up any ideas. Do \
                            not add any extra content at the beginning or end of your \
                            response, and only respond with the updated text." + \
                           "\n=============TEXT TO PROCESS BELOW================" + \
                           text
            }
        ]
    )

    return completion.choices[0].message.content