package com.medipay.service;

import com.medipay.model.MedicalClaim;
import com.medipay.repository.ClaimRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
// IMPORT THIS:
import org.springframework.jms.core.JmsTemplate;

import java.util.Optional;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class ClaimServiceTest {

    @Mock
    private ClaimRepository claimRepository;

    @Mock
    private JmsTemplate jmsTemplate;

    @InjectMocks
    private ClaimService claimService;

    @Test
    public void testApproveClaim() {
        MedicalClaim mockClaim = new MedicalClaim();
        mockClaim.setId(1L);
        mockClaim.setStatus("PENDING");

        when(claimRepository.findById(1L)).thenReturn(Optional.of(mockClaim));
        when(claimRepository.save(any(MedicalClaim.class))).thenReturn(mockClaim);

        MedicalClaim result = claimService.approveClaim(1L);

        assertEquals("APPROVED", result.getStatus());
    }
}