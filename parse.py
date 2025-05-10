import json
from bs4 import BeautifulSoup

input_file = "ollama.com_library.html"
output_file = "models.json"

def extract_model_data(html_content):
    """
    Parses the HTML content and extracts model information.
    Adjust the selectors based on the actual HTML structure.
    """
    soup = BeautifulSoup(html_content, 'lxml')
    models_data = []

    # Updated selectors based on inspection of ollama.com_library.html
    # Each model is in an <li> tag with attribute x-test-model
    # Name is in the 'title' attribute of a <div x-test-model-title>
    # Description is in a <p class='max-w-lg break-words text-neutral-800 text-md'> within that div

    model_cards = soup.find_all('li', attrs={'x-test-model': True})

    for card in model_cards:
        name = "N/A"
        description = "N/A"
        tags = [] # Default to empty list for tags

        # Extract name
        name_container = card.find('div', attrs={'x-test-model-title': True})
        if name_container and name_container.has_attr('title'):
            name = name_container['title'].strip()

        # Extract description
        # The description <p> is a child of the name_container <div>
        if name_container:
            description_tag = name_container.find('p', class_='max-w-lg break-words text-neutral-800 text-md')
            if description_tag:
                description = description_tag.text.strip()

        # Tags are still using hypothetical selectors as their structure isn't clear
        # from the provided snippets for the main list.
        # This will likely result in an empty list for tags unless the old structure is coincidentally present.
        tags_container = card.find('div', class_='model-tags') # Original hypothetical selector
        if tags_container:
            tag_elements = tags_container.find_all('span', class_='tag') # Original hypothetical selector
            tags = [tag.text.strip() for tag in tag_elements]

        models_data.append({
            "name": name,
            "description": description,
            "tags": tags
        })
    return models_data

def main():
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found. Please create it or download the HTML content.")
        print("You can download it using: curl https://ollama.com/library -o ollama.com_library.html")
        return
    except Exception as e:
        print(f"Error reading file '{input_file}': {e}")
        return

    extracted_info = extract_model_data(html_content)

    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_info, f, indent=4)
        print(f"Successfully extracted data to '{output_file}'")
    except Exception as e:
        print(f"Error writing to JSON file '{output_file}': {e}")

if __name__ == "__main__":
    main()



