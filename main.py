import json
from dataclasses import dataclass
from pathlib import Path
from pprint import pprint

import requests

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/24.1.0.0 Safari/537.36",
}

STATUSES = {
    "Архивный": 1,
    "Действует": 6,
    "Прекращен": 14,
    "Приостановлен": 15,
    "Частично приостановлен": 19,
}


@dataclass
class AccreditedPerson:
    type_person: str
    name: str
    address: str

    full_name: str
    mail: str
    phone: str

    @staticmethod
    def create_accredited_person(applicant_json) -> "AccreditedPerson":
        type_id = applicant_json.get("idType") # передать для получаения наименования типа
        name_type = get_accredited_person_name_type(type_id)
        shortName = applicant_json.get("shortName")
        address = applicant_json.get("addresses")[0].get("fullAddress")

        head_person = applicant_json.get("headPerson")
        full_name = f"{head_person.get("name")} {head_person.get("surname")} {head_person.get("patronymic")}"
        phone = applicant_json.get("contacts")[0].get("value")
        mail = applicant_json.get("contacts")[1].get("value")

        return AccreditedPerson(type_person=name_type, name=shortName, address=address, full_name=full_name, mail=mail, phone=phone)

@dataclass
class Accreditation:
    full_name: str
    confirmation_of_competence: str | None

    @staticmethod
    def create_application(applicant_json) -> "Accreditation":
        regNumber = applicant_json.get("regNumbers")[0].get("regNumber")

        inn = applicant_json.get("inn")

        shortName = applicant_json.get("shortName")

        applicant = applicant_json.get('applicant')
        person = applicant.get('person')
        full_name = f"{person.get("name")} {person.get("surname")} {person.get("patronymic")}"

        contacts = applicant.get("contacts")
        phone = contacts[0].get("value")
        mail = contacts[2].get("value")

        addres = applicant.get("addresses")[0].get("fullAddress")
        
        return Applicant(ral=regNumber, inn=inn, applicant=shortName, full_name=full_name,mail=mail, phone=phone, addres=addres, accreditation=accreditation, accredited_person=accredited_person)

@dataclass
class Applicant:
    ral: str
    inn: str
    applicant: str

    full_name: str
    mail: str
    phone: str
    addres: str

    accredited_person: AccreditedPerson
    accreditation: Accreditation

class Applicants_req:
    def __init__(self, limit: int = 10, statuses: list = None) -> None:
        if not stasuses:
            statuses = []
        self.statuses = statuses
        self.limit = limit

        self.token = Applicants_req.get_token_request()
        self.applicants_json = self.get_applicants()
        self.list_applicants_path = self.create_list_applicants()

    def get_applicants(self):
        headers["Authorization"] = self.token
        json_data = {
            "idStatus": self.statuses,
            "columns": [],
            "sort": [
                "-id",
            ],
            "limit": self.limit,
            "offset": 0,
            "numberOfAllRecords": False,
        }
        responce = requests.post(
            url="https://pub.fsa.gov.ru/api/v1/ral/common/showcases/get",
            headers=headers,
            json=json_data,
            timeout=15,
        )
        return responce.json()

    def create_list_applicants(self) -> Path:
        applicants_id = [item.get("id") for item in self.applicants_json.get("items")]
        data = {
            "statuses": self.statuses,
            "limit": self.limit,
            "applicants_id": applicants_id,
        }

        return Applicants_req.write_json(data, "applicants_id")

    @staticmethod
    def get_token_request() -> str:
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

    @staticmethod
    def write_json(data: list[dict], file_name: str) -> Path:
        file_path = f"{file_name}.json"
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

        return Path(file_path)


stasuses: list[int] = [
    STATUSES.get("Действует"),
    STATUSES.get("Приостановлен"),
    STATUSES.get("Частично приостановлен"),
]

obj = Applicants_req(statuses=stasuses)

if obj.list_applicants_path.exists():
    with open(obj.list_applicants_path, "r", encoding="utf-8") as file:
        applicants_id = json.loads(file).get("applicants_id")


def get_applicant_by_id(id: str):
    headers["Authorization"] = obj.token
    response = requests.get(
        f"https://pub.fsa.gov.ru/api/v1/ral/common/companies/{id}",
        headers=headers,
        timeout=15,
    )
    return response.json()

for applicant in applicants_id:
    applicant_json = get_applicant_by_id(applicant)
    accredited_person = AccreditedPerson.create_accredited_person(applicant_json)
    accreditation = Accreditation()

def get_accredited_person_name_type(type_id: int):
    headers["Authorization"] = obj.token
    json_data = {
        "items": {
            "guApType": [
                {
                    "id": [
                        type_id,
                    ],
                    "fields": [
                        "id",
                        "masterId",
                        "name",
                    ],
                },
            ],
        }
    }

    return requests.post(
        "https://pub.fsa.gov.ru/nsi/api/multi",
        headers=headers,
        json=json_data,
    )


