# Instructions Guide

When you create a domain using this framework, you define it with an `[domain].instructions.md` file. This file is the philosophical and operational charter for your domain—where you explain *why* this system exists and *how* it should work within your specific context.

## What Is An Instructions File?

An instructions file is not a technical specification (that's what `thing.skill.md` provides). It's your domain's constitution: the beliefs, principles, and paradigm shifts that justify why you're using this framework for this particular problem.

## Structure

Your domain's `[domain].instructions.md` should include:

### Philosophy
**Why does this domain exist? What problem are you solving?**

Explain the paradigm shift. What traditional approaches fail? How does this framework invert or improve on them? This section should feel like the opening argument—why should someone care?

Examples:
- Life Manager: "Traditional productivity apps separate concerns (input/UI → processing/logic → output/notifications). This system inverts the model entirely."
- Project Management: "Typical project tools force rigid categorization. This system lets structure emerge alongside work."
- Creative Writing: "Writing tools are either too structured (outlining) or too free-form (blank page). This system structures the *metadata* while keeping the narrative free."

### Core Principles
**What beliefs drive this system?**

List 4-7 core principles that guide how things work in your domain. These should be:
- Specific enough to inform decisions
- Universal enough to apply across use cases in the domain
- Grounded in the philosophy above

Examples from life-manager:
- "Atomic Units: Everything is a thing. No special cases."
- "Minimal Core, Emergent Detail: Start simple; let the schema grow with your needs."

### How It Works
**What is the flow? How do users interact with this system?**

Describe the loop: how does a user interact with the LLM? What happens? How does data flow? Keep it concrete but concise.

The life-manager example:
> "1. Your life exists as a collection of things in git
> 2. Each thing is a markdown file with YAML metadata and narrative
> 3. When you need help, you talk to Claude
> 4. Claude reads relevant things, reasons about what you're asking
> 5. Claude updates your files or creates insights..."

### What This System Is / What It Is Not
**Set clear expectations.**

Clarify boundaries. What is this system NOT trying to do? What integration points does it have with other tools? This prevents feature creep and confused users.

Examples:
- "Not a calendar (but it drives calendar entries)"
- "Not a database (but it acts like one through git)"
- "Not replacing human intuition (but augmenting decision-making)"

## Before You Write

Ask yourself:

1. **Why am I using LLMs for this domain?** — What would be hard without LLM reasoning? What becomes possible with semantic understanding?

2. **What traditional approach am I replacing or inverting?** — What's broken about the status quo?

3. **What are my non-negotiables?** — What principles must hold true for this to work?

4. **Who is this for?** — If someone reads your instructions and disagrees with the philosophy, should they use this system? (If yes, your instructions aren't clear enough.)

## Examples

See `domains/life-manager/life-manager.instructions.md` for a complete, real-world example. Notice how it:
- Opens with the paradigm shift (why this matters)
- Explains the three decoupled layers
- Lists core principles with context
- Describes the interaction loop
- Sets boundaries on what the system is and isn't

## Length

Your instructions don't need to be long. Life-manager is ~800 words. That's enough to be complete without being overwhelming.

## Remember

Your instructions file is not enforcing rules; it's expressing *why* the rules exist. When someone (including a future version of you) reads your domain's instructions, they should understand not just what to do, but why it matters.

The best instructions files make you think: "Oh, I see. That's actually clever."
