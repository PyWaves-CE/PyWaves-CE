# Test Funding List - WAVES Amounts

This document lists the amount of WAVES funded to each test via `prepareTestcase()`.  
Note: Amounts are in base units where 1 WAVES = 100,000,000 base units.  
Default amount (if not specified) = 1,000,000 base units (0.01 WAVES).

## Test Files and Funding Amounts

| Test File | Base Units | WAVES | Notes |
|-----------|------------|-------|-------|
| test_AddressCreation.py | N/A | N/A | No `prepareTestcase()` call - uses direct address creation |
| test_AddressScript.py | 100,000,000 | 1.0 | |
| test_Alias.py | 1,000,000 | 0.01 | Default amount |
| test_BurnAsset.py | 1,000,000 | 0.01 | Default amount |
| test_CancelLease.py | 1,000,000 | 0.01 | Default amount |
| test_Data.py | 100,000,000 | 1.0 | |
| test_InvokeScript.py | 100,000,000 | 1.0 | Also sends tokens |
| test_IssueAsset.py | 101,000,000 | 1.01 | |
| test_IssueSmartAsset.py | 101,000,000 | 1.01 | |
| test_Lease.py | 100,000,000 | 1.0 | |
| test_MassTransferAsset.py | 101,000,000 | 1.01 | Also sends tokens |
| test_MassTransferWaves.py | 1,000,000 | 0.01 | Default amount |
| test_MultiSignature.py | 200,000,000 | 2.0 | |
| test_Oracle.py | 1,500,000 | 0.015 | |
| test_ReissueAsset.py | 100,000 | 0.001 | Uses faucet directly - no `prepareTestcase()` call |
| test_SendAsset.py | 1,000,000 | 0.01 | Default amount, also sends tokens |
| test_SendWaves.py | 1,000,000 | 0.01 | Default amount |
| test_SetAssetScript.py | 310,000,000 | 3.1 | Highest funding amount |
| test_SetScript.py | 1,500,000 | 0.015 | |
| test_SponsorAsset.py | 201,000,000 | 2.01 | |
| test_Trading.py | 200,000,000 | 2.0 | Also sends tokens |
| test_UpdateAssetInfo.py | 100,000 | 0.001 | Uses faucet directly - no `prepareTestcase()` call |
| test_WavesBalance.py | 100,000,000 | 1.0 | |
| test_Evaluate.py | 100,000,000 | 0.01 | Default Amount|

## Conversion Reference

- 1 WAVES = 100,000,000 base units
- Default amount = 1,000,000 base units = 0.01 WAVES

