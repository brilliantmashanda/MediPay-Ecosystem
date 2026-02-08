package com.medipay.model;

import jakarta.persistence.*;
import lombok.Data;
import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "medical_claims")
@Data // Generates getters, setters, equals, hashCode, and toString
public class MedicalClaim {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "patient_name", nullable = false)
    private String patientName;

    @Column(name = "patient_surname", nullable = false)
    private String patientSurname;

    @Column(name = "claim_amount", nullable = false, precision = 10, scale = 2)
    private BigDecimal claimAmount;

    @Column(name = "provider_name")
    private String providerName;

    @Column(name = "provider_no", nullable = false)
    private String providerNo;

    @Column(length = 50)
    private String status = "PENDING";

    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @Column(name = "effective_start_date")
    private LocalDateTime effectiveStartDate = LocalDateTime.now();

    // Note: Mapping to match your SQL typo "efective" to ensure it connects
    @Column(name = "efective_end_date")
    private LocalDateTime effectiveEndDate;
}