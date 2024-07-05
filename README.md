# Translator API

This is a Translator API that utilizes the LLM3 model to provide language translation and spelling correction capabilities. The API is built using FastAPI in Python.

## Features

- Language Translation: The API allows you to translate text from one language to another using the powerful LLM3 model.
- Spelling Correction: It also provides the ability to correct spelling errors in the input text.

## Usage

To use the Translator API, you need to send a POST request to the appropriate endpoint with the following parameters:

- `text`: The text that you want to translate or correct.
- `source_language`: The language of the input text. (optional)
- `target_language`: The language to which you want to translate the text. (optional)

Example Request:

```python
import requests

url = "http://translator-api.com/translate"

payload = {
    "text": "Hello, how are you?",
    "source_language": "en",
    "target_language": "fr"
}

response = requests.post(url, json=payload)

print(response.json())
```

Example Response:

```json
{
    "translated_text": "Bonjour, comment ça va?"
}
```

## Installation

To install and run the Translator API locally, follow these steps:

1. Clone the repository:

```bash
git clone https://github.com/your-username/translator-api.git
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Start the API server:

```bash
uvicorn main:app --reload
```

The API will be accessible at `http://localhost:8000`.

## Contributing

Contributions are welcome! If you have any suggestions or improvements, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.
