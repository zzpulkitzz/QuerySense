from google import genai
import json
import sys
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
    return f"I want you to generate text that will be directly used as the main interface of an E-commerce platform through which a user will interact with the Ecommerce platform's product search experience . Your main goal is to help the user find the right product to buy and assist them with the shopping experience . This is the dataset for all the product listings availaible on the platform :\n\n{context}\n\n  -Make sure you do not answer any queries that are not related to the E-commerce store. \n User-query : {user_query}\n"


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
print(sys.argv)
prompt = build_prompt(prods, sys.argv[1])
answer = ask_gemini(prompt)
print(answer)
