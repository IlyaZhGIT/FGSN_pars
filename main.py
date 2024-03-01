import json
from pathlib import Path
from pprint import pprint

import requests
from pydantic import BaseModel


STATUSES = {
    "Архивный": 1,
    "Действует": 6,
    "Прекращен": 14,
    "Приостановлен": 15,
    "Частично приостановлен": 19,
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
}

class AccreditedPerson(BaseModel):
    type_person: str
    name: str
    address: str

    full_name: str
    mail: str
    phone: str

    @staticmethod
    def create_accredited_person(applicant_json) -> "AccreditedPerson":
        type_id = applicant_json.get("idType") # передать для получаения наименования типа
        name_type = get_multi_nsi_by_id("guApType", type_id)
        shortName = applicant_json.get("shortName")
        address = applicant_json.get("addresses")[0].get("fullAddress")

        head_person = applicant_json.get("headPerson")
        full_name = f"{head_person.get("name")} {head_person.get("surname")} {head_person.get("patronymic")}"
        phone = applicant_json.get("contacts")[0].get("value")
        mail = applicant_json.get("contacts")[-1].get("value")

        return AccreditedPerson(type_person=name_type, name=shortName, address=address, full_name=full_name, mail=mail, phone=phone)

class Accreditation(BaseModel):
    full_name: str
    confirmation_of_competence: str | None

    @staticmethod
    def create_accreditation(applicant_json):
        confirmations = applicant_json.get("confirmCompetenceChanges")
        if not confirmations: 
            return None
        last_confirmation = confirmations[-1]
        
        full_name = last_confirmation.get("expertGroup").get("expertFio")
        
        confirmation_id = last_confirmation.get("idResult")
        confirmation_of_competence = get_multi_nsi_by_id("typeResultOfConfirm", confirmation_id)
        
        return Accreditation(full_name=full_name, confirmation_of_competence=confirmation_of_competence)
        

class Applicant(BaseModel):
    ral: str
    inn: str
    applicant: str

    full_name: str
    mail: str
    phone: str
    address: str

    accredited_person: AccreditedPerson
    accreditation: Accreditation | None
    

    @staticmethod
    def create_applicant(applicant_json, accredited_person, accreditation) -> "Applicant":
        reg_number = applicant_json.get("regNumbers")[0].get("regNumber")

        short_name = applicant_json.get("shortName")

        applicant = applicant_json.get('applicant')
        inn = applicant.get("inn")
        address = applicant.get("addresses")[0].get("fullAddress")
        
        person = applicant.get('person')
        full_name = f"{person.get("name")} {person.get("surname")} {person.get("patronymic")}"

        contacts = applicant.get("contacts")
        phone = contacts[0].get("value")
        mail = contacts[-1].get("value")
        
        return Applicant(ral=reg_number, inn=inn, applicant=short_name, full_name=full_name,mail=mail, phone=phone, address=address, accreditation=accreditation, accredited_person=accredited_person)    


def get_applicant_by_id(id: str):
    response = requests.get(
        f"https://pub.fsa.gov.ru/api/v1/ral/common/companies/{id}",
        headers=headers,
        timeout=15,
    )
    return response.json()


def get_multi_nsi_by_id(item: str ,type_id: int) -> str:
    json_data = { 
        "items": {
            item: [
                {
                    "id": [
                        type_id,
                    ],
                    "fields": [
                        "name",
                    ],
                },
            ],
        }
    }
    
    response = requests.post(
        "https://pub.fsa.gov.ru/nsi/api/multi",
        headers=headers,
        json=json_data,
        timeout=10
    ).json().get(item)[0].get("name")
    
    return response


def write_json(data: list[dict], file_name: str) -> Path:
    file_path = f"{file_name}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return Path(file_path)    


def get_applicants_json(statuses, limit):
    json_data = {
        "idStatus": statuses,
        "columns": [],
        "sort": [
            "-id",
        ],
        "limit": limit,
        "offset": 0,
        "numberOfAllRecords": False,
    }
    response = requests.post(
        url="https://pub.fsa.gov.ru/api/v1/ral/common/showcases/get",
        headers=headers,
        json=json_data,
        timeout=15,
    )
    return response.json()

def get_token_request(headers) -> str:
    json_data = {
        
        "username": "anonymous",
        "password": "hrgesf7HDR67Bd",
    }
    response = requests.post(
        "https://pub.fsa.gov.ru/login",
        headers=headers,
        json=json_data,
        timeout=15,
    )
    return response.headers.get("Authorization")
    

def main():
    global headers
    headers["Authorization"] = get_token_request(headers)
    
    limit = 3
    statuses: list[int] = [
    STATUSES.get("Действует"),
    STATUSES.get("Приостановлен"),
    STATUSES.get("Частично приостановлен"),
    ]
    
    applicants_json = get_applicants_json(statuses, limit)
    
    applicants_id = [item.get("id") for item in applicants_json.get("items")]
    data = {
        "statuses": statuses,
        "limit": limit,
        "applicants_id": applicants_id,
    }
    applicants_file = write_json(data, "applicants_id")
    
    if applicants_file.exists():
        with open(applicants_file, "r", encoding="utf-8") as file:
            applicants_id = json.load(file).get("applicants_id")
    
    d = {}
    
    for applicant_id in applicants_id:
        applicant_json = get_applicant_by_id(applicant_id)
        
        accredited_person = AccreditedPerson.create_accredited_person(applicant_json)
        
        accreditation = Accreditation.create_accreditation(applicant_json)
        
        applicant = Applicant.create_applicant(applicant_json, accredited_person, accreditation)
        
        serialized_applicant = applicant.model_dump()
        d[applicant_id] = serialized_applicant
    
    write_json(d, "dirt_data")
    
    print("done!")
    
if __name__ == "__main__":
    main()
