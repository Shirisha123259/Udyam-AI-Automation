
from pathlib import Path
import json
from playwright.sync_api import sync_playwright


# Project files
DATA_FILE = Path("output/extracted_data.json")
HTML_FILE = Path("mock_udyam_portal.html")

SCREENSHOT_DIR = Path("screenshots")
OUTPUT_DIR = Path("output")


def load_business_data():
    if not DATA_FILE.exists():
        raise FileNotFoundError(
            "output/extracted_data.json not found. Run python main.py first."
        )

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def automate_mock_portal():

    SCREENSHOT_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    if not HTML_FILE.exists():
        raise FileNotFoundError("mock_udyam_portal.html not found.")

    data = load_business_data()

    # Only use fictional sample data in this local mock form.
    if data.get("enterprise_name") != "Sunrise Digital Services":
        raise ValueError(
            "This demo is configured for the fictional Sunrise Digital Services sample only."
        )

    # Map extracted JSON fields to mock form IDs
    field_mapping = {
        "enterprise_name": "enterprise_name",
        "organization_type": "organization_type",
        "owner_name": "owner_name",
        "business_activity": "business_activity",
        "city": "city",
        "district": "district",
        "state": "state",
        "pin_code": "pin_code",
        "commencement_date": "commencement_date",
        "employees": "employees",
        "major_activity": "major_activity",
        "business_description": "business_description",
        "bank_name": "bank_name",
        "ifsc_code": "ifsc_code",
        "account_number": "account_number"
    }

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)
        page = browser.new_page(
            viewport={"width": 1366, "height": 1000}
        )

        try:
            print("\n=== MOCK UDYAM AUTOMATION ===")

            page.goto(HTML_FILE.resolve().as_uri())
            page.wait_for_timeout(1000)

            print("Opened:", page.title())

            filled_fields = []
            skipped_fields = []

            # Automatically fill the mock form
            for json_key, element_id in field_mapping.items():

                value = data.get(json_key)

                if value is None or str(value).strip() == "":
                    skipped_fields.append(json_key)
                    continue

                page.locator(f"#{element_id}").fill(str(value))
                filled_fields.append(json_key)

                print(f"Filled {json_key}")

            print("\nTotal fields filled:", len(filled_fields))

            if skipped_fields:
                print("Skipped missing fields:", skipped_fields)

            # Trigger local mock validation
            page.locator("#validateBtn").click()

            page.wait_for_timeout(1000)

            message = page.locator("#message").inner_text()
            print("\nValidation result:", message)

            review_visible = page.locator("#review").is_visible()

            if review_visible:
                print("\nSUCCESS: Final Review reached.")
            else:
                print("\nERROR: Final Review was not reached.")

            # Save screenshot
            screenshot_path = SCREENSHOT_DIR / "mock_final_review.png"
            page.screenshot(
                path=str(screenshot_path),
                full_page=True
            )

            # Save automation report
            report = {
                "portal": "Local Mock Udyam Registration",
                "automation": "Playwright",
                "filled_fields": filled_fields,
                "skipped_fields": skipped_fields,
                "validation_message": message,
                "final_review_reached": review_visible,
                "submitted": False,
                "real_government_portal_used": False
            }

            report_path = OUTPUT_DIR / "automation_report.json"

            with open(report_path, "w", encoding="utf-8") as file:
                json.dump(report, file, indent=4)

            print("\nReport saved:", report_path)
            print("Screenshot saved:", screenshot_path)
            print("Submission performed: NO")

            input("\nPress Enter to close browser...")

        except Exception as error:
            print("\nAutomation error:", error)

        finally:
            browser.close()


if __name__ == "__main__":
    automate_mock_portal()
