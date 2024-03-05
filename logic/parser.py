import json
import requests
import os
from dataclasses import dataclass

from fake_useragent import UserAgent

from dto.enums import ItemNameParam, Status


@dataclass
class User:
    username: str
    password: str


class Extractor:
    def __init__(self, user):
        self._user = user
        _ua = UserAgent()
        self._headers = {"UserAgent": _ua.chrome}
        token = self._get_token()
        self._headers.update({"Authorization": token})

    def _get_token(self) -> str:
        json_data = {
            "username": self._user.username,
            "password": self._user.password,
        }
        response = requests.post(
            "https://pub.fsa.gov.ru/login",
            headers=self._headers,
            json=json_data,
            timeout=15,
        )
        token = response.headers.get("Authorization")
        if token:
            return token
        raise ValueError("Token not accessible")

    def get_applicants_json(self, statuses: list[Status], limit: int):
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
            headers=self._headers,
            json=json_data,
            timeout=15,
        )
        if response.status_code == 200:
            return response.json()
        raise ValueError(
            f"An unsuccessful response was received {response.status_code}"
        )

    def get_applicant_by_id(self, id_: str):
        response = requests.get(
            f"https://pub.fsa.gov.ru/api/v1/ral/common/companies/{id_}",
            headers=self._headers,
            timeout=15,
        )
        if response.status_code == 200:
            return response.json()
        raise ValueError(
            f"An unsuccessful response was received {response.status_code}"
        )

    def get_multi_nsi_by_id(self, item: str, type_id: int) -> str:
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
            headers=self._headers,
            json=json_data,
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
        raise ValueError(
            f"An unsuccessful response was received {response.status_code}"
        )
        # return response.json().get(item)[0].get("name")


def write_json(data: list[dict], file_name: str) -> os.PathLike:
    file_path = f"{file_name}.json"
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    return file_path
