from tools.search_tool import search_web

def research_topic(query):

    print("\nResearcher Agent Searching...\n")

    search_results = search_web(query)

    return search_results