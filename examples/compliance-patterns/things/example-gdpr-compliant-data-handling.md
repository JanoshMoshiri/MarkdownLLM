---
id: example-gdpr-compliant-data-handling
type: example
pattern_type: data-handling
demonstrates: compliance
applies_to: [client-matter, document-storage, communication, personal-data]
created: 2026-05-18
---

# GDPR Compliant: Data Handling Pattern

## The Pattern

A thing that handles personal data correctly within GDPR constraints:

```yaml
---
id: client-matter-smith-ltd
type: client-matter
data_classification: personal
data_residency_requirement: uk-only
access_control: [authorized-personnel-only]
data_minimization_check: true
audit_logging_enabled: true
retention_policy: legal-hold-7-years
created: 2026-05-18
---

# Smith Ltd Matter

## Sensitive Data Involved
This thing involves personal data of clients and third parties.

## Data Handling Approach
- All data processed within UK infrastructure only
- Access restricted to authorized personnel
- Complete audit log of who accessed what and when
- Minimum retention: legal hold period (7 years)
- Deletion procedure defined in retention_policy
```

## Why This Matters

### Lens 1: Domain Logic ✓
Creates a client matter with all necessary information to support legal work.

### Lens 2: Compliance Logic ✓
- `data_classification: personal` — Declares this thing contains personal data (triggers GDPR requirements)
- `data_residency_requirement: uk-only` — Ensures only UK-authorized LLMs and processors handle it
- `access_control: [authorized-personnel-only]` — Enforces principle of least privilege
- `data_minimization_check: true` — Confirms we're only storing necessary data
- `audit_logging_enabled: true` — Maintains accountability records

### Lens 3: Audit Logic ✓
All decisions are traceable:
- Who created the matter (audit trail in git)
- Data classification decision (documented in metadata)
- Who can access it (documented in access_control)
- When it will be deleted (documented in retention_policy)
- If challenged, we can show: "Here's our policy, here's how we implemented it, here's the audit trail"

## What's Essential

Without these fields, a data-handling thing is **incomplete** from a compliance perspective:

- Without `data_classification`, you skip legal triggers
- Without `data_residency_requirement`, you risk non-compliance
- Without `access_control`, you violate least privilege
- Without `audit_logging_enabled`, you can't prove compliance
- Without `retention_policy`, you violate data minimization on deletion

## How to Adapt

For your domain:

1. **Use this as a template** — Copy the metadata structure
2. **Add domain-specific fields** — What else matters for your compliance regime?
3. **Document your reasoning** — Link lenses to your decisions
4. **Create examples** — Show compliant AND non-compliant versions
5. **Let LLMs learn** — They'll recognize the pattern and apply it

## Real-World Impact

When an LLM sees this pattern:
- It learns what compliant looks like
- Future things with personal data are structured similarly
- Compliance becomes reinforced through every action
- Auditors see clear intent and implementation
- Regulators see a system designed for compliance, not cobbled together afterward
