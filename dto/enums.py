from enum import IntEnum, Enum


class ItemNameParam(Enum):
    APPLICANT_TYPE = "guApType"
    CONFIRM_RESULT_TYPE = "typeResultOfConfirm"


class Status(IntEnum):
    ARCHIVED = 1
    ACTIVE = 6
    DISCONTINUED = 14
    STOPPED = 15
    PARTIAL_STOPPED = 19
