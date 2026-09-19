# Review workflow

1. Establish the requested behavior, diff boundary, repository instructions, and profile strictness.
2. Trace changed behavior through callers, boundaries, state transitions, effects, and error paths.
3. Evaluate every applicable Core Rule. Prioritize correctness, data loss, security, contract breaks, and missing risk-focused tests over style preferences.
4. Confirm findings with concrete code evidence and the conditions that trigger impact. Exclude speculative or purely subjective findings.
5. Run or inspect relevant configured checks when feasible; distinguish verified failures from unverified risk.
6. Report findings by severity with file and location, then note rule coverage and residual testing gaps. If no actionable findings exist, say so explicitly.
