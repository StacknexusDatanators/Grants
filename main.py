from fastapi import FastAPI, UploadFile, File, HTTPException
from google.cloud import documentai_v1beta3 as documentai
import os
from typing import List, Dict
import ollama
import ast
import re

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/astrobalaji/Documents/stacknexus/grants/notebook/creds/grant01-joby.json"

app = FastAPI()

# If you already have a Document AI Processor in your project, assign the full processor resource name here.
processor_name = "projects/332125695616/locations/us/processors/a6bceed480e9d614"


def process_document(processor_name: str, file_path: str) -> documentai.Document:
    client = documentai.DocumentProcessorServiceClient()

    # Read the file into memory
    with open(file_path, "rb") as f:
        document_content = f.read()

    # Configure the request
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(
            content=document_content,
            mime_type="application/pdf"
        )
    )

    result = client.process_document(request=request)
    return result.document


@app.post("/process-pdf/")
async def process_pdf(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    document = process_document(processor_name, file_path=file_path)

    if document:
        extracted_data: List[Dict] = []

        # Extract text from the document
        document_text = document.text

        # Split the text into chunks based on paragraphs
        document_chunks = document_text.split('\n\n')  # Assuming paragraphs are separated by double newlines

        for chunk_number, chunk_content in enumerate(document_chunks, start=1):
            extracted_data.append(
                {
                    "file_name": file.filename,
                    "file_type": os.path.splitext(file.filename)[1],
                    "chunk_number": chunk_number,
                    "content": chunk_content,
                }
            )

        combined_list = [t["content"] for t in extracted_data]
        combined_str = "\n".join(combined_list)

        # Remove the temporary file
        os.remove(file_path)

        return {"text": combined_str}
    else:
        return {"error": "Failed to process the document"}


def parse_aadhaar_info(extracted_text: str) -> dict:
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': f"""[Requirement] for the following content parsed from a scanned Aadhaar card document. The Aadhaar number is a 12 digit number with spaces in between. I want you to give me the following data in the following json structure. 
            [json_structure] {{"Name":---, "Aadhaar_number":---, "Date_of_birth":---}}
            ["content"]{extracted_text}
            """,
        },
    ], format="json")

    # Safely evaluate the response content to convert it to a dictionary
    try:
        aadhaar_info = ast.literal_eval(response['message']['content'])
    except (SyntaxError, ValueError) as e:
        aadhaar_info = {"error": e}

    return aadhaar_info


def validate_aadhaar_info(aadhaar_info: dict) -> None:
    """Validates the extracted Aadhaar information."""
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


@app.post("/process-aadhaar/")
async def process_aadhaar(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    document = process_document(processor_name, file_path=file_path)

    if document:
        extracted_text = document.text

        # Parse Aadhaar information
        aadhaar_info = parse_aadhaar_info(extracted_text)

        # Validate Aadhaar information
        validate_aadhaar_info(aadhaar_info)

        # Remove the temporary file
        os.remove(file_path)

        return aadhaar_info
    else:
        return {"error": "Failed to process the document"}


def parse_income_cert(extracted_text: str) -> dict:
    prompt_template = """
        [Requirement] for the content that follows, which was extracted from an application form that was scanned. In addition to the applicant's name, which is a character with spaces between it, the date of birth is a variable character,  the mobile number with 10 digit number with spaces between it, the Adhaar number is a 12-digit number with spaces between it, and the ration card number is also a character. Please provide me with the following information in the JSON structure. 
        [json_structure] {{"Applicant Name":---, "Father_Husband_Name":---, "Date_of_birth":---  "Adhaar_Number":---  "Mobile_number":---  "Ration_card:---}}
        [content] {0}
    """
    response = ollama.chat(model='llama3', messages=[
        {
            'role': 'user',
            'content': prompt_template.format(extracted_text),
        },
    ], format="json")
    # Safely evaluate the response content to convert it to a dictionary
    try:
        inc_info = ast.literal_eval(response['message']['content'])
    except (SyntaxError, ValueError) as e:
        inc_info = {"error": "Failed to parse income information"}

    return inc_info


def validate_income_cert_applicant_form(applicant_data: Dict[str, str]) -> None:
    validation_errors = {}

    # Validate Applicant Name
    if not re.match(r'^[A-Za-z\s\-]+$', applicant_data.get("Applicant Name", "").strip()):
        validation_errors["Applicant Name"] = "Invalid name format. Only letters, spaces, and hyphens are allowed."

    # Validate Father/Husband Name
    if not re.match(r'^[A-Za-z\s\-]+$', applicant_data.get("Father_Husband_Name", "").strip()):
        validation_errors["Father_Husband_Name"] = "Invalid name format. Only letters, spaces, and hyphens are allowed."

    # Validate Date of Birth
    if not re.match(r'^\d{2}/\d{2}/\d{4}$', applicant_data.get("Date_of_birth", "").strip()):
        validation_errors["Date_of_birth"] = "Invalid date format. Expected format is dd/mm/yyyy."

    # Validate Aadhaar Number
    if not re.match(r'^\d{4}\s?\d{4}\s?\d{4}$', applicant_data.get("Adhaar_Number", "").strip()):
        validation_errors["Adhaar_Number"] = "Invalid Aadhaar number. It should be a 12-digit number with optional spaces."

    # Validate Mobile Number
    if not re.match(r'^\d{10}$', applicant_data.get("Mobile_number", "").strip()):
        validation_errors["Mobile_number"] = "Invalid mobile number. It should be a 10-digit number."

    # Validate Ration Card Number
    if not re.match(r'^[A-Za-z0-9\s\-]+$', applicant_data.get("Ration_card", "").strip()):
        validation_errors["Ration_card"] = "Invalid ration card number. Only alphanumeric characters, spaces, and hyphens are allowed."

    if validation_errors:
        raise HTTPException(status_code=422, detail=validation_errors)


@app.post("/process-income-cert/")
async def process_income_cert(file: UploadFile = File(...)):
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    document = process_document(processor_name, file_path=file_path)

    if document:
        extracted_text = document.text

        # Parse Income Certificate information
        inc_info = parse_income_cert(extracted_text)

        # Validate Income Certificate information
        validate_income_cert_applicant_form(inc_info)

        # Remove the temporary file
        os.remove(file_path)

        return inc_info
    else:
        return {"error": "Failed to process the document"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
