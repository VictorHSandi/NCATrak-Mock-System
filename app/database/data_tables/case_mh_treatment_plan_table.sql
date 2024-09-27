CREATE TABLE case_mh_treatment_plan (
    treatment_plan_id INTEGER PRIMARY KEY,
    cac_id SMALLINT NOT NULL,
    case_id INTEGER NOT NULL,
    authorized_status_id INTEGER,
    duration INTEGER,
    duration_unit VARCHAR(255),
    planned_start_date DATE,
    planned_end_date DATE,
    planned_review_date DATE,
    provider_agency_id INTEGER,
    provider_employee_id INTEGER,
    treatment_model_id INTEGER,
    treatment_plan_date DATE,
    FOREIGN KEY(cac_id) REFERENCES child_advocacy_center(cac_id),
    FOREIGN KEY(case_id) REFERENCES cac_case(case_id),
    FOREIGN KEY(provider_agency_id) REFERENCES cac_agency(agency_id),
    FOREIGN KEY(provider_employee_id) REFERENCES employee(employee_id),
    FOREIGN KEY(treatment_model_id) REFERENCES case_mh_treatment_model(treatment_model_id)
);