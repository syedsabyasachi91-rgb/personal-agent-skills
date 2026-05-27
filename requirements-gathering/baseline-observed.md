# Baseline Observations (Without Skill)

## Scenario 1: Notification System

**Observed behavior:** Without the skill, the AI tends to:
- Ask 2-3 questions bundled together ("What kind of notifications? Who receives them? What channels?")
- Jump to suggesting architecture before gathering all requirements
- Miss some categories entirely (dependencies, priorities, success criteria)
- Not systematically synthesize back to the user
- Make implicit assumptions without checking

**Excerpt of typical response:**
> "Great question! Let me start by asking a few things:
> 1. What kinds of notifications? (invoice due, payment, etc.)
> 2. Who receives them? (customers, staff, both?)
> 3. What channels? (email, SMS, in-app?)
> 
> Once I know that, I can suggest an architecture..."

**Problems:**
- Multiple questions at once (overwhelming)
- Already hinting at architecture before all requirements known
- Missing: scope boundaries, success criteria, constraints, dependencies, priorities
- No synthesis step

## Scenario 2: Data Export

**Observed behavior:** Without the skill, the AI tends to:
- Focus on technical details (format, library choice) too early
- Miss stakeholder and priority questions
- Jump to implementation suggestions

## Scenario 3: Auth System

**Observed behavior:** Without the skill, the AI tends to:
- Ask about auth methods, then immediately suggest a library/framework
- Miss: deployment constraints, integration points, success criteria, trade-offs
