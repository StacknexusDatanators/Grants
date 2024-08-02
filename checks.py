from fastapi import HTTPException
import re
from typing import Dict


def validate_aadhaar_info(aadhaar_info: dict) -> None:
    name = aadhaar_info.get("Name", "").strip()
    aadhaar_number = aadhaar_info.get("Aadhaar_number", "").strip()
    dob = aadhaar_info.get("Date_of_birth", "").strip()

    # Check Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Name is missing or invalid")
    
    # Check Aadhaar Number (ensure it matches the 12-digit format with optional spaces)
    if not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', aadhaar_number):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Aadhaar number is missing or invalid")
    
    # Check Date of Birth (ensure it matches the dd/mm/yyyy format)
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Date of birth is missing or invalid")


def validate_income_cert_applicant_form(applicant_data: Dict[str, str]) -> None:
    applicant_name = applicant_data.get("Applicant Name", "").strip()
    father_husband_name = applicant_data.get("Father_Husband_Name", "").strip()
    dob = applicant_data.get("Date_of_birth", "").strip()
    aadhaar_number = applicant_data.get("Adhaar_Number", "").strip()
    mobile_number = applicant_data.get("Mobile_number", "").strip()
    ration_card = applicant_data.get("Ration_card", "").strip()

    # Check Applicant Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', applicant_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Applicant Name is missing or invalid")
    
    # Check Father/Husband Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', father_husband_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Father/Husband Name is missing or invalid")
    
    # Check Date of Birth (ensure it matches the dd/mm/yyyy format)
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Date of Birth is missing or invalid")
    
    # Check Aadhaar Number (ensure it matches the 12-digit format with optional spaces)
    if not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', aadhaar_number):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Aadhaar Number is missing or invalid")
    
    # Check Mobile Number (ensure it matches the 10-digit format)
    if not re.match(r'^\d{10}$', mobile_number):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Mobile Number is missing or invalid")
    
    # Check Ration Card Number (ensure it's a valid alphanumeric string with optional spaces and hyphens)
    if not re.match(r'^[A-Za-z0-9\s\-]+$', ration_card):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Ration Card Number is missing or invalid")


def validate_community_or_birth_certificate_form(birth_certificate_data: Dict[str, str]) -> None:
    name = birth_certificate_data.get("Name", "").strip()
    father_husband_name = birth_certificate_data.get("Father_Husband_Name", "").strip()
    dob = birth_certificate_data.get("Date_of_birth", "").strip()
    mobile_number = birth_certificate_data.get("Mobile_number", "").strip()
    caste = birth_certificate_data.get("Caste", "").strip()
    aadhaar_number = birth_certificate_data.get("Aadhaar_Number", "").strip()

    # Check Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Name is missing or invalid")
    
    # Check Father/Husband Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', father_husband_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Father/Husband Name is missing or invalid")
    
    # Check Date of Birth (ensure it matches the dd/mm/yyyy format)
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Date of Birth is missing or invalid")
    
    # Check Mobile Number (ensure it matches the 10-digit format)
    if not re.match(r'^\d{10}$', mobile_number):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Mobile Number is missing or invalid")
    
    # Check Caste (ensure it's a valid string with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', caste):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Caste is missing or invalid")
    
    # Check Aadhaar Number (ensure it matches the 12-digit format with optional spaces)
    if not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', aadhaar_number):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Aadhaar Number is missing or invalid")
    
def validate_aadhar_ration_EPIC_card_info(card_data: Dict[str, str], document_type: str) -> None:
    name = card_data.get("Name", "").strip()
    dob = card_data.get("Date_of_birth", "").strip()
    card_no = card_data.get("Card_No", "").strip()
    member_names = card_data.get("Member_Name(s)", "").strip()  # Relevant for Ration Card

    # Check Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Name is missing or invalid")
    
    # Check Date of Birth (ensure it matches the dd/mm/yyyy format)
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Date of Birth is missing or invalid")
    
    # Check Card Number (ensure it matches a generic card number format)
    if not re.match(r'^[A-Za-z0-9\s\-]+$', card_no):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Card Number is missing or invalid")

    # Check Member Names (only applicable for Ration Card; ensure it's a valid string with alphabetic characters and spaces)
    if document_type == 'ration_card' and member_names and not re.match(r'^[A-Za-z\s,]+$', member_names):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Member Names are invalid or formatted incorrectly")

def validate_ebc_certificate_info(ebc_data: Dict[str, str]) -> None:
    name = ebc_data.get("Name", "").strip()
    father_husband_name = ebc_data.get("Father_Husband_Name", "").strip()
    dob = ebc_data.get("Date_of_birth", "").strip()
    mobile_no = ebc_data.get("Mobile_No", "").strip()
    caste = ebc_data.get("Caste", "").strip()
    aadhaar_no = ebc_data.get("Aadhar_Card_No", "").strip()
    annual_income = ebc_data.get("Annual_Income", "").strip()

    # Check Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Name is missing or invalid")
    
    # Check Father/Husband Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', father_husband_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Father/Husband Name is missing or invalid")
    
    # Check Date of Birth (ensure it matches the dd/mm/yyyy format)
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Date of Birth is missing or invalid")
    
    # Check Mobile Number (ensure it matches a 10-digit number)
    if not re.match(r'^\d{10}$', mobile_no):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Mobile Number is missing or invalid")
    
    # Check Caste (ensure it's a valid string with alphabetic characters and spaces)
    if not re.match(r'^[A-Za-z\s]+$', caste):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Caste is missing or invalid")
    
    # Check Aadhaar Number (ensure it matches the 12-digit format with optional spaces)
    if not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', aadhaar_no):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Aadhaar Card Number is missing or invalid")
    
    # Check Annual Income (ensure it's a valid numerical value, optionally with commas)
    if not re.match(r'^\d+(?:,\d{3})*$|^\d+$', annual_income):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Annual Income is missing or invalid")


def validate_ews_applicant_form(ews_data: Dict[str, str]) -> None:
    name = ews_data.get("Name", "").strip()
    father_husband_name = ews_data.get("Father_Husband_Name", "").strip()
    dob = ews_data.get("Date_of_birth", "").strip()
    mobile_no = ews_data.get("Mobile_No", "").strip()
    caste = ews_data.get("Caste", "").strip()
    aadhar_card_no = ews_data.get("Aadhar_Card_No", "").strip()
    annual_income = ews_data.get("Annual_Income", "").strip()

    # Check Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Name is missing or invalid")

    # Check Father/Husband Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', father_husband_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Father/Husband Name is missing or invalid")

    # Check Date of Birth (ensure it matches the dd/mm/yyyy format)
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Date of Birth is missing or invalid")

    # Check Mobile Number (ensure it's a 10-digit number)
    if not re.match(r'^\d{10}$', mobile_no):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Mobile Number is missing or invalid")

    # Check Caste (ensure it's a valid string with alphabetic characters and spaces)
    if not re.match(r'^[A-Za-z\s]+$', caste):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Caste is missing or invalid")

    # Check Aadhaar Card Number (ensure it matches the 12-digit format with optional spaces)
    if not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', aadhar_card_no):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Aadhaar Card Number is missing or invalid")

    # Check Annual Income (ensure it matches a number with optional thousands separators)
    if not re.match(r'^\d+(?:,\d{3})*$|^\d+$', annual_income):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Annual Income is missing or invalid")
    
def validate_obc_applicant_form(obc_data: Dict[str, str]) -> None:
    name = obc_data.get("Name", "").strip()
    father_husband_name = obc_data.get("Father_Husband_Name", "").strip()
    dob = obc_data.get("Date_of_birth", "").strip()
    mobile_no = obc_data.get("Mobile_No", "").strip()
    caste_subcaste = obc_data.get("Caste_Subcaste", "").strip()
    aadhar_card_no = obc_data.get("Aadhar_Card_No", "").strip()

    # Check Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Name is missing or invalid")

    # Check Father/Husband Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', father_husband_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Father/Husband Name is missing or invalid")

    # Check Date of Birth (ensure it matches the dd/mm/yyyy format)
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', dob):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Date of Birth is missing or invalid")

    # Check Mobile Number (ensure it's a 10-digit number)
    if not re.match(r'^\d{10}$', mobile_no):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Mobile Number is missing or invalid")

    # Check Caste/Subcaste (ensure it contains alphabetic characters and spaces)
    if not re.match(r'^[A-Za-z\s]+$', caste_subcaste):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Caste/Subcaste is missing or invalid")

    # Check Aadhaar Card Number (ensure it matches the 12-digit format with optional spaces)
    if not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', aadhar_card_no):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Aadhaar Card Number is missing or invalid")
    

def validate_residence_certificate_form(residence_data: Dict[str, str]) -> None:
    name = residence_data.get("Name", "").strip()
    father_husband_name = residence_data.get("Father_Husband_Name", "").strip()
    mandal_name = residence_data.get("Mandal_Name", "").strip()
    village_name = residence_data.get("Village_Name", "").strip()
    house_number = residence_data.get("House_Number", "").strip()
    no_of_years = residence_data.get("No_of_years", "").strip()
    address = residence_data.get("Address", "").strip()

    # Check Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Name is missing or invalid")

    # Check Father/Husband Name (ensure it's a valid name with alphabetic characters, spaces, and hyphens)
    if not re.match(r'^[A-Za-z\s\-]+$', father_husband_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Father/Husband Name is missing or invalid")

    # Check Mandal Name (ensure it's a valid string with alphabetic characters and spaces)
    if not re.match(r'^[A-Za-z\s]+$', mandal_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Mandal Name is missing or invalid")

    # Check Village Name (ensure it's a valid string with alphabetic characters and spaces)
    if not re.match(r'^[A-Za-z\s]+$', village_name):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Village Name is missing or invalid")

    # Check House Number (ensure it's alphanumeric with optional spaces and hyphens)
    if not re.match(r'^[A-Za-z0-9\s\-]+$', house_number):
        raise HTTPException(status_code=422, detail="Unrecognized entity: House Number is missing or invalid")

    # Check No of Years (ensure it's a numeric value)
    if not re.match(r'^\d+$', no_of_years):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Number of Years is missing or invalid")

    # Check Address (ensure it's a valid address with alphabetic characters, numbers, spaces, and optional commas)
    if not re.match(r'^[A-Za-z0-9\s,]+$', address):
        raise HTTPException(status_code=422, detail="Unrecognized entity: Address is missing or invalid")