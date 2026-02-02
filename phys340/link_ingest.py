import requests
from bs4 import BeautifulSoup
import json
import sys


def extract_qa_pairs(url):
    # Make request to the webpage
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find the container with class "listLinks"
    list_container = soup.find("ol", class_="listLinks")

    if not list_container:
        print("No element with class 'listLinks' found")
        return []

    # Find all li elements in the container
    li_elements = list_container.find_all("li")

    qa_pairs = []

    # Extract Q and A from each li element
    for li in li_elements:
        strong_tag = li.find("strong")
        p_tag = li.find("p")

        if strong_tag and p_tag:
            question = strong_tag.get_text(strip=True)
            answer = p_tag.get_text(strip=True)

            qa_pairs.append({"Q": question, "A": answer})

    return qa_pairs


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    qa_pairs = extract_qa_pairs(url)

    # Output JSON
    print(json.dumps(qa_pairs, indent=2))

    # Optionally save to file
    with open("qa_pairs.json", "w") as f:
        json.dump(qa_pairs, indent=2, fp=f)


if __name__ == "__main__":
    main()
