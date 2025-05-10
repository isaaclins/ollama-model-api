import json
import requests # Added for fetching HTML
from bs4 import BeautifulSoup

input_file = "ollama.com_library.html"
output_file = "models.json"
ollama_library_url = "https://ollama.com/library" # URL to fetch

def extract_model_data(html_content):
    """
    Parses the HTML content and extracts model information.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    models_data = []

    model_cards = soup.find_all('li', attrs={'x-test-model': True})

    # Define tags that should be moved to 'extras'
    special_case_tags = ["vision", "embedding", "tools"]

    for card in model_cards:
        name = "N/A"
        description = "N/A"
        raw_tags = []

        name_container = card.find('div', attrs={'x-test-model-title': True})
        if name_container and name_container.has_attr('title'):
            name = name_container['title'].strip()

        if name_container:
            description_tag = name_container.find('p', class_='max-w-lg break-words text-neutral-800 text-md')
            if description_tag:
                description = description_tag.text.strip()

        metadata_container = card.find('div', class_='flex flex-col space-y-2')
        if metadata_container:
            tags_div = metadata_container.find('div', class_='flex flex-wrap space-x-2')
            if tags_div:
                tag_elements = tags_div.find_all('span')
                for tag_span in tag_elements:
                    raw_tags.append(tag_span.text.strip().lower()) # Convert to lower for consistent matching

        final_tags = []
        extras_list = []
        for t in raw_tags:
            if t in special_case_tags:
                extras_list.append(t)
            else:
                final_tags.append(t)

        models_data.append({
            "name": name,
            "description": description,
            "tags": final_tags,
            "extras": extras_list
        })
    return models_data

def main():
    html_content = None
    try:
        print(f"Attempting to download HTML from {ollama_library_url}...")
        response = requests.get(ollama_library_url, timeout=10)
        response.raise_for_status()
        # Use apparent_encoding for robustness, then fallback to utf-8 if needed
        response.encoding = response.apparent_encoding 
        html_content = response.text
        print("Successfully downloaded HTML content.")
        try:
            with open(input_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Saved downloaded HTML to '{input_file}'")
        except Exception as e:
            print(f"Warning: Could not save HTML to '{input_file}': {e}")

    except requests.exceptions.RequestException as e:
        print(f"Error downloading HTML: {e}")
        print(f"Attempting to use local file '{input_file}' as a fallback.")
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                html_content = f.read()
            print(f"Successfully read HTML from local file '{input_file}'.")
        except FileNotFoundError:
            print(f"Error: Local input file '{input_file}' not found. Please create it or ensure internet connectivity.")
            print(f"You can manually download it using: curl {ollama_library_url} -o {input_file}")
            return
        except Exception as e_read:
            print(f"Error reading local file '{input_file}': {e_read}")
            return
    
    if not html_content:
        print("Error: No HTML content available to parse.")
        return

    extracted_info = extract_model_data(html_content)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_info, f, indent=4, ensure_ascii=False) # Added ensure_ascii=False
        print(f"Successfully extracted data to '{output_file}'")
    except Exception as e:
        print(f"Error writing to JSON file '{output_file}': {e}")

if __name__ == "__main__":
    main()



