# ai_parser/utils.py
import openai
import tiktoken
import logging
import json
from django.conf import settings

# Configure logging
logger = logging.getLogger(__name__)
openai.api_key = settings.OPENAI_API_KEY


def count_tokens(prompt, model="gpt-3.5-turbo"):
    """Count the number of tokens in a prompt for the specified OpenAI model."""
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(prompt))

def parse_invoice_text(text):
    """Parse the invoice text using OpenAI's GPT model to extract structured data."""
    logger.info(f"OPENAI_API_KEY loaded: {openai.api_key}")

    prompt = f"""
  You are a smart invoice parser. Your job is to extract key fields from OCR text that may come from **any country**, **any language**, and **any layout or format**.

  Instructions:
  - Auto-detect the language.
  - Extract values even if the layout is inconsistent or messy.
  - Currency may be in symbols (€, $, £, CHF) or abbreviations (USD, EUR, CHF, JPY, etc.).
  - Always return a consistent JSON structure with all fields below.
  - Extract the invoice line items as a list under "line_items".
  - Each line item should have these fields: "description", "quantity", "unit_price", "total_price".
  - Parse the invoice date carefully.
  - Convert and return the invoice date strictly in ISO 8601 format: "YYYY-MM-DD" or "YYYY-MM-DDTHH:MM:SS" (24-hour clock).
  - Do NOT return dates in any other format.
  - If the original date/time is ambiguous or contains extra characters, clean and normalize it.
  - Return null if a valid date cannot be extracted or parsed.
  - Return null for any field that is missing or not detected.

  OCR Text:
  \"\"\"
  {text}
  \"\"\"

  Return JSON ONLY in this exact format:
  {{
    "vendor_name": "...",
    "invoice_number": "...",
    "invoice_date": "...",
    "total_amount": {{
      "value": ...,         
      "currency": "..."     
    }},
    "tax": {{
      "value": ...,         
      "currency": "..."     
    }},
    "line_items": [
      {{
        "description": "...",
        "quantity": ...,
        "unit_price": ...,
        "total_price": ...
      }}
    ]
  }}
  """


    try:
        logger.debug(f"Token count: {count_tokens(prompt)}")
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )

        content = response.choices[0].message.content.strip()
        logger.debug(f"OpenAI response: {content}")

        return json.loads(content)
    except json.JSONDecodeError:
        logger.error("JSON parsing failed: malformed AI response.")
        return None
    except Exception as e:
        logger.exception(f"AI parsing error {e.message}")
        return None
