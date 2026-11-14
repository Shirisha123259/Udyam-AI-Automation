
import json
from pathlib import Path

from ai_extractor import extract_business_data
from validator import validate_business_data
from nic_mapper import suggest_nic_codes
from field_mapper import map_business_data, display_mapping


def main():

    print("\n========================================")
    print(" UDYAM AI REGISTRATION AUTOMATION SYSTEM")
    print("========================================")

    # Create output folder
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)

    # STEP 1: AI DATA EXTRACTION
    print("\n[STEP 1] AI BUSINESS DATA EXTRACTION")

    try:
        extracted_data = extract_business_data("business_data.txt")

        print("\nAI extraction completed successfully.")

        print("\n=== EXTRACTED BUSINESS INFORMATION ===")
        print(json.dumps(extracted_data, indent=4))

    except Exception as error:
        print("\nAI extraction failed:", error)
        return

    # Save extracted data
    extracted_file = output_dir / "extracted_data.json"

    with open(extracted_file, "w", encoding="utf-8") as file:
        json.dump(extracted_data, file, indent=4)

    print("\nExtracted data saved:", extracted_file)

    # STEP 2: DATA VALIDATION
    print("\n[STEP 2] BUSINESS DATA VALIDATION")

    errors, warnings = validate_business_data(extracted_data)

    if errors:
        print("\nValidation errors:")
        for error in errors:
            print("-", error)
    else:
        print("\nNo format or required-field errors found.")

    if warnings:
        print("\nValidation warnings:")
        for warning in warnings:
            print("-", warning)
    else:
        print("No missing-information warnings found.")

    # STEP 3: NIC CODE SUGGESTIONS
    print("\n[STEP 3] NIC CODE SUGGESTIONS")

    description = extracted_data.get("business_description", "")

    nic_suggestions = suggest_nic_codes(description)

    if nic_suggestions:
        print("\nSuggested NIC codes:")

        for suggestion in nic_suggestions:
            print("-", suggestion)
    else:
        print("No NIC suggestions found.")

    print("\nPlease confirm the principal business activity manually.")

    # STEP 4: PORTAL FIELD MAPPING
    print("\n[STEP 4] UDYAM PORTAL FIELD MAPPING")

    mapped_data, unmapped_fields = map_business_data(extracted_data)

    display_mapping(mapped_data, unmapped_fields)

    # Save mapped data
    mapped_file = output_dir / "mapped_data.json"

    with open(mapped_file, "w", encoding="utf-8") as file:
        json.dump(mapped_data, file, indent=4)

    print("\nMapped data saved:", mapped_file)

    # STEP 5: FINAL PROCESSING REPORT
    print("\n[STEP 5] FINAL PROCESSING REPORT")

    report = {
        "extraction_status": "Success",
        "validation_status": "Passed" if not errors else "Needs Correction",
        "validation_errors": errors,
        "validation_warnings": warnings,
        "nic_suggestions": nic_suggestions,
        "mapped_fields_count": len(mapped_data),
        "unmapped_fields": unmapped_fields,
        "portal_automation_status": "Inspection and mapping only",
        "final_submission_status": "Not submitted"
    }

    report_file = output_dir / "final_report.json"

    with open(report_file, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    print("\n=== FINAL REPORT ===")
    print(json.dumps(report, indent=4))

    print("\nFinal report saved:", report_file)

    print("\n========================================")
    print(" UDYAM AI PROCESSING COMPLETED")
    print("========================================")

    print("\nImportant:")
    print("- This run uses fictional demonstration data.")
    print("- Portal field mapping is preliminary.")
    print("- No Aadhaar or OTP was entered.")
    print("- No government registration was submitted.")


if __name__ == "__main__":
    main()
