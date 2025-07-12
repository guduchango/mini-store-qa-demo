import os
import requests
import json
import logging

ollama_host = os.environ.get("OLLAMA_HOST", "localhost")
ollama_port = os.environ.get("OLLAMA_PORT", "11434")


def build_prompt_from_data(data):
    seller_tone = data.get("context", {}).get("seller_tone", "neutral")
    products = data.get("context", {}).get("products", [])
    client_query = data.get("client_query", "")

    product_lines = []
    for product in products:
        line = (
            f"- {product['name']} (Category: {product['category']}, "
            f"Size: {product['size']}, Color: {product['color']}, "
            f"Price: ${product['price']})\n  Description: {product['description']}"
        )
        product_lines.append(line)

    product_text = "\n\n".join(product_lines)

    prompt = (
        f"You are a helpful product assistant with a '{seller_tone}' tone.\n\n"
        f"Available products:\n\n{product_text}\n\n"
        f"Client asked: \"{client_query}\"\n\n"
        f"Respond in Spanish in a friendly and persuasive way."
    )

    return prompt

def generate_response(prompt):
    """Sends the prompt to Ollama and returns the generated response."""

    prompt = build_prompt_from_data(prompt)
    logging.info(f"🚀🚀🚀🚀 Prompt sent to Ollama:\n%s", {prompt})

    try:
        print("🚀 Sending prompt to Ollama...")
        ollama_response = requests.post(
            f"http://{ollama_host}:{ollama_port}/api/generate",
            json={"model": "deepseek-llm", "prompt": prompt},
            timeout=300,  # increase if you expect long responses
            stream=True   # key: enables streaming response
        )
        print(f"📡 Ollama HTTP Status: {ollama_response.status_code}")
        
        # This will raise an exception if Ollama returned an HTTP error
        ollama_response.raise_for_status()

        full_response = ""

        # Iterate over each JSON line emitted by Ollama
        for line in ollama_response.iter_lines(decode_unicode=True):
            if not line.strip():
                continue
            print(f"📥 RAW Ollama line: {line}")
            try:
                partial = json.loads(line)
                full_response += partial.get("response", "")
            except json.JSONDecodeError as e:
                print(f"⚠️ Error decoding JSON line: {e}")

        print(f"✅ Final response: {full_response}")
        return full_response.strip() or "An error occurred: empty response."

    except Exception as e:
        print(f"❌ Error calling Ollama: {e}")
        return "An error occurred while generating the response."
