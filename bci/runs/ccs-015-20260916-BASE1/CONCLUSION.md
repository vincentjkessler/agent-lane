# CCS-015 Comparative Baseline Result

Verdict: **CONVENTIONAL_AUTOMATION_SIMPLER_FOR_THIS_DETERMINISTIC_TASK**

- Exact semantic output match: `true`
- Compositional implementation: 4 files, 317 nonblank/noncomment LOC, 2 required workflow stages, 3 observed attempts.
- Conventional baseline: 2 files, 81 nonblank/noncomment LOC, 1 required workflow stage, 1 observed attempt.
- Both require one human policy decision conceptually.
- The compositional version uniquely provides an explicit durable human interrupt/resume point and an independent runtime verifier.
- For this deterministic transformation, those extra properties are not required to obtain the final release output and therefore are treated as added machinery, not automatic practical advantage.

## Interpretation

This experiment is a calibration result. If the conventional baseline is simpler while reproducing the same output, the lab should not use deterministic release transformation as evidence that composition is superior. Future comparative tests should target tasks where semantic adaptation, cold continuation, changing requirements, or recovery are actually needed.
