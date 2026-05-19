---
name: Compliance Patterns Workflow
type: workflow
description: How domain builders integrate compliance patterns into their domains
version: 1.0
applies_to: "compliance-patterns/**/*.md"
---

# Compliance Patterns Workflow

## Primary Process: Building a Regulated Domain

When you're building a domain that operates under regulatory constraints, the Compliance Patterns library helps you encode compliance as verifiable reasoning.

### Phase 1: Study Existing Patterns

Before building your domain:

1. **Identify your regulatory constraints** — What regulations apply? (GDPR, HIPAA, SOX, etc.)
2. **Load relevant patterns** — Study pattern things in this library
3. **Understand multi-lens reasoning** — See how domain specification, compliance, and audit logic interact
4. **Identify common patterns** — What decisions repeat in your domain?

### Phase 2: Design Your Domain With Compliance Built-In

When defining your domain in your own `domain.specification.skill.md`:

1. **Document regulatory constraints** — What rules apply?
2. **Define reasoning lenses** — How will you approach compliance?
3. **Create example patterns** — Add domain-specific examples to your domain
4. **Link to reference patterns** — Reference patterns from this library where applicable

### Phase 3: Create Domain-Specific Examples

In your domain's `things/`:

1. **Document patterns** — Create `type: pattern` things for compliant behaviors in your context
2. **Document anti-patterns** — Show violations and how to fix them
3. **Create decision trees** — Reusable frameworks for recurring compliance decisions
4. **Store in git** — Build your library and audit trail

### Phase 4: Use Patterns During Execution

When working within your domain:

1. **Reference patterns** — When making compliance decisions, load relevant examples
2. **Reason through multi-lens** — Apply domain, compliance, and audit logic
3. **Document precedent** — If you make a compliance decision, document it as a thing
4. **Grow your library** — Over time, your domain accumulates its own pattern library

### Phase 5: Audit and Review

Periodically:

1. **Review pattern usage** — Are patterns being applied consistently?
2. **Update patterns** — Did you discover edge cases? Update the pattern.
3. **Validate alignment** — Do all three lenses still align?
4. **Share patterns** — Contribute back to the reference library

## Sub-Processes

### Learning From a Pattern

**When:** You're studying an existing pattern to understand how compliance works

**Process:**
1. Load a `type: pattern` thing
2. Understand domain logic: "What does this accomplish?"
3. Understand compliance logic: "Why is this compliant?"
4. Understand audit logic: "How is this traceable?"
5. Ask: "How does this apply to my domain?"

### Creating a New Pattern

**When:** You've discovered a compliant behavior that should be documented

**Process:**
1. Describe the behavior clearly
2. Reason through: domain logic, compliance logic, audit logic
3. Create a `type: pattern` thing
4. Create related `type: anti-pattern` showing the violation
5. Link them together
6. Store in your domain's things/

### Resolving a Multi-Lens Conflict

**When:** Domain logic says yes, but compliance says no (or vice versa)

**Process:**
1. Document all three lenses clearly
2. Identify the exact conflict: "Where do they diverge?"
3. Create a `type: example` thing showing the conflict
4. Document the resolution: "How is this decided?"
5. Escalate to expert/human if needed
6. Store the precedent in your things/

### Building a Decision Tree

**When:** You have recurring compliance decisions that follow a pattern

**Process:**
1. Identify the decision: "What do we decide repeatedly?"
2. Map the decision points: "What questions do we ask?"
3. Create a `type: decision-tree` thing with clear branches
4. Document outcomes: "What happens at each decision point?"
5. Link to relevant patterns/examples
6. Store in your things/

## Integration With Your Domain

Your domain (life-manager, project-tracking, healthcare-system, etc.) will integrate compliance patterns like this:

1. **In your domain.instructions.skill.md** — Reference compliance patterns that apply to your context
2. **In your domain's read/write prompts** — Include guidance about when to reference compliance patterns
3. **In your domain's things/** — Create domain-specific examples and patterns
4. **In decision-making** — When faced with a compliance question, load relevant patterns and reason through multi-lens framework

## Key Workflows For Different Roles

### For Domain Architects
- Study reference patterns to understand compliance approaches
- Create domain-specific patterns
- Design multi-lens reasoning into your domain
- Document compliance assumptions in your domain's instructions

### For LLMs Operating In Regulated Domains
- Load patterns when making decisions
- Reason through all three lenses
- Reference patterns in your reasoning
- Mark things as compliant/non-compliant based on pattern matching

### For Auditors
- Review patterns documented in git
- Verify domain/compliance/audit alignment
- Check that multi-lens reasoning was applied
- Compare actual decisions against documented patterns

### For Domain Builders Adding New Constraints
- Load existing patterns for similar scenarios
- Adapt patterns for new constraint
- Create new examples showing both constraints
- Test reasoning across all three lenses

## Decision Framework: When To Create a New Pattern

**Create a pattern when:**
- You've identified a verifiable compliance behavior
- It's likely to repeat in your domain
- Both positive (compliant) and negative (violating) versions exist
- You can document it clearly with examples

**Don't create a pattern when:**
- It's a one-time decision
- It requires subjective judgment
- It's too domain-specific to be useful elsewhere
- You can reference an existing pattern instead

## Scaling From Example to Production

As your domain grows:

1. **Start with reference patterns** — Use patterns from this library
2. **Create domain-specific examples** — Document scenarios specific to your context
3. **Discover emergent patterns** — As you make decisions, patterns emerge
4. **Formalize patterns** — Document recurring patterns as reusable things
5. **Build your library** — Over time, your domain has a rich pattern library
6. **Audit naturally** — Your git history IS your compliance documentation
