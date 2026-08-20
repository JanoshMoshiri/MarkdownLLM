---
id: example-gdpr-violation-anti-patterns
type: example
status: stable
pattern_type: data-handling
demonstrates: anti-pattern
applies_to: [client-matter, document-storage]
created: 2026-05-18
linked_things:
  - id: example-gdpr-compliant-data-handling
    relation: remediated-by
---

# GDPR Violation: Anti-Patterns to Avoid

> **Synthetic, non-authoritative risk example.** These facts are warning signs,
> not a legal determination. Location, access, minimisation, and retention
> duties are context-specific; a qualified human decides whether a real design
> complies.

## The Problem

A thing that violates GDPR through poor practice:

```yaml
---
id: client-matter-acme
type: client-matter
notes: "Store all emails here for reference"
---

# Acme Corp

All emails from this client, including personal details, 
sent to external archive service. Everyone on the team has access.
Delete when engagement ends.
```

## Why This Fails

### Lens 1: Domain Logic ✓
Goal is clear: keep client emails for reference. But...

### Lens 2: Compliance Logic ✗
**Multiple unaddressed risks:**

- **No data classification** — System doesn't know this contains personal data
- **No approved processing-location policy** — the external archive has not
  been assessed or contractually bounded
- **No access control evidence** — "Everyone on the team" is unlikely to
  demonstrate a purpose-specific need-to-know decision
- **No audit logging** — No record of who accessed what
- **No minimization** — Stores "all emails" (includes spam, personal messages, irrelevant data)
- **No retention policy** — "Delete when engagement ends" is too vague to test
  against the applicable matter-specific schedule or legal holds

### Lens 3: Audit Logic ✗
**Cannot be defended:**
- No documentation of decision-making
- No audit trail of access
- No proof of compliance
- Regulator asks: "Why did you send personal data outside UK? Who accessed it? When was it deleted?"
- You have no answers.

## The Specific Violations

| Requirement | What Should Happen | What Actually Happened | Impact |
|-------------|-------------------|----------------------|--------|
| Data Classification | Declare: personal data | No declaration | System treats it as non-sensitive |
| Processing location | Use approved processors/locations for this matter | Sent to an unassessed external service | Transfer and processor risk cannot be evaluated |
| Access Control | Restrict to need-to-know | Everyone on team | Excess access, privacy breach |
| Audit Trail | Log all access | None | Cannot prove compliance |
| Data Minimization | Store only necessary data | Store all emails | Violation (including sensitive personal data) |
| Retention | Document the applicable schedule and holds | Vague deletion | Timely deletion/retention cannot be tested |

## How to Fix It

Transform it into the compliant pattern:

```yaml
---
id: client-matter-acme
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

# Acme Corp

## Client Matter Details
Regular correspondence with client and opposing counsel.

## Data Handling
- Only relevant correspondence stored (not all emails)
- Stored only through the approved mechanism for this matter
- Access enforced by the assigned identity group and reviewed
- Logging operation sampled into a linked evidence record
- Deleted or held according to the matter-specific schedule

## Rationale
This approach balances client service (we have what we need) 
with compliance (we minimize data, control access, maintain audit trail).
```

## The Lesson

Violations often come from convenience, not malice:

- It's easier to store everything than decide what matters
- It's simpler to give everyone access than maintain an access matrix
- It's faster to use any cloud service than keep data local
- It's less work to delete on "task completion" than follow a retention policy

**But compliance isn't about effort. It's about protecting data subjects and respecting their rights.**

When you build policy, mechanism, evidence, and human judgement into the thing
structure, missing links become visible. Structure supports compliance work; it
does not make compliance automatic.

## Related Patterns

- See `example-gdpr-compliant-data-handling.md` for the corrected approach
  (linked as `remediated-by` in the frontmatter — the library's convention for
  pairing every violation with its fix)
