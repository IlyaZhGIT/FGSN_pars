from typing import Any, List, Optional

from pydantic import BaseModel, Field


class ApplicantDTO(BaseModel):
    id: int
    id_type: int = Field(..., alias="idType")
    name_type: str = Field(..., alias="nameType")
    id_status: int = Field(..., alias="idStatus")
    name_status: str = Field(..., alias="nameStatus")
    name_type_activity: str = Field(..., alias="nameTypeActivity")
    ids_type_activity: Any = Field(..., alias="idsTypeActivity")
    reg_number: str = Field(..., alias="regNumber")
    reg_date: str = Field(..., alias="regDate")
    full_name: str = Field(..., alias="fullName")
    address: str
    federal_district: str = Field(..., alias="federalDistrict")
    fa_country: Any = Field(..., alias="faCountry")
    fa_name: Any = Field(..., alias="faName")
    fa_name_eng: Any = Field(..., alias="faNameEng")
    solution_number: Any = Field(..., alias="solutionNumber")
    unique_register_number: Any = Field(..., alias="uniqueRegisterNumber")
    fa_id_status: Any = Field(..., alias="faIdStatus")
    has_eng_version: bool = Field(..., alias="hasEngVersion")
    full_name_eng: str = Field(..., alias="fullNameEng")
    short_name_eng: Any = Field(..., alias="shortNameEng")
    head_full_name_eng: str = Field(..., alias="headFullNameEng")
    address_eng: str = Field(..., alias="addressEng")
    applicant_full_name_eng: str = Field(..., alias="applicantFullNameEng")
    applicant_inn: str = Field(..., alias="applicantInn")
    applicant_full_name: str = Field(..., alias="applicantFullName")
    oa_description: Any = Field(..., alias="oaDescription")
    oa_description_eng: Any = Field(..., alias="oaDescriptionEng")
    combined_sign_id: Any = Field(..., alias="combinedSignId")
    is_government_company: bool | None = Field(..., alias="isGovernmentCompany")
    insert_national_part_name: Any = Field(..., alias="insertNationalPartName")


class Person(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    name_eng: str = Field(..., alias="nameEng")
    surname_eng: str = Field(..., alias="surnameEng")
    patronymic_eng: str = Field(..., alias="patronymicEng")
    inn: Any
    addresses: List
    contacts: List


class Address(BaseModel):
    id: int
    id_type: int = Field(..., alias="idType")
    id_code_oksm: Any = Field(..., alias="idCodeOksm")
    id_subject: Any = Field(..., alias="idSubject")
    id_district: Any = Field(..., alias="idDistrict")
    id_city: Any = Field(..., alias="idCity")
    zato: bool
    id_locality: Any = Field(..., alias="idLocality")
    id_street: Any = Field(..., alias="idStreet")
    id_house: Any = Field(..., alias="idHouse")
    flat: Any
    post_code: Any = Field(..., alias="postCode")
    unique_address: Any = Field(..., alias="uniqueAddress")
    full_address: str = Field(..., alias="fullAddress")
    alien_district: Any = Field(..., alias="alienDistrict")
    alien_city: Any = Field(..., alias="alienCity")
    alien_locality: Any = Field(..., alias="alienLocality")
    alien_street: Any = Field(..., alias="alienStreet")
    alien_house: Any = Field(..., alias="alienHouse")
    full_address_eng: str = Field(..., alias="fullAddressEng")
    id_file_scan: Any = Field(..., alias="idFileScan")


class Contact(BaseModel):
    id_type: int = Field(..., alias="idType")
    value: str
    ord: int
    id: int


class Applicant(BaseModel):
    id: int
    id_type: int = Field(..., alias="idType")
    id_egrulip: int = Field(..., alias="idEgrulip")
    person: Person
    full_name: str = Field(..., alias="fullName")
    short_name: str = Field(..., alias="shortName")
    full_name_eng: str = Field(..., alias="fullNameEng")
    short_name_eng: Any = Field(..., alias="shortNameEng")
    tax_authority_name: str = Field(..., alias="taxAuthorityName")
    tax_authority_reg_date: str = Field(..., alias="taxAuthorityRegDate")
    head_post: str = Field(..., alias="headPost")
    ogrn: str
    inn: str
    kpp: str
    id_legal_form: int = Field(..., alias="idLegalForm")
    id_kopf: Any = Field(..., alias="idKopf")
    name_legal_form: str = Field(..., alias="nameLegalForm")
    info: Any
    is_government_company: bool = Field(..., alias="isGovernmentCompany")
    addresses: List[Address]
    brand_name: str = Field(..., alias="brandName")
    sum_of_charter_capital: Any = Field(..., alias="sumOfCharterCapital")
    ownership: Any
    ownership_additional_text: Any = Field(..., alias="ownershipAdditionalText")
    contacts: List[Contact]
    alien: bool


class TechnicalExpert(BaseModel):
    id: int
    id_expert: int = Field(..., alias="idExpert")
    fio: str


class ExpertGroup(BaseModel):
    id: int
    id_expert: int = Field(..., alias="idExpert")
    expert_reg_number: str = Field(..., alias="expertRegNumber")
    expert_fio: str = Field(..., alias="expertFio")
    id_expert_organization: int = Field(..., alias="idExpertOrganization")
    expert_organization_name: str = Field(..., alias="expertOrganizationName")
    technical_experts: List[TechnicalExpert] = Field(..., alias="technicalExperts")


class AccredScopeUnstructItem(BaseModel):
    id: int
    national_part_regulations: List = Field(..., alias="nationalPartRegulations")
    national_part_tn_ved: List = Field(..., alias="nationalPartTnVed")
    metrolog_sizers: List = Field(..., alias="metrologSizers")
    okpd2: List
    okved2: List
    regulations_rf: List = Field(..., alias="regulationsRf")
    regulations_ts: List = Field(..., alias="regulationsTs")
    business_line: List = Field(..., alias="businessLine")
    scan: List
    tn_ved: List = Field(..., alias="tnVed")
    oa_description: Any = Field(..., alias="oaDescription")
    oa_description_eng: Any = Field(..., alias="oaDescriptionEng")
    pressmark: Any
    oa_description_np: Any = Field(..., alias="oaDescriptionNp")
    code_tn_ved_np: Any = Field(..., alias="codeTnVedNp")
    code_okved2: Any = Field(..., alias="codeOkved2")
    code_okpd2: Any = Field(..., alias="codeOkpd2")
    right: Any
    code_tn_ved: Any = Field(..., alias="codeTnVed")
    code_okp: Any = Field(..., alias="codeOkp")
    code_okpd: Any = Field(..., alias="codeOkpd")
    code_okun: Any = Field(..., alias="codeOkun")
    acc_not_approved: bool = Field(..., alias="accNotApproved")
    comments: Any
    national_part_product_list: List = Field(..., alias="nationalPartProductList")
    accred_persons_aa: List = Field(..., alias="accredPersonsAA")
    accred_experts_aa: List = Field(..., alias="accredExpertsAA")
    other_persons_aa: List = Field(..., alias="otherPersonsAA")
    technical_experts_aa: List = Field(..., alias="technicalExpertsAA")


class AccredScopeUnstructList(BaseModel):
    id: int
    accred_scope_unstruct: List[AccredScopeUnstructItem] = Field(
        ..., alias="accredScopeUnstruct"
    )


class AccredPersonsAaItem(BaseModel):
    id: int
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    patronymic: str
    post: str
    file: str


class AccredExpertsAaItem(BaseModel):
    id: int
    first_name: str = Field(..., alias="firstName")
    last_name: Any = Field(..., alias="lastName")
    patronymic: Any
    rea_link: str = Field(..., alias="reaLink")
    reg_id: Any = Field(..., alias="regId")
    file: str


class TechnicalExpertsAaItem(BaseModel):
    id: int
    first_name: str = Field(..., alias="firstName")
    last_name: Any = Field(..., alias="lastName")
    patronymic: Any
    rte_link: str = Field(..., alias="rteLink")
    reg_id: Any = Field(..., alias="regId")
    file: str


class Accreditation(BaseModel):
    audit_change_date: str = Field(..., alias="auditChangeDate")
    audit_fio: Any = Field(..., alias="auditFio")
    audit_publish_date: str = Field(..., alias="auditPublishDate")
    audit_publish_fio: Any = Field(..., alias="auditPublishFio")
    id: int
    decision_number: str = Field(..., alias="decisionNumber")
    decision_date: str = Field(..., alias="decisionDate")
    info: Any
    id_accred_scope_file: str = Field(..., alias="idAccredScopeFile")
    expert_group: ExpertGroup = Field(..., alias="expertGroup")
    tr_ids: List = Field(..., alias="trIds")
    accred_scope_unstruct_list: AccredScopeUnstructList = Field(
        ..., alias="accredScopeUnstructList"
    )
    accred_persons_aa: List[AccredPersonsAaItem] = Field(..., alias="accredPersonsAA")
    accred_experts_aa: List[AccredExpertsAaItem] = Field(..., alias="accredExpertsAA")
    other_persons_aa: List = Field(..., alias="otherPersonsAA")
    technical_experts_aa: List[TechnicalExpertsAaItem] = Field(
        ..., alias="technicalExpertsAA"
    )


class HeadPerson(BaseModel):
    id: int
    name: str
    surname: str
    patronymic: str
    name_eng: str = Field(..., alias="nameEng")
    surname_eng: str = Field(..., alias="surnameEng")
    patronymic_eng: str = Field(..., alias="patronymicEng")
    inn: Any
    addresses: List
    contacts: List[Contact]

    def __repr__(self) -> str:
        return "%s %s %s" % (self.name, self.surname, self.patronymic)


class RegNumber(BaseModel):
    id: int
    reg_number: str = Field(..., alias="regNumber")
    begin_date: str = Field(..., alias="beginDate")
    end_date: Any = Field(..., alias="endDate")
    active: bool


class Change(BaseModel):
    audit_change_date: str = Field(..., alias="auditChangeDate")
    audit_fio: Any = Field(..., alias="auditFio")
    audit_publish_date: Optional[str] = Field(..., alias="auditPublishDate")
    audit_publish_fio: Any = Field(..., alias="auditPublishFio")
    id: int
    ap_id: int = Field(..., alias="apId")
    id_type: int = Field(..., alias="idType")
    decision_number: Optional[str] = Field(..., alias="decisionNumber")
    decision_date: Optional[str] = Field(..., alias="decisionDate")


class ActualInfoNationalPart(BaseModel):
    service_number: Any = Field(..., alias="serviceNumber")
    service_date: Any = Field(..., alias="serviceDate")
    decision_number: Any = Field(..., alias="decisionNumber")
    decision_date: Any = Field(..., alias="decisionDate")
    actual_service_number: Any = Field(..., alias="actualServiceNumber")
    actual_service_date: Any = Field(..., alias="actualServiceDate")
    actual_decision_number: Any = Field(..., alias="actualDecisionNumber")
    actual_decision_date: Any = Field(..., alias="actualDecisionDate")
    accred_scope_unstruct_list: AccredScopeUnstructList = Field(
        ..., alias="accredScopeUnstructList"
    )


class ApplicantResponse(BaseModel):
    create_date: str = Field(..., alias="createDate")
    id: int
    applicant: Applicant
    accreditation: Accreditation
    accreditation_before: List = Field(..., alias="accreditationBefore")
    id_type: int = Field(..., alias="idType")
    id_status: int = Field(..., alias="idStatus")
    full_name: str = Field(..., alias="fullName")
    short_name: str = Field(..., alias="shortName")
    head_person: HeadPerson = Field(..., alias="headPerson")
    snils: Any
    head_post: str = Field(..., alias="headPost")
    end_date: Any = Field(..., alias="endDate")
    public_date: str = Field(..., alias="publicDate")
    reg_date: str = Field(..., alias="regDate")
    last_update: str = Field(..., alias="lastUpdate")
    has_eng_version: bool = Field(..., alias="hasEngVersion")
    full_name_eng: str = Field(..., alias="fullNameEng")
    short_name_eng: Any = Field(..., alias="shortNameEng")
    head_post_eng: str = Field(..., alias="headPostEng")
    id_file_acc_description_eng: Any = Field(..., alias="idFileAccDescriptionEng")
    acc_description_scope_eng: Any = Field(..., alias="accDescriptionScopeEng")
    contacts: List[Contact]
    foreing_accreditations: List = Field(..., alias="foreingAccreditations")
    addresses: List[Address]
    licenses: List
    reg_numbers: List[RegNumber] = Field(..., alias="regNumbers")
    changes: List[Change]
    accred_person_changes: List = Field(..., alias="accredPersonChanges")
    address_changes: List = Field(..., alias="addressChanges")
    attestat_changes: List = Field(..., alias="attestatChanges")
    confirm_competence_changes: List = Field(..., alias="confirmCompetenceChanges")
    confirm_competence_next_id_type: int = Field(
        ..., alias="confirmCompetenceNextIdType"
    )
    confirm_competence_next_date: str = Field(..., alias="confirmCompetenceNextDate")
    control_changes: List = Field(..., alias="controlChanges")
    cut_accred_scope_changes: List = Field(..., alias="cutAccredScopeChanges")
    extend_accred_scope_changes: List = Field(..., alias="extendAccredScopeChanges")
    exclude_national_part_changes: List = Field(..., alias="excludeNationalPartChanges")
    insert_national_part_changes: List = Field(..., alias="insertNationalPartChanges")
    extend_national_part_changes: List = Field(..., alias="extendNationalPartChanges")
    reduce_national_part_changes: List = Field(..., alias="reduceNationalPartChanges")
    suspension_changes: List = Field(..., alias="suspensionChanges")
    termination_changes: List = Field(..., alias="terminationChanges")
    resumption_changes: List = Field(..., alias="resumptionChanges")
    full_validate: bool = Field(..., alias="fullValidate")
    accred_scope_unstruct_list: Any = Field(..., alias="accredScopeUnstructList")
    partners_info: List = Field(..., alias="partnersInfo")
    tech_reg_rf: Any = Field(..., alias="techRegRf")
    tech_reg_ts: Any = Field(..., alias="techRegTs")
    id_acc_standard: List[int] = Field(..., alias="idAccStandard")
    combined_sign_id: Any = Field(..., alias="combinedSignId")
    combined_sign_date: Any = Field(..., alias="combinedSignDate")
    cert_organ_test_lab_entities: List = Field(..., alias="certOrganTestLabEntities")
    is_accred_scope_unstruct: bool = Field(..., alias="isAccredScopeUnstruct")
    insert_national_part: bool = Field(..., alias="insertNationalPart")
    actual_info_national_part: ActualInfoNationalPart = Field(
        ..., alias="actualInfoNationalPart"
    )


class ApplicationResponse(BaseModel):
    items: list[ApplicantDTO]
    total: int
    size: int
