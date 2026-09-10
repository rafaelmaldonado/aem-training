# Class 23 · Runtime diagnostics and asynchronous processing

September 16, 2026 · 30 minutes · English slides, Spanish summary and simple examples.
Continuation of the approved course style and built-in image workflow; no intermediate confirmations, speech or PPTX.
Style-only reference: ../lesson-22/origin_image/slide_10.png. No required source figures.

## Slide 1 · Runtime diagnostics and asynchronous processing
- Class 23 · Week 5 · September 16, 2026 · Juan Maldonado
- Logs · OSGi runtime · Workflows and launchers · Sling Jobs
- Layout: Cover: large title and four topic labels, minimal diagnostic route motif. Only title, metadata and topic labels; no teaching panels.

## Slide 2 · Locate the symptom before changing the runtime
- Record the affected instance, time and content path.
- Separate missing output from failed processing.
- Trace the responsible layer: request, service, workflow or job.
- Use one observation to choose the next check.
- Layout: A four-stage diagnostic route with a small example: process label absent → inspect service registration. No invented code, commands or logs.

## Slide 3 · Read logs as an execution timeline
- Filter by time, logger and workflow or job identity.
- Read the exception chain and nearby context.
- An ERROR line is evidence, not a complete diagnosis.
- In Cloud, custom Java logs must reach error.log; use supported log access.
- Layout: Annotated conceptual log fields: timestamp, level, logger, message, correlation. No invented stack trace or arbitrary timestamps. Local SDK uses crx-quickstart/logs/error.log.

## Slide 4 · An active bundle does not prove an active service
- Bundle Installed: inspect unresolved package imports.
- Bundle Resolved: imports are resolved; the bundle is not active.
- DS Unsatisfied: inspect required references and configuration.
- A delayed DS component can be Satisfied until a consumer requests it.
- Layout: Two distinct columns: bundle states and Declarative Services states. A dashed link means bundle hosts components, not identical lifecycles. Add Active bundle ≠ every component Active.

## Slide 5 · Verify the effective configuration
- Find the exact PID or factory configuration instance.
- Confirm the applicable run modes and current property values.
- A source .cfg.json file does not prove the selected runtime values.
- Use local ConfigMgr for the SDK; Cloud changes follow supported configuration delivery.
- Layout: Source config → selection → effective values → service. Include small logger example category com.adobe.aem.guides.wknd.core.training.LogPayloadProcess, level INFO, file logs/error.log. No extra configuration keys.

## Slide 6 · A workflow has a model, a payload and an instance
- Model: the process definition. Payload: the object being processed.
- Instance: one execution with its own history and current step.
- Sync prepares the runtime model; start a new instance after model changes.
- Inspect Instances, Archive or Failures according to the observed state.
- Layout: Separate model definition and runtime execution diagram. Sync arrow between model editing and runtime model; instance launched from runtime model. No hard-coded model repository paths.

## Slide 7 · A process step runs code; a participant step waits
- Process Step: executes a registered WorkflowProcess service.
- Participant Step: assigns work to a user or group.
- Example: Start → Log payload → End, with Handler Advance enabled.
- A log entry proves the step executed; check history to prove completion.
- Layout: Short workflow diagram plus process-versus-participant comparison. Example process label exactly Training: log payload. No Java source or extra business actions. This example only logs; it does not write or publish content.

## Slide 8 · A launcher selects which event starts a workflow
- Match event type, node type, path, conditions and enabled state.
- A saved page can produce multiple repository events.
- Keep the path narrow and prevent self-triggering changes.
- A launcher starts a workflow; it is not the workflow or a timer.
- Layout: Repository event passes through matching-rule gates to workflow start. Clearly gates combine; not alternative OR routes. No concrete launcher rule with invented regex or API values.

## Slide 9 · Sling Jobs decouple submission from processing
- A producer submits a topic and serializable properties.
- A consumer handles that topic and returns a processing result.
- OK: success. FAILED: eligible for configured retry. CANCEL: permanent failure.
- The processing guarantee is at least once; repeated execution is possible.
- Layout: Producer → JobManager → queue → matching consumer, with result branches. FAILED retry arrow conditional on queue retry policy, not infinite. No Java APIs beyond shown names, no exactly-once claim.

## Slide 10 · Retry only after understanding the side effect
- Identify payload, current state, attempt and failure cause.
- Fix the cause before retrying a workflow step or job.
- Repeating the same operation must not duplicate its business effect.
- A timeout does not prove the remote operation never happened.
- Layout: Failure → inspect state → fix cause → safe retry, with simple payment-free content example: set status=processed again versus append a second item. Do not imply a property flag alone guarantees atomic idempotency.

## Slide 11 · Key takeaways
- Correlate the symptom with logs and runtime state.
- Separate bundle, DS component and effective configuration.
- Distinguish workflow definition, instance and launcher trigger.
- Inspect job results and duplicate risk before retrying.
- Layout: Four concise numbered checkpoint panels with different small diagrams. No exercise, assignment, acceptance rubric or extra framework.

## Slide 12 · Questions / Thank you
- Questions
- Thank you.
- Layout: Passive closing. ONLY Questions, Thank you. and small 12 eyebrow. No footer claim, bullets, recap or teaching.
