import requests
from bs4 import BeautifulSoup
import json
import sys
import os
import re


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
        # Try looking for ul with class "listLinks" as well
        list_container = soup.find("ul", class_="listLinks")

    if not list_container:
        print(f"No element with class 'listLinks' found at {url}")
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


def sanitize_filename(url):
    # Remove protocol
    url = re.sub(r"^https?://", "", url)
    # Replace characters that are not allowed in filenames
    url = re.sub(r'[\\/*?:"<>|]', "_", url)
    # Replace additional characters that might cause issues
    url = re.sub(r"[&=+,\s]", "_", url)
    # Limit length to avoid exceeding filename length restrictions
    if len(url) > 100:
        url = url[:100]
    return url + ".json"


def process_links_file(file_path):
    # Create faqs directory if it doesn't exist
    faqs_dir = "faqs"
    os.makedirs(faqs_dir, exist_ok=True)

    # Read the links file
    try:
        with open(file_path, "r") as f:
            links = f.read().splitlines()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return

    if not links:
        print("No links found in the file")
        return

    # Process each link
    for i, link in enumerate(links):
        if not link.strip():
            continue

        print(f"Processing link {i + 1}/{len(links)}: {link}")

        # Extract Q&A pairs
        qa_pairs = extract_qa_pairs(link)

        if not qa_pairs:
            print(f"  No Q&A pairs found at {link}")
            continue

        # Generate filename
        filename = sanitize_filename(link)
        file_path = os.path.join(faqs_dir, filename)

        # Save to file
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(qa_pairs, f, indent=2, ensure_ascii=False)
            print(f"  Extracted {len(qa_pairs)} Q&A pairs and saved to {file_path}")
        except Exception as e:
            print(f"  Error saving to {file_path}: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <links_file>")
        print("  links_file: File containing newline-separated URLs")
        sys.exit(1)

    links_file = sys.argv[1]
    process_links_file(links_file)

    print("\nAll links processed. Results saved in the 'faqs' directory.")


if __name__ == "__main__":
    main()
