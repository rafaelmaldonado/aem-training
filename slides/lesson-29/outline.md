# Session 29 · Repository access with the right identity

Continuation of lesson28: same approved visual reference and built-in image backend; PNG + HTML/Markdown, no PPTX or speech.

## Slide 01 · Repository access with the right identity
- Class 29 · Week 6 · September 24, 2026
- Juan Maldonado
- Request resolvers, service mappings and ownership
- Visual: Large title left, two distinct identity routes to a repository on right.

## Slide 02 · Choose whose permissions apply
- User action: preserve the caller’s access.
- Background task: use a dedicated service identity.
- A service resolver does not authorize the HTTP caller.
- Visual: Two branching routes: user request to request resolver; background task to service resolver. Keep identities distinct.

## Slide 03 · Borrow the request resolver
- request.getResourceResolver()
- Sling owns this resolver. Do not close it.
- Use it only during the request.
- Do not replace a denied read with elevated access.
- Visual: Request start, borrowed resolver, repository read, request end as horizontal lifecycle. Highlight Sling ownership.

## Slide 04 · A mapping connects three names
- Bundle symbolic name: wknd.core
- Subservice: training-guide-read
- Principal: training-guide-reader
- wknd.core:training-guide-read=[training-guide-reader]
- Visual: Three labeled pieces connect to exact mapping line. The line must be readable, intact and accurately spelled.

## Slide 05 · Mapping and permissions are separate
- Repo Init creates the service user and read ACL.
- OSGi configuration maps bundle and subservice.
- Principal-based login does not expand groups.
- A valid mapping does not grant content access.
- Visual: Two columns Identity selection and Repository permission; visually show both required. No implication that principal login requires principal ACL.

## Slide 06 · Close the resolver you create
- getServiceResourceResolver(authInfo)
- Use try-with-resources for an owned resolver.
- Read and copy values before the block ends.
- Never keep a resolver in a singleton field.
- Visual: Open, read, copy String, close timeline with try-with-resources bracket. Detached String leaves scope; Resource and resolver stay inside.

## Slide 07 · One small local example
- Read /content/training-permissions/guides
- Use subservice training-guide-read
- Return a String, not a live Resource.
- No servlet, arbitrary path or write operation.
- Visual: OSGi service to factory to fixed folder to detached String. Show subservice label near factory, closure at boundary.

## Slide 08 · Inspect the deployed configuration
- Confirm the calling bundle’s symbolic name.
- Check the amended user.mapping entry.
- Inspect the service user and direct read grant.
- Use the local OSGi component and error log views.
- Visual: Numbered inspection route with bundle, mapping, principal, folder and log icons. No fabricated console screenshot.

## Slide 09 · Diagnose the failing layer
- LoginException: inspect mapping and identity.
- Null resource: check existence and read access.
- Write failure: inspect operation and privileges.
- HTTP 403: identify the rejecting filter or handler.
- Visual: Four symptom-to-check horizontal rows. Label expectations, do not claim actual results.

## Slide 10 · CSRF is an HTTP check
- Protected writes need a valid CSRF token.
- Fetch /libs/granite/csrf/token.json in the same session.
- Send it in the CSRF-Token header.
- A valid token does not grant repository permissions.
- Visual: Browser request through CSRF check then application then ACL check. Both checks must pass. Do not draw a bypass.

## Slide 11 · Key takeaways
- Choose identity from the operation’s purpose.
- Match bundle, subservice and principal exactly.
- Mapping and ACL solve different problems.
- Close owned resolvers; keep borrowed ones open.
- Diagnose the layer before changing permissions.
- Visual: Five compact takeaways with identity, mapping, permission, lifecycle and diagnosis icons.

## Slide 12 · Questions
- Thank you.
- Visual: Only Questions, Thank you. and number 12. Quiet generous whitespace.
