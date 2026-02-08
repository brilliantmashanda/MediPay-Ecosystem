package com.medipay.repository;

import com.medipay.model.MedicalClaim;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface ClaimRepository extends JpaRepository<MedicalClaim, Long> {
    // You can add custom queries here later, like finding claims by status
}