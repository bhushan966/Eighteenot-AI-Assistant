import os
import json
import requests
from dotenv import load_dotenv
from langchain_tavily import TavilySearch

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ─────────────────────────────────────────────
# SOURCE 1 — Wikipedia via direct requests
# (LangChain WikipediaWrapper has network issues)
# ─────────────────────────────────────────────
def fetch_wikipedia_data():
    print("📖 Fetching from Wikipedia (MediaWiki API)...")

    queries = [
        "Virat_Kohli",
        "List_of_international_cricket_centuries_by_Virat_Kohli",
    ]

    results = []
    headers = {
        "User-Agent": "KohliBot/1.0 (educational cricket chatbot project)",
        "Accept": "application/json",
    }

    for title in queries:
        try:
            url = (
                "https://en.wikipedia.org/w/api.php"
                f"?action=query&prop=extracts&explaintext=true"
                f"&titles={title}&format=json&exsectionformat=plain"
            )
            resp = requests.get(url, headers=headers, timeout=15)
            resp.raise_for_status()
            data = resp.json()
            pages = data.get("query", {}).get("pages", {})
            for page in pages.values():
                text = page.get("extract", "")
                if text:
                    results.append(f"### {title.replace('_', ' ')}\n{text}")
                    print(f"   ✅ '{title}' — {len(text):,} chars")
        except Exception as e:
            print(f"   ⚠️  Failed '{title}': {e}")

    full_text = "\n\n---\n\n".join(results)
    print(f"   📄 Wikipedia total: {len(full_text):,} characters\n")
    return full_text


# ─────────────────────────────────────────────
# SOURCE 2 — LangChain Tavily Search Tool
# ─────────────────────────────────────────────
def fetch_tavily_data():
    print("🔍 Fetching from Tavily using LangChain...")

    search = TavilySearch(
        max_results=5,
        tavily_api_key=TAVILY_API_KEY,
    )

    queries = [
        "Virat Kohli complete list of all ODI centuries venue opponent balls fours sixes",
        "Virat Kohli complete list of all Test centuries venue opponent balls fours sixes",
        "Virat Kohli first ODI century Bangladesh 2012 full scorecard details",
        "Virat Kohli latest match performance 2025 stats runs",
        "Virat Kohli all cricket records achievements milestones",
        "Virat Kohli ICC World Cup all editions performance stats runs centuries",
        "Virat Kohli IPL stats all seasons Royal Challengers Bangalore",
        "Virat Kohli T20 World Cup performances stats",
        "Virat Kohli vs Australia all matches batting stats centuries",
        "Virat Kohli highest scores top innings career all formats",
    ]

    results = []
    for query in queries:
        try:
            response = search.invoke(query)
            search_results = response.get("results", [])
            content_parts = []
            for item in search_results:
                title = item.get("title", "")
                url = item.get("url", "")
                content = item.get("content", "")
                if content:
                    content_parts.append(
                        f"Source: {title}\nURL: {url}\n{content}"
                    )
            combined = "\n\n".join(content_parts)
            results.append(f"### Query: {query}\n{combined}")
            print(f"   ✅ '{query[:55]}...' — {len(combined):,} chars")
        except Exception as e:
            print(f"   ⚠️  Failed '{query[:40]}': {e}")

    full_text = "\n\n---\n\n".join(results)
    print(f"   📄 Tavily total: {len(full_text):,} characters\n")
    return full_text


# ─────────────────────────────────────────────
# COMBINE & SAVE ALL DATA
# ─────────────────────────────────────────────
def fetch_all_data():
    print("\n🚀 Starting KohliBot data collection...\n")

    wiki_text = fetch_wikipedia_data()
    tavily_text = fetch_tavily_data()

    full_document = f"""
VIRAT KOHLI - COMPREHENSIVE CRICKET KNOWLEDGE BASE
Sources: Wikipedia MediaWiki API + LangChain Tavily Search
================================================================

SECTION 1 - WIKIPEDIA (Biography & Career Overview)
----------------------------------------------------------------
{wiki_text}

SECTION 2 - WEB SEARCH (Centuries, Records, Recent Matches)
----------------------------------------------------------------
{tavily_text}
"""

    os.makedirs("data", exist_ok=True)

    with open("data/kohli_document.txt", "w", encoding="utf-8") as f:
        f.write(full_document)

    print(f"✅ Data collection complete!")
    print(f"   📄 Total document: {len(full_document):,} characters")
    print(f"   📁 Saved to: data/kohli_document.txt")

    return full_document


if __name__ == "__main__":
    fetch_all_data()