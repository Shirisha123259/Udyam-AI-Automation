
import json
from pathlib import Path


# Official Udyam form field reference.
# Field names are based on the official application form.
# This is a mapping checklist, not verified browser selectors.

PORTAL_FIELDS = {
    "Aadhaar Verification": [
        ("aadhaar_number", "Aadhaar Number", "Sensitive - manual entry"),
        ("owner_name", "Name of Entrepreneur", "Available in input")
    ],

    "PAN Verification": [
        ("pan_number", "PAN Number", "Sensitive - manual entry"),
        ("pan_holder_name", "Name of PAN Holder", "Not available"),
        ("dob_or_doi", "DOB or DOI as per PAN", "Not available"),
        ("gstin", "GSTIN", "Not available"),
        ("itr_filed", "Previous Year ITR Filed", "Not available")
    ],

    "Basic Details": [
        ("organization_type", "Type of Organisation", "Available in input"),
        ("enterprise_name", "Name of Enterprise", "Available in input"),
        ("mobile_number", "Mobile Number", "Not available"),
        ("email", "Email", "Not available"),
        ("social_category", "Social Category", "Not available"),
        ("gender", "Gender", "Not available"),
        ("specially_abled", "Specially Abled", "Not available")
    ],

    "Plant/Unit Details": [
        ("unit_name", "Plant/Unit Name", "Not available"),
        ("plant_door_number", "Plant Door Number", "Not available"),
        ("plant_street", "Plant Road/Street", "Not available"),
        ("plant_city", "Plant City", "Not available"),
        ("plant_pin_code", "Plant PIN Code", "Not available")
    ],

    "Official Address": [
        ("door_number", "Flat/Door/Block Number", "Available in input"),
        ("premises_name", "Name of Premises/Building", "Not available"),
        ("village_town", "Village/Town", "Not available"),
        ("block", "Block", "Not available"),
        ("street", "Road/Street/Lane", "Available in input"),
        ("city", "City", "Available in input"),
        ("pin_code", "PIN Code", "Available in input"),
        ("state", "State", "Available in input"),
        ("district", "District", "Available in input")
    ],

    "Enterprise Status": [
        ("incorporation_date", "Date of Incorporation/Registration", "Not available"),
        ("commencement_date", "Date of Commencement", "Available in input"),
        ("business_commenced", "Whether Business Commenced", "Not available"),
        ("previous_registration", "Previous EM-II/UAM Registration", "Not available")
    ],

    "Bank Details": [
        ("bank_name", "Bank Name", "Available in input"),
        ("ifsc_code", "IFS Code", "Available in input"),
        ("account_number", "Bank Account Number", "Sensitive - local input only")
    ],

    "Business Activity": [
        ("major_activity", "Major Activity", "Available in input"),
        ("nic_code", "NIC Activity Code", "Suggested - manual confirmation"),
        ("employees_male", "Male Employees", "Not available"),
        ("employees_female", "Female Employees", "Not available"),
        ("employees_others", "Other Employees", "Not available"),
        ("employees", "Total Employees", "Available in input")
    ],

    "Financial Details": [
        ("investment", "Investment in Plant and Machinery/Equipment", "Not available"),
        ("turnover", "Total Turnover", "Not available"),
        ("export_turnover", "Export Turnover", "Not available")
    ]
}


def map_business_data(data):

    mapped = {}
    missing = []
    sensitive = []
    manual_confirmation = []

    for section, fields in PORTAL_FIELDS.items():

        mapped[section] = []

        for key, label, status in fields:

            value = data.get(key)

            if status.startswith("Sensitive"):
                sensitive.append(label)
                mapped[section].append({
                    "field": label,
                    "value": "[MANUAL ENTRY REQUIRED]",
                    "status": status
                })

            elif status.startswith("Suggested"):
                manual_confirmation.append(label)
                mapped[section].append({
                    "field": label,
                    "value": data.get(key, "NIC suggestion required"),
                    "status": status
                })

            elif value is not None and str(value).strip():

                mapped[section].append({
                    "field": label,
                    "value": value,
                    "status": "Available in input"
                })

            else:
                missing.append(label)

                mapped[section].append({
                    "field": label,
                    "value": None,
                    "status": "Information required"
                })

    return mapped, missing, sensitive, manual_confirmation


def display_mapping(mapped, missing, sensitive, manual_confirmation):

    print("\n========== OFFICIAL FIELD MAPPING ==========")

    for section, fields in mapped.items():

        print(f"\n--- {section} ---")

        for item in fields:

            print(
                f"{item['field']}: "
                f"{item['value']} "
                f"[{item['status']}]"
            )

    print("\n========== MISSING INFORMATION ==========")

    for field in missing:
        print("-", field)

    print("\n========== MANUAL ENTRY REQUIRED ==========")

    for field in sensitive:
        print("-", field)

    print("\n========== MANUAL CONFIRMATION ==========")

    for field in manual_confirmation:
        print("-", field)

    print("\nNote:")
    print("This is a field checklist based on the official form.")
    print("Actual live portal controls and selectors need separate inspection.")
    print("Never use fictional data for real government registration.")


if __name__ == "__main__":

    input_file = Path("output/extracted_data.json")

    if not input_file.exists():
        print("Extracted data not found. Run python main.py first.")

    else:
        with open(input_file, "r", encoding="utf-8") as file:
            data = json.load(file)

        mapped, missing, sensitive, manual = map_business_data(data)

        display_mapping(mapped, missing, sensitive, manual)

        output_file = Path("output/verified_field_checklist.json")

        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(mapped, file, indent=4)

        print("\nChecklist saved:", output_file)
