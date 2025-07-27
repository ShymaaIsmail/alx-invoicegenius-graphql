# ai_parser/utils.py
import openai
from decouple import config

openai.api_key = config("OPENAI_API_KEY")

def parse_invoice_text(text):
    prompt = f"""
You are an intelligent invoice parser. Extract the following fields from the given text:
- Vendor name
- Invoice number
- Invoice date
- Total amount
- Tax (if any)

Text:
{text}

Return data in JSON format with keys:
vendor_name, invoice_number, invoice_date, total_amount, tax
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",  # Or another model depending on cost/speed
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        content = response['choices'][0]['message']['content']
        return eval(content) if content.startswith('{') else None  # Use json.loads if preferred
    except Exception as e:
        print("AI parsing error:", e)
        return None
