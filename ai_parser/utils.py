# ai_parser/utils.py
import openai
import tiktoken
import logging
import json
from django.conf import settings

def count_tokens(prompt, model="gpt-3.5-turbo"):
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(prompt))

logger = logging.getLogger(__name__)

openai.api_key = settings.OPENAI_API_KEY


def parse_invoice_text(text):
    logger.info(f"OPENAI_API_KEY loaded: {openai.api_key}")

    prompt = f"""
You are a smart invoice parser. Your job is to extract key fields from OCR text that may come from **any country**, **any language**, and **any layout or format**.

Instructions:
- Auto-detect the language.
- Extract values even if the layout is inconsistent or messy.
- Currency may be in symbols (€, $, £, CHF) or abbreviations (USD, EUR, CHF, JPY, etc.).
- Always return a consistent JSON structure with all fields below.
- Return null if any field is missing or not detected.

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
  }}
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
