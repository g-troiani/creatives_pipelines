import requests

# User Input
user_curated_input = input("What are you looking for?")

def google_search(query, api_key, cse_id, num_results=10):
    """
    Function to perform a Google search using the Custom Search JSON API.

    Parameters:
    - query: The search query string.
    - api_key: The API key for accessing the Google Custom Search API.
    - cse_id: The custom search engine ID.
    - num_results: Number of search results to retrieve (default is 10).

    Returns:
    - A dictionary containing the search results in JSON format.
    """
    url = f"https://www.googleapis.com/customsearch/v1"  # API endpoint
    params = {
        'q': query,      # Search query
        'key': api_key,  # API key
        'cx': cse_id,    # Custom search engine ID
        'num': num_results,  # Number of results to retrieve
    }
    response = requests.get(url, params=params)  # Make the API request
    return response.json()  # Return the response in JSON format


def main():
    """
    Main function to perform a Google search for "AI topics" and print the results.
    """
    query =   user_curated_input
    api_key = "AIzaSyDVKT5fLzWzfvrRs4dlt_JOTaJ6CZou3sM"  # Replace with your actual API key
    cse_id = "f49c715abb2594dd5"    # Replace with your actual custom search engine ID
    
    results = google_search(query, api_key, cse_id)  # Perform the search
    
    # Loop through the search results and print the title, snippet, and link
    for item in results.get('items', []):
        print(f"Title: {item['title']}")       # Print the title of the search result
        print(f"Snippet: {item['snippet']}")   # Print the snippet of the search result
        print(f"Link: {item['link']}\n")       # Print the link of the search result


results


if __name__ == "__main__":
    main()
