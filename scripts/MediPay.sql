-- The main Claims table
CREATE TABLE medical_claims (
    id SERIAL PRIMARY KEY,
    patient_name VARCHAR(255) NOT NULL,
    patient_surname VARCHAR(255) NOT NULL,
    claim_amount DECIMAL(10, 2) NOT NULL,
    provider_name VARCHAR(255), -- e.g., Netcare, Mediclinic
    provider_no VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'PENDING', -- PENDING, APPROVED, REJECTED
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    effective_start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    efective_end_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- The Audit table (For your "Audit Logs" skill)
CREATE TABLE claims_audit_log (
    log_id SERIAL PRIMARY KEY,
    claim_id INT,
    old_status VARCHAR(50),
    new_status VARCHAR(50),
    changed_by VARCHAR(100),
    change_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION log_status_change()
RETURNS TRIGGER AS $$
BEGIN
    IF (OLD.status <> NEW.status) THEN
        INSERT INTO claims_audit_log(claim_id, old_status, new_status, changed_by)
        VALUES (OLD.id, OLD.status, NEW.status, current_user);
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_claims_status_audit
AFTER UPDATE ON medical_claims
FOR EACH ROW
EXECUTE FUNCTION log_status_change();