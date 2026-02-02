import requests
from bs4 import BeautifulSoup
import sys


def extract_links_under_heading(url, heading_text):
    # Make request to the webpage
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return []

    # Parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all h3 elements
    h3_elements = soup.find_all("h3")

    target_h3 = None
    for h3 in h3_elements:
        if heading_text in h3.get_text():
            target_h3 = h3
            break

    if not target_h3:
        print(f"No h3 heading containing '{heading_text}' found")
        return []

    # Find the next ul element after the target h3
    ul_element = target_h3.find_next("ul")

    if not ul_element:
        print(f"No unordered list found after the h3 heading '{heading_text}'")
        return []

    # Extract all links from the ul element
    links = []
    for a_tag in ul_element.find_all("a"):
        href = a_tag.get("href")
        if href:
            links.append(href)

    return links


def main():
    if len(sys.argv) < 3:
        print('Usage: python script.py <url> "<heading_text>" [link_prefix]')
        print("  link_prefix: Optional prefix to add to each link")
        sys.exit(1)

    url = sys.argv[1]
    heading_text = sys.argv[2]

    # Check if a prefix was provided
    link_prefix = ""
    if len(sys.argv) >= 4:
        link_prefix = sys.argv[3]

    links = extract_links_under_heading(url, heading_text)

    # Add prefix to links if provided
    prefixed_links = [f"{link_prefix}{link}" for link in links]

    # Output links as newline-separated list
    if links:
        print("\n".join(prefixed_links))

        # Save to file
        with open("links.txt", "w") as f:
            f.write("\n".join(prefixed_links))
    else:
        print("No links found")


if __name__ == "__main__":
    main()
