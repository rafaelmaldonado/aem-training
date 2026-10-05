# Session 37 · Read a pipeline failure

Nine English PNG slides. Cover follows Session 13: title, agenda, date, instructor, and small symbols. Subsequent slides use slide numbers 02–09. Spanish guide includes an optional local JaCoCo demonstration. No Cloud Manager access or participant exercises.

## Slide 01 · Read a pipeline failure

Title, agenda, date and Juan Maldonado.

## Slide 02 · Locate the first failed step

Read commit, step status, first explanatory log line and affected environment.

## Slide 03 · The first error explains the build

Dependency resolution fails before later summary messages.

## Slide 04 · Coverage is one signal, not the verdict

Cloud Manager code quality includes security findings and coverage; local JaCoCo shows missed code.

## Slide 05 · See which code your tests execute

Configure JaCoCo, run its agent with tests, and open the local HTML report.

## Slide 06 · A 404 in stage is not a build failure

Build and code quality pass, stage deploys, then a fictional test returns 404.

## Slide 07 · Old and new code can share content

Release A reads old and new fields; release B writes the new field while preserving old reads.

## Slide 08 · Recover from the boundary that failed

Respond according to the failed step and preserve compatibility with mutable content.

## Slide 09 · Questions

Thank you. Closing layout follows Session 13 slide 09.

## Teaching boundaries

- Security-related rules are evaluated within code quality; no separate security-testing stage in AEM as a Cloud Service.
- Local JaCoCo coverage is illustrative and does not reproduce the full Cloud Manager gate.
- A stage-test failure does not show production deployment.
- Rolling deployment can put old and new code against shared mutable content; code restore does not undo mutable content.
