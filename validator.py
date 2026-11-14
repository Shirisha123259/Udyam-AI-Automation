
import re
from datetime import datetime

def validate_business_data(data):
    errors = []
    warnings = []

    required_fields = [
        "enterprise_name",
        "organization_type",
        "owner_name",
        "business_activity",
        "city",
        "district",
        "state",
        "pin_code",
        "major_activity"
    ]

    for field in required_fields:
        if not data.get(field):
            errors.append(f"Missing required field: {field}")

    # PIN code validation
    pin = str(data.get("pin_code") or "")
    if pin and not re.fullmatch(r"[1-9][0-9]{5}", pin):
        errors.append("Invalid Indian PIN code format.")

    # Employee count validation
    try:
        employees = int(data.get("employees"))
        if employees < 0:
            errors.append("Employee count cannot be negative.")
    except (ValueError, TypeError):
        errors.append("Employee count must be a valid number.")

    # Date validation
    date_value = data.get("commencement_date")
    if date_value:
        try:
            datetime.strptime(date_value, "%d-%m-%Y")
        except ValueError:
            errors.append("Date must be in DD-MM-YYYY format.")
    else:
        warnings.append("Commencement date is missing.")

    # IFSC format validation only (not bank verification)
    ifsc = str(data.get("ifsc_code") or "").upper()
    if ifsc and not re.fullmatch(r"[A-Z]{4}0[A-Z0-9]{6}", ifsc):
        errors.append("Invalid IFSC format.")

    if not data.get("bank_name"):
        warnings.append("Bank name is missing.")

    if not data.get("business_description"):
        warnings.append("Business description is missing.")

    # AI-reported missing fields and warnings
    warnings.extend(data.get("warnings") or [])
    for field in data.get("missing_fields") or []:
        warnings.append(f"AI identified missing information: {field}")

    return errors, warnings
