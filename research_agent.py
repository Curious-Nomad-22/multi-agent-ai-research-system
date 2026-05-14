from groq import Groq
from agents.researcher import search_web
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
query = input("What do you want to research? ")
search_data = search_web(query)
print("\nSEARCH DATA PREVIEW:\n")
print(search_data[:1000])

prompt = f"""
You are a professional AI startup research analyst.

Generate a CLEAN structured report.

TOPIC:
{query}

SEARCH DATA:
{search_data}

IMPORTANT RULES:

1. Use EXACT headings.
2. Include website links.
3. Include source links.
4. Do NOT skip sections.
5. Keep the format clean.

USE THIS EXACT FORMAT:


# COMPANIES

## Company Name

FOCUS AREA:
...

WHY IT MATTERS:
...

GROWTH SIGNAL:
...

WEBSITE:
https://...

SOURCE:
https://...


## Another Company

FOCUS AREA:
...

WHY IT MATTERS:
...

GROWTH SIGNAL:
...

WEBSITE:
https://...

SOURCE:
https://...


# MARKET INSIGHTS

- Insight 1
- Insight 2
- Insight 3


# CONFIDENCE SCORE

8/10


# SOURCES

https://...

https://...
"""
print("\nPROMPT PREVIEW:\n")
print(prompt[:1500])

print("\nSending the data to LLM...\n")
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="llama-3.3-70b-versatile"
)
print("\nFINAL RESEARCH REPORT:\n")
print(response.choices[0].message.content)
print("\nResearch completed successfully.")