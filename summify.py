import os
import openai
import time
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("API_KEY")
MODEL = "gpt-3.5-turbo"

with open('input.txt', encoding='utf-8') as f:
    text = f.read()

with open('output.txt', 'w') as f:
    f.write('')

LIMIT = 3750*4  # maximum length of text to process at a time
start = 0

while start < len(text):
    end = start + LIMIT
    if end >= len(text):
        end = len(text)
    else:
        # find the last period within the range
        last_period = text.rfind('.', start, end)
        if last_period != -1:
            end = last_period + 1  # include the period in the extracted text

    # extract the text
    chunk = text[start:end]

    try:
        #Make your OpenAI API request here
        response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Summarize the given transcript in the form of points. Try to retain maximum amount of information and give a lot of points. Response must be in points :\n\n"+chunk },
        ],
        temperature=0,
        max_tokens=380
        )

        print(response)

    except openai.error.APIError as e:
        #Handle API error here, e.g. retry or log
        print(f"OpenAI API returned an API Error: {e}")
        pass
    except openai.error.APIConnectionError as e:
        #Handle connection error here
        print(f"Failed to connect to OpenAI API: {e}")
        pass
    except openai.error.RateLimitError as e:
        #Handle rate limit error (we recommend using exponential backoff)
        print(f"OpenAI API request exceeded rate limit: {e}")
        pass
    

    with open("output.txt", "a") as f:
            f.write(response['choices'][0]['message']['content'])
            f.write("\n\n")

    print("Done!!!")
    time.sleep(17)

    start = end
