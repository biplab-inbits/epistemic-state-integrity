# Epistemic State-Transition Integrity in Reasoning Agents

> An empirical investigation of whether reasoning agents correctly propagate evidence changes through downstream, action-relevant reasoning.

**Status:** Early-stage research. The central hypothesis remains unconfirmed.

---

## Overview

Reasoning systems increasingly operate over information that changes over time.

A system may first construct a multi-step justification for an action and later receive evidence that invalidates an upstream premise of that justification.

The central question of this project is:

> **When an upstream premise becomes invalid, does a reasoning agent reliably propagate that change through the downstream reasoning that supports its eventual action?**

A simple dependency chain can be represented as:

```text
evidence
   │
   ▼
intermediate conclusion 1
   │
   ▼
intermediate conclusion 2
   │
   ▼
action justification
   │
   ▼
   action
```

If the upstream evidence is later retracted, the formally justified downstream state should change as well.

The motivating failure hypothesis is that a model could instead retain an obsolete downstream dependency and consequently produce an action that is no longer justified by the current evidence.

This project is investigating whether such a phenomenon exists, under what conditions it occurs, and whether it can eventually be connected to an identifiable internal computational mechanism.

**The project does not currently claim that such a mechanism has been discovered.**

---

# Research Question

Let:

$$
E_{0:t}
\rightarrow
K_t^*
\rightarrow
h_t
\rightarrow
\pi_t
\rightarrow
A_t
$$

represent the transition from evidence to action, where:

- $E_{0:t}$ — available evidence history;
- $K_t^*$ — formally justified epistemic state;
- $h_t$ — model computational state;
- $\pi_t$ — decision process;
- $A_t$ — resulting action.

Suppose an upstream premise $e$ supports a dependency chain:

$$
e \rightarrow c_1 \rightarrow c_2 \rightarrow \cdots \rightarrow A
$$

If new evidence retracts $e$, then the normative state should invalidate its downstream descendants:

$$
\text{Retract}(e)
\Rightarrow
\text{Invalidate}(c_1,c_2,\ldots,A)
$$

The empirical question is whether the model's computation exhibits the corresponding transition.

A potential failure would therefore have the structure:

$$
\text{premise invalidation}
\rightarrow
\text{incomplete downstream updating}
\rightarrow
\text{stale action-relevant reasoning}
\rightarrow
\text{incorrect action}
$$

However, a behavioral failure alone would not establish this mechanism. The project therefore treats behavioral experiments as the first stage of a longer investigation.

---

# What This Project Is — and Is Not

This repository is **not** claiming to have demonstrated:

- epistemic hysteresis;
- stale hidden state;
- a new internal representation of knowledge;
- a mechanistic interpretability result;
- a causal neural mechanism;
- a reliable safety monitor.

Those are hypotheses and future research targets.

The immediate objective is much narrower:

> Determine whether controlled evidence-retraction experiments produce a robust behavioral phenomenon that survives alternative explanations.

Only if such a phenomenon is established does the project proceed to mechanistic investigation.

---

# Formal Experimental Framework

The repository contains a formal scaffold for defining the normative state against which model behavior is evaluated.

The framework includes:

- epistemic states;
- evidence events;
- evidence revision;
- equivalence relations;
- normative actions;
- dependency graphs;
- transitive retraction;
- controlled experimental scenarios.

The epistemic state space includes:

```text
ENTAILED
REFUTED
UNDETERMINED
CONTRADICTORY
```

The corresponding action policy is:

```text
ENTAILED        → PROCEED
REFUTED         → DO_NOT_PROCEED
UNDETERMINED   → VERIFY
CONTRADICTORY  → VERIFY
```

For example:

```text
credential_valid
       │
       ▼
user_authorized
       │
       ▼
operation_permitted
       │
       ▼
operation_cleared
       │
       ▼
PROCEED
```

If `credential_valid` is retracted, the formal system determines that the downstream justification is no longer supported.

The formal framework acts as an **external normative oracle** for the experiments.

It is not itself presented as the scientific contribution.

---

# Experimental Design

The project is being developed incrementally rather than jumping directly to mechanistic interpretability.

The current progression is:

```text
Formal specification
        │
        ▼
Behavioral smoke tests
        │
        ▼
Controlled behavioral characterization
        │
        ▼
Temporal commitment experiments
        │
        ▼
Alternative-explanation controls
        │
        ▼
Internal-state analysis
        │
        ▼
Causal intervention
        │
        ▼
Potential monitoring strategy
```

At every stage, a negative result is considered informative.

If the hypothesized phenomenon disappears under appropriate controls, the project will be revised or abandoned rather than interpreted as evidence for the original hypothesis.

---

# Stage 1 : Retraction Smoke Test

The first model-facing experiment used a simple evidence-retraction scenario.

The model initially received a valid authorization chain and was subsequently informed that the credential had been revoked.

It was asked to select:

```text
PROCEED
DO_NOT_PROCEED
VERIFY
```

The model selected:

```text
DO_NOT_PROCEED
```

This was **not evidence for stale reasoning**.

Instead, it established that the basic task was solvable and motivated a more controlled experimental design.

---

# Stage 2 : Controlled Behavioral Characterization

Stage 2 introduced systematic variation in dependency structure and presentation format.

The experiment contained:

```text
4 domains × 4 dependency depths × 2 presentation conditions = 32 trials
``` 

The domains covered different semantic settings while preserving the underlying logical structure.

The two presentation conditions were:

### Sequential

Information was presented through multiple temporal turns.

```text
initial evidence
      ↓
retraction
      ↓
final decision
```

### Flattened

The corresponding information was presented with the temporal structure collapsed into fewer turns.

The formal oracle specified:

```text
initial action  = PROCEED
revised action  = DO_NOT_PROCEED
```

The completed Stage-2 model runs did not reveal the hypothesized failure in this formulation.

This negative result was important.

The task was sufficiently explicit that the model could apparently recover the correct final action directly from the available information. Therefore, success on the task could not tell us whether the model maintained persistent downstream state and correctly invalidated it.

This motivated the Stage-3 redesign.

---

# Stage 3 : Temporal Commitment and Retraction

Stage 3 changes the experimental question.

Instead of immediately retracting the premise before the model has constructed downstream reasoning, the model is allowed to generate reasoning based on the original evidence first.

Three conditions were implemented.

## 1. Early Retraction

```text
initial evidence
      ↓
retraction
      ↓
final decision
```

This provides a temporal baseline.

## 2. Late Retraction

```text
initial evidence
      ↓
model constructs downstream reasoning
      ↓
retraction
      ↓
final decision
```

This tests whether prior model-generated reasoning changes the subsequent response to premise invalidation.

## 3. Late Retraction + Re-derivation

```text
initial evidence
      ↓
model constructs downstream reasoning
      ↓
retraction
      ↓
explicit reassessment
      ↓
final decision
```

This provides a stronger control for the possibility that explicit re-derivation can recover the correct state.

---

## Stage-3 Experimental Space


```markdown


The current Stage-3 generator produces:

```text
4 domains × 2 dependency depths × 3 conditions = 24 formally validated trials
```

Every generated scenario is checked against the formal oracle.

The required transition is:

```text

initial_status = entailed
revised_status = refuted

initial_action = proceed
revised_action = do_not_proceed
```


This validation occurs before a scenario is sent to the language model.

---

# Current Stage-3 Execution Status

A small three-trial pilot was successfully executed with Qwen3-4B.

The pilot demonstrated that the execution protocol works and that the model can correctly update its answer after credential revocation in the tested authorization scenarios.

The larger 24-trial Stage-3 execution was subsequently started.

The run reached trial 22 of 24 before the available GPU/compute quota was exhausted and the runtime was stopped.

Therefore:

> **No statistical or behavioral conclusion is drawn from the incomplete 24-trial Stage-3 run.**

The remaining two trials must be completed under controlled compute conditions before the Stage-3 dataset can be analyzed as a full experiment.

---

# Why the Stage-3 Question Is Harder

A model can answer the Stage-2 task correctly simply by reading the entire prompt again and recomputing the final answer.

That does not tell us whether it maintains a persistent representation of the dependency structure.

Stage 3 therefore introduces a different possibility:

$$
\text{initial evidence}
\rightarrow
\text{derived reasoning}
\rightarrow
\text{premise retraction}
$$

The model has already generated downstream reasoning before receiving the invalidating evidence.

If its final action changes correctly, that is evidence of behavioral updating.

If it fails, that would be evidence of a behavioral phenomenon worth investigating.

But even then, several alternative explanations must be ruled out before interpreting the failure as stale internal state.

---

# Alternative Explanations

A behavioral failure could arise from many mechanisms unrelated to the central hypothesis.

The project therefore intends to test explanations including:

- recency effects;
- lexical overlap;
- token-position effects;
- conversation-turn effects;
- context-length effects;
- comprehension difficulty;
- prompt-template artifacts;
- generic inconsistency;
- confidence effects;
- model-specific quirks;
- failures to understand the retraction itself.

A successful experiment must distinguish the proposed mechanism from these simpler explanations.

---

# Planned Mechanistic Investigation

Only after establishing a robust behavioral phenomenon would the project move to internal analysis.

The intended progression is:

### 1. Behavioral replication

Test the phenomenon across:

- multiple random seeds;
- dependency depths;
- semantic domains;
- prompt formulations;
- model families.

### 2. Controlled alternatives

Determine whether the effect survives controls for the simpler explanations above.

### 3. Internal-state analysis

Analyze model trajectories around the evidence transition:

$$
h_0 \rightarrow h_1 \rightarrow \cdots \rightarrow h_t
$$

The goal would be to identify candidate internal signals associated with outdated action-relevant dependencies.

### 4. Predictive testing

A candidate signal should predict the eventual behavioral failure beyond obvious lexical, positional, and prompt-level features.

A probe would be treated as a measurement instrument, not automatically as proof of a semantically meaningful representation.

### 5. Causal intervention

If a candidate mechanism is identified, interventions would test whether modifying that internal state changes the downstream behavior.

Correlation would not be considered sufficient.

### 6. Pre-action monitoring

A stronger result would be a signal that appears before the consequential action:

$$
t_{\text{signal}} < t_{\text{action}}
$$

and predicts the stale-action condition reliably.

### 7. Safety evaluation

Only after causal and predictive validation would the possibility of using such a signal as a monitoring mechanism be considered.

Any proposed monitor would also require adversarial evaluation.

---

# Falsifiability

The project is deliberately structured so that the original hypothesis can fail.

Possible outcomes include:

1. No robust behavioral phenomenon exists.
2. A behavioral effect exists but has a simpler explanation.
3. A behavioral effect survives controls but has no identifiable internal correlate.
4. An internal correlate exists but is not causally involved.
5. A causal mechanism is identified.
6. A causal mechanism supports a useful intervention or monitoring strategy.

The objective is not to force the experiment toward outcome 5 or 6.

The objective is to determine which of these possibilities is supported by evidence.

---

# Repository Structure

```text
epistemic-state-integrity/
│
├── src/
│   └── esi/
│       ├── formal_state.py
│       ├── evidence.py
│       ├── evidence_events.py
│       ├── equivalence.py
│       ├── revision.py
│       ├── action.py
│       ├── dependency.py
│       ├── retraction.py
│       ├── retraction_scenario.py
│       ├── scenario_family.py
│       ├── model_prompts.py
│       ├── stage2_behavioral.py
│       ├── stage3_commitment.py
│       └── stage3_execution.py
│
├── tests/
│   └── ...
│
├── experiments/
│   ├── generate_stage2_trials.py
│   ├── inspect_stage2_trials.py
│   ├── generate_stage3_trials.py
│   ├── inspect_stage3_trials.py
│   ├── stage2_trials.jsonl
│   └── stage3_trials.jsonl
│
├── .gitignore
└── README.md
```

---

# Reproducibility

The formal experimental infrastructure is tested locally.

Run:

```bash
python -m pytest -q
```

The current repository checkpoint passes the automated test suite.

The experiment-definition code and model-execution environment are deliberately separated:

```text
VS Code / repository
        │
        │ defines + validates
        ▼
controlled experimental trials
        │
        ▼
GPU execution environment
        │
        ▼
raw model outputs
        │
        ▼
analysis
```

This separation prevents the GPU notebook from becoming a second implementation of the formal experimental logic.

---

# Current Status

**Research hypothesis under investigation.**

Completed:

- formal epistemic-state framework;
- evidence revision machinery;
- dependency and retraction machinery;
- automated validation tests;
- Stage-2 trial generation and execution;
- Stage-3 protocol design;
- Stage-3 formal trial generation;
- Stage-3 pilot execution.

In progress:

- completing the Stage-3 behavioral dataset;
- analyzing whether temporal commitment changes retraction performance;
- designing controls for alternative explanations.

Not yet demonstrated:

- stale internal epistemic state;
- epistemic hysteresis;
- a causal mechanism;
- a pre-action neural signature;
- a safety monitor.

The next scientific decision should be determined by the Stage-3 behavioral evidence.

---

## Research Principle

> **Do not infer a mechanism from a behavioral error. First establish the phenomenon, rule out simpler explanations, identify a candidate mechanism, and then test it causally.**