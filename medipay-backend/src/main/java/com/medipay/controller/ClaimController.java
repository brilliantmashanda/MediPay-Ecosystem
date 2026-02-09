package com.medipay.controller;

import com.medipay.model.MedicalClaim;
import com.medipay.repository.ClaimRepository;
import com.medipay.service.ClaimService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/claims")
@CrossOrigin(origins = "*")
public class ClaimController {

    @Autowired
    private ClaimService claimService;

    @GetMapping
    public List<MedicalClaim> getAllClaims() {
        return claimService.getAllClaims();
    }

    @PostMapping
    public MedicalClaim submitClaim(@RequestBody MedicalClaim claim) {
        return claimService.saveClaim(claim);
    }

    @PutMapping("/{id}/status")
    public MedicalClaim updateStatus(@PathVariable Long id, @RequestParam String status) {
        if ("APPROVED".equalsIgnoreCase(status)) {
            return claimService.approveClaim(id);
        }
        return null;
    }
}