# ollama-model-api

This project provides a GitHub workflow that fetches the plain HTML from [https://ollama.com/library](https://ollama.com/library), parses the available model information, and outputs a JSON file containing the following fields for each model:

- `name`: The model's name (e.g., "gemma3").
- `description`: A short description of the model.
- `tags`: An array of tags (such as model sizes or features).

## How it works

A Python script is used to:

1. Download the HTML from the Ollama library page (or use a local HTML file for testing).
2. Parse the HTML to extract model names, descriptions, and tags.
3. Output the results as a JSON file.

This script is intended to be run in a GitHub Actions workflow, but can also be run locally for development and testing.
