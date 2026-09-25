# Session 31 · Trace a publication

Technical continuation of the approved course style. Twelve English image slides; Spanish guide contains a local Author/Publish demo and a supplied Cloud queue incident. No PPTX or speaker notes requested.

## Slide 01 · Check publication
- Class 31 · Week 7 · September 28, 2026
- Juan Maldonado
- Follow content from Author to Publish.
- Visual: one content path with marked checkpoints. Cover.

## Slide 02 · Four checkpoints for one path
- 1. Author submits an action for a path.
- 2. Distribution accepts and queues it.
- 3. Publish imports the change.
- 4. The target serves the expected version.
- Visual: one horizontal path with four distinct checkpoints. Process.

## Slide 03 · Inside Cloud distribution
- Sling Content Distribution moves content outside the AEM runtime.
- The publish agent is enabled by default.
- The preview agent targets Preview when configured.
- A submitted action is not proof of a completed import.
- Visual: Author, external distribution service, Publish and Preview with agent labels. Architecture.

## Slide 04 · Two queues, two meanings
- persisted: the change is durably stored on Publish.
- fully published: all Publish pods serve it.
- Pending items and Last Item Processed show progress.
- Inspect the affected path before changing anything.
- Visual: two sequential queue checkpoints with exact names. State model.

## Slide 05 · Scope is a dependency graph
- A selected page does not automatically include child pages.
- Review referenced assets and other dependencies.
- A shared reference may support another page.
- Record the exact paths included in the action.
- Visual: selected page, child and shared asset as distinct branches. Graph.

## Slide 06 · Prepare one traceable change
- Record the exact test page and asset paths.
- Change a visible marker from Version A to Version B.
- Publish with Manage Publication after reviewing scope.
- Capture time, destination and included paths.
- Visual: a small lab evidence sheet beside the selected page and asset. Procedure.

## Slide 07 · Read ReplicationStatus carefully
- isActivated(): last action was Activate.
- isPending(): last action remains queued.
- isDelivered(): derived from replication logs.
- None proves the resource is physically on Publish.
- Visual: three API signals plus a separate target verification checkpoint. API evidence.

## Slide 08 · Preview has its own status
- A preview-only action does not update the default publish status.
- Read getStatusForAgent("preview") for Preview.
- Read getStatusForAgent("publish") for Publish.
- Verify the chosen destination separately.
- Visual: one resource with two agent-specific status branches. Comparison.

## Slide 09 · Investigate a pending path
- Tools → Deployment → Distribution → publish.
- Check persisted and fully published queues.
- Inspect Items Pending, Last Item Processed and Logs.
- Record the blocking path; do not clear the queue in class.
- Visual: ordered Cloud investigation route with two queue indicators. Diagnosis.

## Slide 10 · Local proof is not Cloud proof
- Local SDK: Author :4502 → replication agent → Publish :4503.
- Cloud: Author → Sling Content Distribution → Publish.
- Use local Publish to verify content and references.
- Use supplied Cloud queue evidence to reason about SCD.
- Visual: parallel local and Cloud transport lanes ending at Publish. Comparison.

## Slide 11 · Stop at the Publish boundary
- No action: revisit destination and scope.
- Pending path: inspect queue and logs.
- Cleared queues, wrong Publish content: verify path and references.
- Correct Publish content: hand off the request path to Class 32.
- Visual: evidence-based decision tree ending at Publish. Boundary.

## Slide 12 · Questions
- Thank you.
- Visual: quiet closing slide with generous whitespace. Q&A.
