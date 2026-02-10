package com.medipay.service;

import com.medipay.model.MedicalClaim;
import com.medipay.repository.ClaimRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.jms.core.JmsTemplate;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ClaimService {
    @Autowired
    private ClaimRepository claimRepository;
    @Autowired
    private JmsTemplate jmsTemplate;

    public List<MedicalClaim> getAllClaims() {
        return claimRepository.findAll();
    }

    public MedicalClaim saveClaim(MedicalClaim claim) {
        return claimRepository.save(claim);
    }

    public MedicalClaim approveClaim(Long id) {
        MedicalClaim claim = claimRepository.findById(id).orElseThrow();
        claim.setStatus("APPROVED");
        MedicalClaim savedClaim = claimRepository.save(claim);

        // Send message to Python Analytics asynchronously
        String message = "Claim Approved: " + savedClaim.getId() + " Amount: " + savedClaim.getClaimAmount();
        jmsTemplate.convertAndSend("claims-queue", message);

        return savedClaim;
    }
}