---
id: example-gdpr-compliant-data-handling
type: example
status: stable
pattern_type: data-handling
demonstrates: compliance
applies_to: [client-matter, document-storage, communication, personal-data]
created: 2026-05-18
linked_things:
  - id: example-gdpr-violation-anti-patterns
    relation: contrasts-with
---

# GDPR Compliant: Data Handling Pattern

> **Synthetic, non-authoritative teaching example.** GDPR duties depend on
> purpose, lawful basis, data subjects, jurisdictions, contracts, risk, and
> applicable retention law. The fields below declare a proposed control; they
> do not implement authorisation, residency, logging, deletion, or legal
> compliance. A qualified human must select the real policy and verify its
> operation.

## The Pattern

A thing that handles personal data correctly within GDPR constraints:

```yaml
---
id: client-matter-smith-ltd
type: client-matter
data_classification: personal
declared_policy:
  residency: approved-processing-locations-for-this-matter
  access: assigned-team-need-to-know
  minimization: collect-only-documented-purpose-fields
  retention: matter-specific-schedule-id
enforcement_mechanism:
  residency: infrastructure-policy-id
  access: identity-group-id
  minimization: intake-schema-id
  retention: records-system-rule-id
evidence_of_operation:
  access_review: evidence-record-id
  audit_log_sample: evidence-record-id
  deletion_test: evidence-record-id
created: 2026-05-18
---

# Smith Ltd Matter

## Sensitive Data Involved
This thing involves personal data of clients and third parties.

## Data Handling Approach
- Processing locations follow the matter's approved, evidenced policy
- Access is enforced by the named identity group and reviewed periodically
- Audit evidence is sampled from the actual logging system
- Retention follows the matter-specific schedule and applicable legal holds
- Deletion operation is tested and linked as evidence
```

## Why This Matters

### Lens 1: Domain Logic ✓
Creates a client matter with all necessary information to support legal work.

### Lens 2: Compliance Logic ✓
- `data_classification: personal` — declares that the workflow must evaluate
  applicable data-protection duties
- `declared_policy` — records the human-approved intent for this matter
- `enforcement_mechanism` — names the system expected to make each control real
- `evidence_of_operation` — points at observations that can test whether the
  mechanism actually operated

The metadata makes omissions visible; it does not itself ensure or enforce a
control.

### Lens 3: Audit Logic ✓
The record is inspectable:
- Git shows who committed the declaration and how it changed
- metadata records the classification and intended policy
- mechanism identifiers point to the systems that should enforce it
- evidence identifiers point to samples/reviews from those systems

Git does **not** show who accessed the underlying data unless an access system
exports that evidence into a reviewed record.

## What's Essential

Without these fields, a data-handling thing is **incomplete** from a compliance perspective:

- Without `data_classification`, you skip legal triggers
- Without a purpose-specific declared policy, the control intent is ambiguous
- Without an enforcement mechanism, policy is only prose
- Without evidence of operation, implementation is an untested claim
- Without human legal judgement, a reusable example cannot select the correct
  location or retention period

## How to Adapt

For your domain:

1. **Use this as a reasoning pattern** — Do not copy its policy values
2. **Add domain-specific fields** — What else matters for your compliance regime?
3. **Document your reasoning** — Link lenses to your decisions
4. **Create examples** — Show compliant AND non-compliant versions
5. **Let LLMs learn** — They'll recognize the pattern and apply it

## Real-World Impact

When an LLM sees this pattern:
- It learns what compliant looks like
- Future things with personal data are structured similarly
- Policy, mechanism, and evidence are less likely to be conflated
- Auditors can follow a declared chain and test its missing or stale links
- Humans still decide whether the chain satisfies the law and the real context
