# Evaluation Framework

Read this before scoring any external source. It defines the criteria and thresholds for the four verdicts.

## Verdict Definitions

### Adopt
**Threshold:** 95%+ confidence this is better than what we have AND can be integrated without breaking existing workflows.
- The source does something we need that we don't currently do, OR
- The source does something we already do but measurably better
- Integration effort is low relative to the improvement
- Well-maintained (recent commits, active issues, clear docs)
- **Bias:** This is the rarest verdict. Default away from it unless the case is overwhelming.

### Adapt
**Threshold:** 80%+ confidence some elements are valuable, but our context requires modification.
- Parts of the approach are genuinely better than ours
- Needs tailoring for our workflow patterns, repo structure, or team size
- The valuable parts can be extracted without importing the whole thing
- **Output:** Specific recommendations on what to take and how to modify it

### Learn
**Threshold:** The source teaches something useful even if we don't change anything right now.
- Interesting patterns or techniques to reference later
- Solves a problem we might have in the future
- Well-executed approach worth understanding even if not adopting
- **Output:** Knowledge stored in the learnings folder for future reference

### Skip
**Threshold:** Not relevant to our goals right now, or what we have is already better.
- Solves a problem we don't have
- Our existing approach is already superior for our context
- Too complex for our team size or stage
- Poorly maintained or outdated
- **Output:** Brief note explaining why, so we don't re-evaluate the same thing

## Scoring Criteria

Rate each source on these dimensions (1-5 scale):

| Criterion | 1 (Low) | 5 (High) |
|-----------|---------|----------|
| **Relevance** | Unrelated to what you're actively doing | Directly improves something you do frequently |
| **Quality** | Poorly documented, buggy, abandoned | Well-maintained, clear docs, active community |
| **Freshness** | >6 months old, uses outdated tools | <3 months old, uses latest versions |
| **Integration Effort** | Would require rewriting our workflows | Drop-in or minimal adaptation |
| **Signal Strength** | Unknown author, no stars | High-credibility source, many stars, recommended by trusted people |

**Composite score:** Average of all 5. But relevance and quality are weighted 2x.

**Composite = (Relevance*2 + Quality*2 + Freshness + Integration Effort + Signal Strength) / 9**

## Red Flags (auto-lower score)

- No README or sparse documentation
- Last commit >6 months ago with no explanation
- Depends on tools/services we don't use and won't adopt
- Adds complexity without clear benefit
- "Kitchen sink" repos that try to do everything
- No license or restrictive license

## Green Flags (auto-raise score)

- Recommended by someone trusted
- >500 GitHub stars with recent activity
- Clear, opinionated documentation
- Solves a specific problem well rather than being a framework for everything
- Uses tools we already have
- Author has credibility in the space
