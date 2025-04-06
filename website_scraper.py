import requests
from bs4 import BeautifulSoup
import validators


def get_website_data(url):
    # Validate URL
    if not validators.url(url):
        return {"error": "Invalid URL"}

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise error for bad responses
    except requests.exceptions.RequestException as e:
        return {"error": f"Request failed: {e}"}

    soup = BeautifulSoup(response.text, "html.parser")

    # Extract title & meta description
    title = soup.title.string if soup.title else "No title found"
    meta_desc = soup.find("meta", attrs={"name": "description"})
    meta_desc = meta_desc["content"] if meta_desc else "No description found"

    # Extract links and check for broken ones
    links = {a["href"] for a in soup.find_all("a", href=True)}
    broken_links = []

    for link in links:
        if not validators.url(link):  # Skip relative links
            continue
        try:
            link_response = requests.head(link, timeout=5)
            if link_response.status_code >= 400:
                broken_links.append(link)
        except requests.exceptions.RequestException:
            broken_links.append(link)

    # Extract images & check for missing alt text
    images = [
        {"src": img["src"], "alt": img.get("alt", "Missing alt text")}
        for img in soup.find_all("img", src=True)
    ]

    return {
        "title": title,
        "meta_description": meta_desc,
        "broken_links": broken_links,
        "images": images,
    }


# Example Usage
if __name__ == "__main__":
    url = input("Enter website URL: ")
    result = get_website_data(url)
    print(result)
