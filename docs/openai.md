Text generation

Copy page
Learn how to generate text from a prompt.
OpenAI provides simple APIs to use a large language model to generate text from a prompt, as you might using ChatGPT. These models have been trained on vast quantities of data to understand multimedia inputs and natural language instructions. From these prompts, models can generate almost any kind of text response, like code, mathematical equations, structured JSON data, or human-like prose.

Quickstart
To generate text, you can use the chat completions endpoint in the REST API, as seen in the examples below. You can either use the REST API from the HTTP client of your choice, or use one of OpenAI's official SDKs for your preferred programming language.

Create a human-like response to a prompt

curl "https://api.openai.com/v1/chat/completions" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer $OPENAI_API_KEY" \
    -d '{
        "model": "gpt-4o",
        "messages": [
            {
                "role": "developer",
                "content": "You are a helpful assistant."
            },
            {
                "role": "user",
                "content": "Write a haiku about recursion in programming."
            }
        ]
    }'
