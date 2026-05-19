# Scalability Guide

When you start with this framework, everything is simple: you have a few things, Claude reads them all, reasons holistically, and responds. But as your system grows—from dozens to hundreds to thousands of things—you need a strategy for keeping that reasoning efficient.

This guide explores the philosophy and practice of scaling this framework to handle complex systems without losing the elegance that makes it powerful.

## The Problem: What Breaks at Scale

### Scenario: You Have 50 Things

Claude loads all 50 thing files. Reads metadata and narratives. Responds to "What should I focus on?" in a couple seconds. All good.

### Scenario: You Have 200 Things

Claude loads all 200 files. Takes longer. Starts using more tokens. For "What should I focus on?" it takes 10-20 seconds. Productivity tools are getting expensive.

### Scenario: You Have 500 Things

Loading everything feels slow. Each query costs real money. You're asking Claude broad questions like "prioritize my work" and it's loading the full narrative of all 500 things. You feel the friction.

### Scenario: You Have 1000+ Things

This breaks. It's expensive, slow, and inefficient. Claude needs to search or index rather than load everything holistically.

**The root problem:** Treating all information as equally important, all the time.

## The Philosophy: How Neural Networks Handle Complexity

Your instinct was right to look at how neural networks work. A neural network doesn't load all its weights equally. It doesn't activate every neuron for every input. Instead:

1. **Edges matter, not nodes** — Neural networks process through connections and attention patterns, not by loading every piece of data
2. **Multiple levels of abstraction** — Different layers process information at different scales simultaneously
3. **Attention is dynamic** — Relevant patterns light up based on the input; irrelevant patterns stay quiet
4. **Efficiency through abstraction** — High-level patterns are captured at lower resolution before deeper processing

Translated to your system:

- **Don't load all things equally** — Load at the level of detail you need for the task
- **Use abstraction levels** — Metadata for broad questions, relationships for connections, full narrative for depth
- **Let Claude's attention work** — Don't pre-index or search; let Claude reason about relevance given what's loaded
- **Scale through layers** — As systems grow, add summarization layers without changing the core structure

## Three Approaches to Scaling

### Approach 1: Contextual Loading (Practical Now)

**The idea:** Don't load everything. Load contextually by domain, time period, or theme.

**Example:**

Instead of: "Show me everything across all my projects"

Do this: "What's due this month?" → Load things with `due_date` in current month

Or: "Show me my health goals" → Load things tagged `health`

Or: "What's my situation with project X?" → Load project X and its linked things

**Implementation:**
- Prompts guide Claude to ask: "What domain/time/theme should I focus on?"
- User specifies context
- Claude loads only the relevant subset at the appropriate level
- Claude processes that subset holistically

**Pros:**
- Works immediately with no new tooling
- Natural and intuitive
- Teaches the system to think contextually

**Cons:**
- User has to manually specify context
- For complex queries ("Show me everything blocking my critical path"), context is ambiguous

**When to use:** Starting point. Works up to 200-300 things in a single domain.

### Approach 2: Incremental Summarization (Medium Scale)

**The idea:** Things that have been "settled" or "completed" get pre-summarized. Claude uses summaries for overview, then drills into detail.

**Example:**

```yaml
---
id: q1-retrospective
type: summary
summarizes: [completed-project-a, completed-project-b, completed-project-c]
created: 2026-05-17
---

# Q1 2026 Retrospective

## Projects Completed (3)
- Project A: shipped on time, 5 people, $200k budget
- Project B: shipped late due to feedback iterations, 3 people, $80k
- Project C: cancelled mid-project due to strategic shift, 2 people, sunk cost $30k

## Key Learnings
- Feedback loops need defined windows
- Strategic alignment should happen earlier
- Resource allocation worked well for A, needs rework for B

## What It Unblocked
- Q2 product roadmap
- 2 people now available for Q2 initiatives
```

**How Claude uses it:**
- Load "What happened in Q1?" → Load 1 summary file instead of 3 detailed project files
- Load "Tell me about completed projects" → Load summary, then drill into full project files if needed
- Load "What resources are available?" → Summaries answer the question; no need to read full things

**Implementation:**
- Create summary things manually or ask Claude to generate them
- Summaries live in the same repo alongside regular things
- Prompts recognize `type: summary` and treat it specially

**Pros:**
- Explicit, human-readable summaries
- Natural stopping points (end of quarter, project completion)
- Lets you curate what matters
- Still uses the same data structure (just thing files)

**Cons:**
- Summaries go stale; require maintenance
- Need to decide when to summarize
- Adds another layer of files to manage

**When to use:** When you have 200-500 things and notice patterns of "completed" or "archived" things that clutter current queries.

### Approach 3: Full Tiered System (Long Term)

**The idea:** Formalize three abstraction levels—metadata, relationships, full context—as first-class parts of the system. Different prompts or query types load different levels.

**How it works:**

**Level 1: Metadata Map**
- All things, metadata only (YAML frontmatter stripped of body)
- Fast scan of the entire landscape
- "Broad question" queries use this

**Level 2: Relationship Graph**
- All things with metadata + linked_things + dependencies + blocks
- No narrative body, but full connection information
- "Connection" and "path" queries use this

**Level 3: Deep Dive**
- Full thing files for specific things
- Narrative body + all metadata
- "Detail" queries use this

**Example workflow:**

```
User: "I'm feeling overwhelmed. What should I focus on?"

Claude:
1. Load Level 1 (all things, metadata only)
2. Analyze: "You have 23 in-progress, 8 blocked, 15 urgent"
3. Return: "Your system is overloaded. Let's focus on unblocking the 8 blockers first."

User: "Which blockers are easiest to solve?"

Claude:
1. Load Level 2 for the 8 blocked things and their dependencies
2. Trace back: "5 are blocked on decisions, 2 on external approval, 1 on technical blocker"
3. Return: "The decision blockers are quickest if you can decide. Want me to show you those decisions?"

User: "Yes, show me the decisions"

Claude:
1. Load Level 3 for those 5 specific things
2. Read full narrative to understand the decision context
3. Present the decisions with full context
```

**Implementation:**
- Structured in thing.md (already done)
- Prompts are aware of levels and choose them strategically
- As you use the system at scale, this becomes natural

**Pros:**
- Maximally scalable (works at 10,000+ things)
- Mirrors how neural networks actually work
- Elegant: same files, different loading patterns
- Evolves naturally from Approach 1

**Cons:**
- Requires more sophisticated prompting initially
- Needs data discipline (your metadata has to be consistent)
- Overkill for small systems

**When to use:** When you have 500+ things across multiple domains or complex dependencies; or when you're building this as a long-term personal infrastructure.

## When You Hit the Limits

You'll know it's time to scale when:

1. **Slowness** — Queries that used to be instant take 15-30 seconds
2. **Cost** — Each broad query is noticeably expensive
3. **Frustration** — You're asking Claude to load things you don't actually need
4. **Patterns** — You start wanting summaries or snapshots for historical reference
5. **Complexity** — You have multiple domains and queries often ask across them

These aren't hard thresholds—they're signals that your system has grown and optimization is worth it.

## Recommendation: Start Simple, Evolve Naturally

**Today:** Use Approach 1 (contextual loading). Your prompts already support this. As you use the system:
- Notice what context you ask for repeatedly ("Show me work things," "What's due this week")
- That's information about your mental model
- You'll feel it when Approach 1 isn't enough

**Tomorrow:** When you feel friction, start creating summary things (Approach 2). They're just thing files; no new infrastructure required.

**Months later:** If you're using this heavily, you naturally move toward Approach 3—loading metadata only for "What's my situation?" queries, loading relationships for "What blocks what?" queries, loading full context only for deep work.

The system doesn't force you to scale. You scale when the benefit is obvious and the friction matters.

## Key Principle

**Scale through abstraction, not through search or indexing.**

Don't build database functionality. Don't add query languages. Load at the right level of abstraction, let Claude's natural reasoning do the work, and let summaries emerge as your system grows.

This keeps the framework simple while still enabling complex systems.

---

**Questions?**

- How do I know which level to load for my query? See `read.thing.md` and `write.thing.md` for guidance.
- Can I use summaries with my existing domain? Yes. Create a thing with `type: summary` and it works.
- Should I architect for Approach 3 from day one? No. Start with Approach 1, migrate as needed.
- What if I want to stay small forever? Great. Approach 1 works indefinitely for systems under 100-200 things.
