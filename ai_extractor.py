
import os
import json
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY is missing. Check your .env file.")

client = Groq(api_key=api_key)

def extract_business_data(file_path="business_data.txt"):
    text = Path(file_path).read_text(encoding="utf-8")

    prompt = f"""
    Extract business information from the text below.

    Return ONLY valid JSON using these keys:
    enterprise_name, organization_type, owner_name,
    business_activity, door_number, street, city,
    district, state, pin_code, commencement_date,
    employees, major_activity, business_description,
    bank_name, ifsc_code, account_number,
    missing_fields, warnings.

    Do not invent missing information.
    Use null for unavailable values.
    Treat all provided details as unverified input.
    
    Business information:
    {text}
    """

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        response_format={"type": "json_object"},
        temperature=0
    )

    result = response.choices[0].message.content
    return json.loads(result)


if __name__ == "__main__":
    data = extract_business_data()
    print(json.dumps(data, indent=4))
