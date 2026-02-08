package com.medipay.controller;

import com.medipay.model.MedicalClaim;
import com.medipay.repository.ClaimRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/claims")
@CrossOrigin(origins = "*") // Allows your Angular app to talk to this later
public class ClaimController {

    @Autowired
    private ClaimRepository claimRepository;

    @GetMapping
    public List<MedicalClaim> getAllClaims() {
        return claimRepository.findAll();
    }

    @PostMapping
    public MedicalClaim submitClaim(@RequestBody MedicalClaim claim) {
        return claimRepository.save(claim);
    }

    @PutMapping("/{id}/status")
    public MedicalClaim updateStatus(@PathVariable Long id, @RequestParam String status) {
        MedicalClaim claim = claimRepository.findById(id).orElseThrow();
        claim.setStatus(status);
        return claimRepository.save(claim); // This will trigger your SQL Audit Log!
    }
}