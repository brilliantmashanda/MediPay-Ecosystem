package com.medipay.service;

import com.medipay.model.MedicalClaim;
import com.medipay.repository.ClaimRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ClaimService {
    @Autowired
    private ClaimRepository claimRepository;

    public List<MedicalClaim> getAllClaims() {
        return claimRepository.findAll();
    }

    public MedicalClaim saveClaim(MedicalClaim claim) {
        return claimRepository.save(claim);
    }

    public MedicalClaim approveClaim(Long id) {
        MedicalClaim claim = claimRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Claim not found"));
        claim.setStatus("APPROVED");
        return claimRepository.save(claim);
    }
}