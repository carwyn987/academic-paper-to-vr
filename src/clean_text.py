from openai import OpenAI

def clean_page_content_map(page_content_map: dict[int,str]) -> dict[int,str]:
    for key,value in page_content_map:
        page_content_map[key] = clean_text(value)

def clean_text(text: str) -> str:
    
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    )

    print(completion.choices[0].message)