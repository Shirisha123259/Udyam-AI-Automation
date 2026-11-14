
from pathlib import Path
from playwright.sync_api import sync_playwright
import json

HTML_FILE = Path("mock_udyam_portal.html").resolve()
OUTPUT_DIR = Path("output")
SCREENSHOT_DIR = Path("screenshots")

OUTPUT_DIR.mkdir(exist_ok=True)
SCREENSHOT_DIR.mkdir(exist_ok=True)

TEST_DATA = {
    "enterprise_name": "Sunrise Digital Services",
    "organization_type": "Proprietorship",
    "owner_name": "Demo Owner",
    "business_activity": "Software Development",
    "city": "Bengaluru",
    "district": "Bengaluru Urban",
    "state": "Karnataka",
    "pin_code": "560001",
    "commencement_date": "01-04-2024",
    "employees": "5",
    "major_activity": "Services",
    "business_description": "Website design and IT consulting",
    "bank_name": "Demo Bank",
    "ifsc_code": "DEMO0001234",
    "account_number": "TEST000000"
}


def run_test(browser, test_name, changes, expected_message):

    page = browser.new_page()
    page.goto(HTML_FILE.as_uri())

    for field, value in TEST_DATA.items():
        page.locator(f"#{field}").fill(value)

    for field, value in changes.items():
        page.locator(f"#{field}").fill(value)

    page.locator("#validateBtn").click()

    message = page.locator("#message").inner_text()
    review_visible = page.locator("#review").is_visible()

    passed = (
        expected_message in message
        and not review_visible
    )

    print(f"\nTest: {test_name}")
    print("Message:", message)
    print("Final Review visible:", review_visible)
    print("Result:", "PASS" if passed else "FAIL")

    page.screenshot(
        path=str(SCREENSHOT_DIR / f"{test_name}.png"),
        full_page=True
    )

    result = {
        "test_name": test_name,
        "expected_message": expected_message,
        "actual_message": message,
        "final_review_visible": review_visible,
        "result": "PASS" if passed else "FAIL"
    }

    page.close()
    return result


def main():

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        results.append(run_test(
            browser,
            "invalid_pin_test",
            {"pin_code": "123"},
            "PIN code must contain exactly 6 digits."
        ))

        results.append(run_test(
            browser,
            "missing_enterprise_test",
            {"enterprise_name": ""},
            "Please complete the required fields."
        ))

        browser.close()

    report = {
        "total_tests": len(results),
        "passed": sum(r["result"] == "PASS" for r in results),
        "failed": sum(r["result"] == "FAIL" for r in results),
        "results": results
    }

    with open(
        OUTPUT_DIR / "error_handling_report.json",
        "w",
        encoding="utf-8"
    ) as file:
        json.dump(report, file, indent=4)

    print("\n=== ERROR HANDLING SUMMARY ===")
    print(json.dumps(report, indent=4))
    print("\nReport saved: output/error_handling_report.json")


if __name__ == "__main__":
    main()
