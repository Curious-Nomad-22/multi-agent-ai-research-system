from groq import Groq
from memory.save_memory import save_to_memory
from memory.retrieve_memory import retrieve_relevant_memory
from agents.planner import create_plan
from agents.researcher import research_topic
from agents.writer import format_report
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

query = input("What do you want to research? ")
# STEP 1 — Planning
plan = create_plan(query)
print(plan)
# STEP 2 — Research
research_data = research_topic(query)

formatted_research = ""

for item in research_data:

    title = item.get("title", "No Title")
    snippet = item.get("snippet", "No Snippet")
    link = item.get("link", "No Link")

    formatted_research += f"""
RESULT

Title: {title}

Snippet: {snippet}

Source: {link}

------------------------
"""

memory_data = retrieve_relevant_memory(query)

save_to_memory(research_data)


# STEP 3 — Build Prompt
prompt = f"""
You are an AI startup research analyst.

Generate a SIMPLE and CLEAN research report.

TOPIC:
{query}

RESEARCH PLAN:
{plan}

RESEARCH FINDINGS:
{formatted_research}

====================================

STRICT FORMAT:

# PLANNER
Show the research plan using bullet points.

# COMPANIES

For EACH company provide:

## Company Name

- Focus Area
- Why It Matters
- Growth Signal
- Website
- Source

# MARKET INSIGHTS

Write 2-3 concise lines.

# CONFIDENCE SCORE

Give a score out of 10.

# SOURCES

List all source links.

====================================

IMPORTANT:

- Keep output CLEAN
- Keep output SHORT
- Use bullet points
- DO NOT generate huge paragraphs
- Include links whenever available
- Make it readable like a research dashboard
"""

# Reduce prompt size
formatted_research = formatted_research[:2500]

# STEP 4 — LLM Analysis
response = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ],
    model="llama-3.3-70b-versatile"
)

final_report = response.choices[0].message.content

# STEP 5 — Writer Agent
formatted_output = format_report(final_report)

print(formatted_output)