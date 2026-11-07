## Operator escalation and immediate blocker reporting — 2026-11-07

### Finding
The operator requires immediate escalation whenever an execution blocker exists or an available tool cannot run a required workflow. Do not wait for the operator to prompt again.

### Evidence
Nolan's explicit instruction in the Project Oracle conversation on 2026-11-07: "if there is a blocker or you cant run a workflow - tell me immedately so we dont wasit time, dont wait for me to promtp you."

### Root cause
Prior interaction patterns allowed status limitations or workflow-dispatch limitations to be reported only after the operator prompted again. This creates avoidable idle time and delays the dependency owner.

### Impact
A workflow requiring operator action, missing permission, unavailable dispatch capability, failed credential, unavailable artifact, or blocked dependency must be surfaced as soon as it is established, with the exact action required. Never imply a workflow is running unless its live status confirms that.

### Fix
All Project Oracle continuation lanes must:
1. Explicitly distinguish actions completed by the assistant from actions requiring operator execution.
2. Immediately report blockers and tool limitations, including the exact GitHub URL, workflow name, branch, missing permission/secret, or manual operation required.
3. When a workflow is running, inspect its run status, jobs, logs and artifacts before asking the operator for another action.
4. Never wait for another "Continue" prompt to disclose a known blocker.
5. If a tool is unavailable, say so immediately and switch to the closest supported read-only diagnostic or manual instruction.

### Validation
Applied in this continuation: run 42361333640 was inspected live and confirmed in_progress, with checkout, Python setup and dependency installation complete; the 50-league source validation step was in_progress; reconciliation and persistence were pending. No workflow-dispatch limitation blocked this run because Nolan had already started it. Production Oracle V1.6 remains untouched.
