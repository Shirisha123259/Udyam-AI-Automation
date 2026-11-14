
from pathlib import Path
import json
from playwright.sync_api import sync_playwright


URL = "https://udyamregistration.gov.in/UdyamRegistration.aspx"


def inspect_portal():

    Path("screenshots").mkdir(exist_ok=True)
    Path("output").mkdir(exist_ok=True)

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False)

        page = browser.new_page(
            viewport={"width": 1366, "height": 900}
        )

        try:
            print("\n=== UDYAM PORTAL INSPECTION ===")

            page.goto(
                URL,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(4000)

            print("Page title:", page.title())
            print("URL:", page.url)

            # Inspect visible form controls
            controls = page.locator(
                "input:not([type=hidden]), select, textarea, button"
            ).evaluate_all("""
                elements => elements
                    .filter(el => {
                        const r = el.getBoundingClientRect();
                        const style = window.getComputedStyle(el);

                        return r.width > 0 &&
                               r.height > 0 &&
                               style.visibility !== "hidden" &&
                               style.display !== "none";
                    })
                    .map(el => ({
                        tag: el.tagName,
                        type: el.getAttribute("type"),
                        id: el.id,
                        name: el.getAttribute("name"),
                        placeholder: el.getAttribute("placeholder"),
                        text: el.innerText?.trim() || "",
                        disabled: el.disabled,
                        maxLength: el.maxLength
                    }))
            """)

            print("\n=== VISIBLE FORM CONTROLS ===")

            for item in controls:
                print(item)

            # Inspect visible headings and labels
            headings = page.locator(
                "h1, h2, h3, h4, h5, label"
            ).evaluate_all("""
                elements => elements
                    .filter(el => {
                        const r = el.getBoundingClientRect();
                        return r.width > 0 && r.height > 0;
                    })
                    .map(el => el.innerText.trim())
                    .filter(text => text.length > 0)
            """)

            print("\n=== HEADINGS AND LABELS ===")

            for heading in headings:
                print("-", heading)

            # Save results
            report = {
                "page_title": page.title(),
                "url": page.url,
                "visible_controls": controls,
                "headings_and_labels": headings,
                "inspection_only": True
            }

            output_path = Path(
                "output/portal_inspection_report.json"
            )

            with open(
                output_path,
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(report, file, indent=4)

            page.screenshot(
                path="screenshots/portal_inspection.png",
                full_page=True
            )

            print("\nInspection report saved:", output_path)
            print("Screenshot saved: screenshots/portal_inspection.png")

            print("\nNo personal information entered.")
            print("No verification button clicked.")
            print("No OTP or CAPTCHA handled.")
            print("No registration submitted.")

            input("\nPress Enter to close browser...")

        except Exception as error:
            print("Inspection error:", error)

        finally:
            browser.close()


if __name__ == "__main__":
    inspect_portal()
