# Epistemic State-Transition Integrity in Reasoning Agents

An ongoing investigation into whether reasoning agents correctly propagate evidence changes through downstream, action-relevant reasoning.

> **Status: Research hypothesis under investigation. No mechanistic finding or safety benefit is claimed yet.**

---

## Research Question

When new evidence invalidates a premise supporting a multi-step action, does a reasoning agent correctly propagate that invalidation through the downstream reasoning that supports the action?

The central object of study is the transition:

\[
E_{0:t} \rightarrow K_t^* \rightarrow h_t \rightarrow \pi_t \rightarrow A_t
\]

where:

- \(E_{0:t}\) is the available evidence history;
- \(K_t^*\) is the formally justified epistemic state;
- \(h_t\) is the model's computational state;
- \(\pi_t\) is the decision process;
- \(A_t\) is the resulting action.

The motivating failure hypothesis is that an upstream premise may become invalid while some downstream, action-relevant reasoning remains stale.

In schematic form:

\[
K_t^* \text{ changes}
\quad\text{but}\quad
h_t^{\text{action}}
\text{ retains an obsolete dependency}
\]

potentially producing an action that is no longer justified by the current evidence.

This is a hypothesis, not an established phenomenon.

---

## Central Hypothesis

Suppose a reasoning process contains a dependency chain

\[
e \rightarrow c_1 \rightarrow c_2 \rightarrow \cdots \rightarrow A
\]

where \(e\) is an evidence-supported premise and \(A\) is an action.

If new evidence retracts \(e\), the formally justified state should invalidate its downstream descendants:

\[
\operatorname{retract}(e)
\Rightarrow
\operatorname{invalidate}(c_1,c_2,\ldots,A)
\]

The research question is whether capable reasoning models always perform the analogous transition in their computation.

A possible failure would therefore be:

\[
\text{premise invalidation}
\rightarrow
\text{failure to propagate invalidation}
\rightarrow
\text{stale action-relevant reasoning}
\rightarrow
\text{incorrect action}
\]

The project specifically seeks to distinguish this possibility from simpler explanations such as:

- recency effects;
- lexical artifacts;
- position effects;
- prompt/template effects;
- comprehension failures;
- generic inconsistency;
- context-length effects;
- confidence effects;
- model-specific quirks.

---

## Formal Experimental Scaffold

The repository contains a machine-checkable formal scaffold used to define the normative ground truth of the experiments.

The scaffold includes:

- epistemic states;
- evidence events;
- evidence revision;
- logical equivalence;
- normative actions;
- dependency graphs;
- transitive retraction;
- controlled experimental scenarios.

The epistemic status space includes:

```text
ENTAILED
REFUTED
UNDETERMINED
CONTRADICTORY