# ollama-model-api

This project provides a GitHub workflow that automatically fetches model information from [https://ollama.com/library](https://ollama.com/library), parses it, and makes it available as a structured JSON file. The live JSON output is hosted on GitHub Pages.

**Live Model Data:** [https://isaaclins.com/ollama-model-api/models.json](https://isaaclins.com/ollama-model-api/models.json)

## Output JSON Structure

The output JSON file (`models.json`) contains an array of model objects, each with the following fields:

- `name`: The model's name (e.g., "gemma3").
- `description`: A short description of the model.
- `tags`: An array of tags primarily representing model sizes (e.g., "7b", "27b").
- `extras`: An array of other relevant tags, such as capabilities (e.g., "vision", "tools", "embedding").

### Example

```json
    {
        "name": "gemma3",
        "description": "The current, most capable model that runs on a single GPU.",
        "tags": [
            "1b",
            "4b",
            "12b",
            "27b"
        ],
        "extras": [
            "vision"
        ]
    },
    {
        "name": "qwen3",
        "description": "Qwen3 is the latest generation of large language models in Qwen series, offering a comprehensive suite of dense and mixture-of-experts (MoE) models.",
        "tags": [
            "0.6b",
            "1.7b",
            "4b",
            "8b",
            "14b",
            "30b",
            "32b",
            "235b"
        ],
        "extras": [
            "tools"
        ]
    },
    {
        "name": "deepseek-r1",
        "description": "DeepSeek's first-generation of reasoning models with comparable performance to OpenAI-o1, including six dense models distilled from DeepSeek-R1 based on Llama and Qwen.",
        "tags": [
            "1.5b",
            "7b",
            "8b",
            "14b",
            "32b",
            "70b",
            "671b"
        ],
        "extras": []
    },
```



## How it works

A GitHub Actions workflow (`.github/workflows/deploy_models.yml`) orchestrates the process:

1.  **Scheduled & Manual Trigger**: The workflow runs automatically on a daily schedule, on pushes to the main branch, and can also be triggered manually.
2.  **Environment Setup**: It sets up a Python environment and installs necessary dependencies (`BeautifulSoup4`, `requests`, `lxml`) listed in `requirements.txt`.
3.  **Data Fetching & Parsing**: The Python script (`parse.py`) is executed:
    - It downloads the latest HTML content from [https://ollama.com/library](https://ollama.com/library).
    - Using `BeautifulSoup` with the `lxml` parser, it extracts model information (name, description, and various tags).
    - The extracted tags are categorized: size-related tags (ending in 'b') are placed in the `"tags"` field, while specific capability tags ("vision", "embedding", "tools") are moved to the `"extras"` field.
    - The processed data is saved as `models.json`.
4.  **Deployment to GitHub Pages**: The workflow uploads the generated `models.json` as an artifact and deploys it to GitHub Pages, making it publicly accessible via the link mentioned above.

The script can also be run locally for development and testing, and it will attempt to use a local `ollama.com_library.html` file if the direct download fails.
