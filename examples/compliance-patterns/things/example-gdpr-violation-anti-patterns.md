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
**Multiple violations:**

- **No data classification** — System doesn't know this contains personal data
- **No residency constraint** — "External archive service" likely sends data outside UK
- **No access control** — "Everyone on the team has access" violates least privilege
- **No audit logging** — No record of who accessed what
- **No minimization** — Stores "all emails" (includes spam, personal messages, irrelevant data)
- **No retention policy** — "Delete when engagement ends" is vague and non-compliant with 7-year legal hold

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
| Residency | Process only in UK | Sent to external service | Likely GDPR violation |
| Access Control | Restrict to need-to-know | Everyone on team | Excess access, privacy breach |
| Audit Trail | Log all access | None | Cannot prove compliance |
| Data Minimization | Store only necessary data | Store all emails | Violation (including sensitive personal data) |
| Retention | Document and follow policy | Vague deletion | Cannot prove compliance or timely deletion |

## How to Fix It

Transform it into the compliant pattern:

```yaml
---
id: client-matter-acme
type: client-matter
data_classification: personal
data_residency_requirement: uk-only
access_control: [senior-attorney, paralegal-assigned]
data_minimization_check: true
audit_logging_enabled: true
retention_policy: legal-hold-7-years
created: 2026-05-18
---

# Acme Corp

## Client Matter Details
Regular correspondence with client and opposing counsel.

## Data Handling
- Only relevant correspondence stored (not all emails)
- Stored locally in UK infrastructure only
- Access restricted to attorney and assigned paralegal
- All access logged with timestamps
- Deleted after legal hold period (7 years)

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

When you build compliance into the thing structure itself (metadata, fields, reasoning), compliance becomes the default, not the exception.

## Related Patterns

- See `example-gdpr-compliant-data-handling.md` for the corrected approach
- See `pattern-gdpr-data-residency.md` for detailed residency requirements
- See `pattern-access-control-matrix.md` for least-privilege implementation
