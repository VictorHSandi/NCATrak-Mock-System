CREATE TABLE cac_case (
    cac_id SMALLINT NOT NULL,
    case_id INTEGER PRIMARY KEY,
    case_number VARCHAR(20),
    cac_received_date DATE,
    case_closed_date DATE,
    closed_reason_id INTEGER,
    created_date DATE,
    mh_lead_employee_id INTEGER,
    mh_agency_id INTEGER,
    mh_case_number VARCHAR(20),
    mh_mdt_ready BOOLEAN,
    mh_na BOOLEAN,
    mh_referral_agency_id INTEGER,
    mh_referral_date DATE,
    mh_therapy_accepted BOOLEAN,
    mh_therapy_complete_date DATE,
    mh_therapy_end_reason_id INTEGER,
    mh_therapy_offered_date DATE,
    mh_therapy_record_created BOOLEAN,
    va_agency_id INTEGER,
    va_case_number VARCHAR(20),
    va_claim_denied_reason VARCHAR(200),
    va_claim_number VARCHAR(20),
    va_claim_status_id INTEGER,
    va_have_birth_cert BOOLEAN,
    va_has_police_report BOOLEAN,
    va_mdt_ready BOOLEAN,
    va_na BOOLEAN,
    va_referral_agency_id INTEGER,
    va_referral_date DATE,
    va_services_accepted BOOLEAN,
    va_services_offered_date DATE,
    va_services_end_date DATE,
    FOREIGN KEY(cac_id) REFERENCES child_advocacy_center(cac_id),
    FOREIGN KEY(mh_agency_id) REFERENCES cac_agency(agency_id),
    FOREIGN KEY(mh_referral_agency_id) REFERENCES cac_agency(agency_id),
    FOREIGN KEY(va_agency_id) REFERENCES cac_agency(agency_id),
    FOREIGN KEY(va_referral_agency_id) REFERENCES cac_agency(agency_id)
);