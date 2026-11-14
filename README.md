# AI-Powered MSME Udyam Registration Automation System

## Project Overview

This project is a prototype of an AI-powered MSME Udyam Registration Automation System. It extracts business information from a local TXT file, converts it into structured data using an LLM, validates the extracted fields, suggests NIC codes, and demonstrates browser automation using Playwright.

**Important:** This is an educational prototype. The sample business information is fictional. The system does not submit any application to the Government of India.

## Features

1. **AI Data Extraction** – Extracts enterprise information from a TXT file using Groq LLM.
2. **Data Validation** – Checks required fields, PIN code format, employee count, commencement date and IFSC format.
3. **NIC Code Suggestions** – Suggests relevant NIC code candidates based on business activity.
4. **Field Mapping** – Maps available business data to a registration field checklist and identifies missing and sensitive fields.
5. **Portal Inspection** – Uses Playwright to inspect the official Udyam portal's publicly visible first-stage form.
6. **Mock Browser Automation** – Automatically fills 15 fields in a local mock registration form.
7. **Error Handling** – Tests invalid PIN code and missing enterprise name scenarios.
8. **Final Review** – Stops at the mock final review stage without submitting anything.

## Technologies Used

- Python
- Groq API / LLM
- Playwright
- Pandas
- Pydantic
- JSON
- HTML, CSS and JavaScript

## Project Workflow

TXT Business Data → AI Extraction → Data Validation → NIC Suggestions → Field Mapping → Playwright Mock Form Automation → Error Handling → Final Review

## Project Structure

```text
Udyam_AI_Automation/
│
├── main.py
├── ai_extractor.py
├── validator.py
├── nic_mapper.py
├── field_mapper.py
├── portal_automation.py
├── portal_inspector.py
├── test_error_handling.py
├── mock_udyam_portal.html
├── business_data.txt
├── requirements.txt
├── .env
│
├── output/
│   ├── extracted_data.json
│   ├── mapped_data.json
│   ├── final_report.json
│   ├── verified_field_checklist.json
│   ├── portal_inspection_report.json
│   ├── automation_report.json
│   └── error_handling_report.json
│
└── screenshots/
```

## How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API key

Create a `.env` file:

```text
GROQ_API_KEY=your_groq_api_key
```

Keep your actual API key private. Do not upload `.env` to GitHub.

### 3. Run AI extraction and validation

```bash
python main.py
```

### 4. Inspect the official portal

```bash
python portal_inspector.py
```

This inspects the publicly visible first-stage registration page only. No personal information is entered and no verification is attempted.

### 5. Run mock browser automation

```bash
python portal_automation.py
```

### 6. Run error-handling tests

```bash
python test_error_handling.py
```

## Test Results

| Test | Result |
|---|---|
| Mock form automation | Successful |
| Fields automatically filled | 15 |
| Mock form validation | Successful |
| Invalid PIN code test | PASS |
| Missing enterprise name test | PASS |
| Final Review reached | Yes |
| Government application submitted | No |

## Limitations and Safety

- The sample business data is fictional and used only for offline testing.
- The official Udyam portal was inspected, but the full registration workflow was not automated.
- Aadhaar verification, OTP and CAPTCHA were not attempted.
- Later official registration fields were not verified through an authorized registration session.
- The mock form demonstrates the browser automation workflow without interacting with government registration records.
- No application was submitted.

## Conclusion

This prototype demonstrates AI-based business data extraction, validation, NIC code suggestions, field mapping, browser automation and error handling. It provides a foundation for a compliant registration-assistance workflow using genuine, authorized business information.