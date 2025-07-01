from google import genai
import json
client = genai.Client()  # reads GEMINI_API_KEY


def load_filtered_products(path):
    selected = []
    with open(path) as f:
        for line in f:
            prod = json.loads(line)
            selected.append(prod)
    return selected


def build_prompt(products, user_query):
    lines = []
    for p in products:
        line = (
            f"ASIN: {p.get('parent_asin', 'N/A')}\n"
            f"Title: {p.get('title', 'No Title')}\n"
            f"Description: {p.get('description', 'No Description')}\n"
            f"Store Info: {p.get('store', 'N/A')}\n"
            f"Category: {p.get('main_category', 'N/A')}\n"
            f"Price: ${p.get('price', 'N/A')}\n"
            f"Average Rating: {p.get('average_rating', 'N/A')} "
            f"(Based on {p.get('rating_number', 'N/A')} ratings)\n"
            f"Details: {p.get('details', 'N/A')}\n"
            "-------------------------"
        )
        lines.append(line)

    context = "\n".join(lines)
    return f"You are a product expert. Below are some product listings:\n\n{context}\n\nUser asked: {user_query}\nAnswer:"


def ask_gemini(prompt):
    from google import genai
    client = genai.Client()
    resp = client.models.generate_content(
        model="gemini-2.5-flash",  # choose free long-context model
        contents=prompt
    )
    return resp.text

# Use case
prods = load_filtered_products("./data/amazon2023_500.jsonl")
prompt = build_prompt(prods, "what would be a good music album to buy for a sexy time?")
answer = ask_gemini(prompt)
print(answer)
