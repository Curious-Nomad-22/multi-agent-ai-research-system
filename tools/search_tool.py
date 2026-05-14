from ddgs import DDGS

def search_web(query, max_results=5):

    results_list = []

    with DDGS() as ddgs:

        results = list(ddgs.text(query, max_results=max_results))

        for result in results:

            title = result.get("title", "No title")
            body = result.get("body", "No description")
            link = result.get("href", "No link")

            results_list.append({
                "title": title,
                "snippet": body,
                "link": link
            })

    return results_list