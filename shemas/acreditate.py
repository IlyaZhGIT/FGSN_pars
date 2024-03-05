from logic.parser import Extractor
from dto.enums import Status
from dto.entities import ApplicationResponse


class ApplicantHandler:
    def __init__(self, extractor: Extractor) -> None:
        self.extractor = extractor

    def get_list(self):
        statuses = [Status.ARCHIVED, Status.PARTIAL_STOPPED]
        applicants = self.extractor.get_applicants_json(statuses=statuses, limit=10)
        applicants = ApplicationResponse(**applicants)
