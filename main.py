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
    addres: str

    full_name: str
    mail: str
    phone: str


@dataclass
class Accreditation:
    full_name: str
    confirmation_of_competence: str | None


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
            stasuses = []
        self.statuses = statuses
        self.limit = limit

        self.applicants_json = self.get_applicants()
        self.token = Applicants_req.get_token_request()

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


# req1 = req("https://pub.fsa.gov.ru/api/v1/ral/common/showcases/get", json_data)
# pprint(req1)


# for applicant in applicants_id:
#     response = requests.get(
#         f"https://pub.fsa.gov.ru/api/v1/ral/common/companies/{applicant}",
#         cookies=cookies,
#         headers=headers,
#         timeout=15,
#     )
#     res_j = response.json()


#     regNumber = res_j.get("regNumbers")[0].get("regNumber")

#     inn = res_j.get("inn")

#     shortName = res_j.get("shortName")

#     applicant = res_j.get('applicant')
#     person = applicant.get('person')
#     full_name = f"{person.get("name")} {person.get("surname")} {person.get("patronymic")}"

#     contacts = applicant.get("contacts")
#     phone = contacts[0].get("value")
#     mail = contacts[2].get("value")

#     addres = applicant.get("addresses")[0].get("fullAddress")


#     #AccreditedPerson
#     id_type = res_j.get("idType") # передать для получаения наименования типа
#     name_type = ...
#     shortName = res_j.get("shortName")
#     addres = res_j.get("addresses")[0].get("fullAddress")

#     head_person = res_j.get("headPerson")
#     full_name = f"{head_person.get("name")} {head_person.get("surname")} {head_person.get("patronymic")}"
#     phone = res_j.get("contacts")[0].get("value")
#     mail = res_j.get("contacts")[1].get("value")

#     accredited_person = AccreditedPerson(type_person=name_type, name=shortName, addres=addres, full_name=full_name, mail=mail, phone=phone)

#     accreditation = Accreditation()

#     Applicant(ral=regNumber, inn=inn, applicant=shortName, full_name=full_name,mail=mail, phone=phone, addres=addres, accreditation=accreditation, accredited_person=accredited_person)


# #Обращение за названием типа по id
# # json_data = {
# #     "items": {
# #         "guApType": [
# #             {
# #                 "id": [
# #                     5,
# #                 ],
# #                 "fields": [
# #                     "id",
# #                     "masterId",
# #                     "name",
# #                 ],
# #             },
# #         ],
# #     }
# # }

# # response = requests.post(
# #     "https://pub.fsa.gov.ru/nsi/api/multi",
# #     cookies=cookies,
# #     headers=headers,
# #     json=json_data,
# # )

# # pprint(response.text)
