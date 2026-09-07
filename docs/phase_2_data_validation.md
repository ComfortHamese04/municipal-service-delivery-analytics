# Phase 2A data-validation report

## Outcome

The project can proceed, but the sources support different analytical levels and update frequencies. The portfolio solution will combine national/provincial service-access context with a detailed Cape Town case study and live project-owned intervention tracking.

## Confirmed scope decisions

1. City of Cape Town is the detailed case study.
2. Municipal Money is the financial source and will use v2 datasets for 2019/20 onward where available.
3. Stats SA GHS 2025 is the current annual survey source; its weights and metadata are mandatory.
4. Cape Town Household Survey/open-data resources provide the preferred suburb-level basic-services context.
5. Public data uses scheduled incremental refreshes. Only the future C# intervention application supplies immediate operational updates.
6. Raw external datasets will not be committed to GitHub.

## Business-question feasibility

| Question | Current feasibility | Evidence needed next |
|---|---|---|
| BQ01: largest service gaps | Feasible | GHS weighted fields and Cape Town basic-services data |
| BQ02: repeated service requests | Conditional | Exact public service-request resource with dates, categories and geography |
| BQ03: resolution delays | Conditional | Created/closed timestamps and suitable request attributes |
| BQ04: spending aligned with needs | Feasible with careful interpretation | Municipal Money v2 finance facts plus compatible geographic/time outcomes |
| BQ05: disadvantaged groups | Feasible at survey-supported geography | GHS weights, household attributes and Cape Town survey variables |
| BQ06: intervention improvement | Planned | Project-owned intervention and KPI observations after Phase 5 |

## Quality tests for Phase 2B

- File/API availability and HTTP result
- Schema snapshot and type inference
- Row and column counts
- Candidate-key uniqueness
- Duplicate rows
- Required-field completeness
- Valid date and financial-period ranges
- Municipality code validity, including `CPT`
- Survey weight validity and missing-value conventions
- Spatial geometry validity and coordinate reference system
- Source-to-Bronze checksum reconciliation
- Quarantine count and reason
- Latest source timestamp and ingestion latency

## GitHub readiness controls

- Repository paths use lowercase and underscores where appropriate.
- No secrets or raw datasets are versioned.
- Environment-variable examples contain no credentials.
- Installation, tests and source validation are documented.
- CI runs linting and unit tests on pushes and pull requests.
- Dataset licences remain separate from the MIT licence covering project code.

## Phase 2B acceptance criteria

- At least one representative dataset from Treasury, Stats SA and Cape Town is downloaded by a reproducible connector.
- Every download has a manifest containing retrieval time, byte size, checksum and source metadata.
- A profiling report describes schema, nulls, duplicates, keys and coverage.
- Invalid records are quarantined with machine-readable reasons.
- Source field names map to proposed warehouse fields.
- Each business question is marked confirmed, revised or deferred based on actual columns.
