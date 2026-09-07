# Data-source register

Validated on 7 September 2026. “Validated” means the official landing page, purpose and access method were confirmed. It does not mean that every record is complete or analytically suitable.

| ID | Source | Provider | Access | Frequency | Intended use | Validation decision |
|---|---|---|---|---|---|---|
| DS01 | Municipal Money API | South African National Treasury / Municipal Money | JSON API and bulk files | Quarterly snapshots | Budget, expenditure, capital acquisition, repairs, debtors and financial indicators | Accept; retain publication/version metadata and test completeness |
| DS02 | General Household Survey 2025 | Statistics South Africa | CSV, metadata and questionnaire | Annual | Weighted household access to water, sanitation, electricity and refuse services | Accept for national/provincial context; confirm smallest defensible geography from metadata |
| DS03 | Cape Town Open Data Portal | City of Cape Town | CSV, ArcGIS REST and GIS files | Dataset-dependent | Detailed Cape Town basic services, boundaries and infrastructure context | Accept conditionally; register each exact dataset and terms before ingestion |
| DS04 | Cape Town Household Survey | City of Cape Town | Published open-data resources; fuller researcher dataset by request | Every two to three years is planned | Suburb-level household characteristics and basic-services case study | Accept published de-identified resources; do not assume access to restricted detail |
| DS05 | Intervention Tracker | Project-owned C# application | REST API and SQL database | Immediate | Corrective actions, owners, dates, targets and outcomes | Planned for Phase 5 |

## Required metadata per ingested dataset

- Source and exact resource URL
- Provider and dataset title
- Retrieval timestamp in UTC
- Publication or update date
- File format, byte size and SHA-256 checksum
- Licence or terms URL
- Schema and data dictionary version
- Geographic and time coverage
- Expected grain and candidate key
- Missing, invalid and duplicate record counts
- Known limitations and permitted use

## Evidence limitations

- Municipal Money states that completeness and trustworthiness depend on municipal submissions. Recent figures may still be under verification.
- Finance datasets changed with mSCOA from the 2019/20 financial year; v2 datasets should not be joined blindly to older versions.
- Survey estimates require the supplied weights. Raw row counts are not population estimates.
- GHS is appropriate for national/provincial context, but detailed municipal or suburb claims require a source whose sample design supports that geography.
- Cape Town portal refresh frequency and terms must be recorded separately for each selected resource.
- No public source should be described as real-time unless its documented publication method supports that claim.

## Official source pages

- Municipal Money API documentation: https://municipaldata.treasury.gov.za/docs
- Stats SA GHS portal: https://isibaloweb.statssa.gov.za/pages/surveys/pss/ghs/ghsp.php
- City of Cape Town Open Data Portal: https://www.capetown.gov.za/City-Connect/All-City-online-services/open-data-portal/
- City of Cape Town Household Survey: https://www.capetown.gov.za/general/city-survey
