# Evaluation Framework

Read this before evaluating any external source. It defines how a CTO actually decides whether something is worth adopting.

## How Great CTOs Actually Evaluate Things

They don't use scoring rubrics. They run the source through a series of filters. Most things get caught early. Each filter either lets something through to the next stage, redirects it to Learn (store the knowledge), or stops it at Skip (not relevant). The verdict emerges from where things land, not from adding up numbers.

## The Five Filters

### Filter 1: "Does this touch something I'm actually dealing with?"

Not theoretically relevant. Specifically: am I wrestling with this problem right now? Is this something I'm actively building, maintaining, or trying to improve? If the answer is "maybe someday," it's an automatic Learn at best. File the pattern, move on.

**Passes if:** You can name the specific thing in your repo or workflow that this relates to, and you've worked on it recently.

**Fails if:** You have to stretch to find the connection, or the connection is abstract ("this is about code quality and we write code").

### Filter 2: "Is this actually good?"

This is taste, not a checklist. After reading the source deeply (not just the README), does the approach feel right? Is there evidence it works in production, not just in demos? Has the author shipped real things?

Watch for:
- **Invented problems** - tools that exist because someone wanted to build something, not because there was genuine need
- **Demo-only quality** - looks great in a 5-minute video, falls apart at scale
- **Hype-to-substance ratio** - viral Twitter repos vs. steady organic growth
- **Better alternatives** - is this actually the best approach to this problem, or are there well-known better ways?

**Passes if:** The approach is sound, the implementation is solid, and you'd trust it in your system. A tiny repo with one brilliant technique passes. A 10k-star repo with a questionable approach fails.

**Fails if:** It's hype, it's solving an invented problem, or there are clearly better alternatives. Fast-track to Skip.

### Filter 3: "What specifically would I pinch?"

Great CTOs are cherry-pickers. They look at a repo with 20 features and say "that one technique is clever, the rest is noise." Be specific: name the exact thing you'd take. Not "their approach to X" but "their specific technique of doing Y in file Z."

**Passes if:** You can list specific, concrete things worth taking - techniques, patterns, configurations, approaches. Each one should be describable in a sentence.

**Fails if:** You can't name anything specific. "It's generally interesting" means Learn. "Nothing useful for us" means Skip.

### Filter 4: "Can I see the change?"

Can you literally picture the PR? What files get created or modified? What's the diff? How long does it take? This is the reality check that separates "interesting" from "actionable."

**Write down:**
- Files created and where they go
- Files modified and what changes
- Dependencies added (tools, packages, setup steps)
- Config changes needed
- Time estimate (30-minute PR or 3-day refactor?)
- What could break and how you'd roll back

**Passes if:** The PR is clear in your head. You could write the ticket right now.

**Fails if:** You can't describe the change concretely. This is a Learn - the knowledge is valuable but you're not ready to act on it.

### Filter 5: "Is the juice worth the squeeze?"

Given the specific change you'd make: is the improvement worth the disruption? Think about:
- **Maintenance burden** - who maintains this after it's in? Does it add ongoing complexity?
- **Cognitive load** - would a new team member look at this and be confused?
- **Opportunity cost** - is this the best use of time right now, vs. the other things on the list?
- **Reversibility** - can you try it and back out if it doesn't work?

**Passes if:** The improvement clearly outweighs the cost, and you'd still want this in 3 months.

**Fails if:** The improvement is marginal, the disruption is high, or there are more important things to do. This is a Learn - store the pattern for when the calculus changes.

## How Filters Map to Verdicts

| Where it lands | Verdict |
|---------------|---------|
| Passes all 5 filters with high confidence. The change is clear, the improvement is significant, and you'd do it this week. | **Adopt** |
| Passes filters 1-4, but needs tailoring. The technique is sound but your context requires modification. You can describe what to take and what to change. | **Adapt** |
| Caught at filter 1 (not dealing with this right now), filter 3 (interesting but nothing specific to pinch), or filter 4 (can't describe the PR). The source has genuine value worth remembering. | **Learn** |
| Caught at filter 2 (not actually good), or passes nothing. Not relevant, not useful, or we already do it better. | **Skip** |

**The default is Learn or Skip.** Adopt is rare - it requires passing every filter with confidence. Most things are interesting but not actionable right now, and that's fine. The learnings folder exists precisely for this.

## Warning Signs (Bias Towards Skip)

- No README or sparse documentation
- Last commit >6 months ago with no explanation
- "Kitchen sink" repos that try to do everything
- No license or restrictive license
- Depends on tools or services you don't use and won't adopt

## Good Signs (Bias Towards Deeper Look)

- Recommended by someone you trust
- Solves a specific problem well rather than being a framework for everything
- Uses tools you already have
- Author has shipped real production systems
- Clear, opinionated documentation that makes trade-offs explicit
