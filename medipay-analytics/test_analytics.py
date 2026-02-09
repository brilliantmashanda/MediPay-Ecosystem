import pandas as pd
import pytest
from app import calculate_summary

def test_calculate_summary():
    # Create mock data that matches the full schema expected by app.py
    data = {
        'claim_amount': [100.0, 200.0],
        'status': ['APPROVED', 'PENDING'],
        'provider_name': ['Netcare', 'Mediclinic']
    }
    df = pd.DataFrame(data)

    # Run logic
    result = calculate_summary(df)

    # Assertions
    assert result['total_claims'] == 2
    assert result['total_value'] == 300.0
    assert result['status_counts']['APPROVED'] == 1