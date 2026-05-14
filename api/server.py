from fastapi import FastAPI
from groq import Groq

from agents.planner import create_plan
from agents.researcher import research_topic
from agents.writer import format_report

from memory.save_memory import save_to_memory
from memory.retrieve_memory import retrieve_relevant_memory
from dotenv import load_dotenv
import os

load_dotenv()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
app = FastAPI()


@app.get("/research")
def research(query: str):

    # STEP 1 — Planning
    plan = create_plan(query)

    # STEP 2 — Research
    research_data = research_topic(query)

    formatted_research = ""

    for item in research_data:

        title = item.get("title", "No Title")
        snippet = item.get("snippet", "No Snippet")
        link = item.get("link", "No Link")

        formatted_research += f"""
Title: {title}

Snippet: {snippet}

Source: {link}

------------------------
"""

    # Reduce token usage
    formatted_research = formatted_research[:2500]

    # STEP 3 — Memory
    memory_data = retrieve_relevant_memory(query)

    save_to_memory(research_data)

    # STEP 4 — Prompt
    prompt = f"""
You are an AI startup research analyst.

Generate a SIMPLE and CLEAN research report.

TOPIC:
{query}

RESEARCH PLAN:
{plan}

RESEARCH FINDINGS:
{formatted_research}

MEMORY:
{memory_data}

STRICT FORMAT:

Return ONLY valid markdown.

Use EXACT structure below.

# PLANNER

- Bullet point
- Bullet point

# COMPANIES

## Company Name

- **Focus Area:** value

- **Why It Matters:** value

- **Growth Signal:** value

- **Website:** value

- **Source:** value

---

## Company Name

- **Focus Area:** value

- **Why It Matters:** value

- **Growth Signal:** value

- **Website:** value

- **Source:** value

---

# MARKET INSIGHTS

Write 2 concise lines.

# CONFIDENCE SCORE

8/10

# SOURCES

- source link
- source link

IMPORTANT:
- Use proper markdown spacing
- Leave empty line between sections
- Never write everything in one line
- Never merge labels together
- Keep formatting clean
- If official website is unavailable, use source URL
"""

    # STEP 5 — LLM Analysis
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

    formatted_output = format_report(final_report)

    # Clean markdown spacing
    formatted_output = formatted_output.replace("\n\n\n", "\n\n")
    formatted_output = formatted_output.strip()

    return {
        "plan": f"## PLANNER\n\n{plan}",
        "report": formatted_output
}
