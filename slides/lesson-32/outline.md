# Session 32 · Apache and Dispatcher request processing

Twelve English PNG slides; Spanish guide and local Dispatcher Tools exercise. No PPTX or speaker notes.

## Slide 01 · Apache and Dispatcher request processing
- Class 32 · Week 7 · September 29, 2026
- Juan Maldonado
- Follow a public URL to the response owner.

## Slide 02 · Trace one HTTP request
- Browser, CDN, Apache vhost, Dispatcher farm and filter, Publish.
- Track Host and URL as each layer processes the request.
- Compare status, Location and resolved path.

## Slide 03 · The Apache virtual host
- Host selects a vhost via ServerName or ServerAlias.
- Check the enabled vhost and included rewrite rules.

## Slide 04 · The Dispatcher farm
- Farm matching uses the request host and URI.
- The farm supplies virtualhosts, filter and renderer.

## Slide 05 · Rewrite or redirect
- An internal Apache rewrite keeps the browser URL.
- An external redirect returns 301 or 302 with Location.

## Slide 06 · Dispatcher request filters
- A filter can match method, URL, selectors or extension.
- Allowed requests continue to Publish; a denied filter request returns 404.
- Use logs to prove the matched rule.

## Slide 07 · Headers across the boundary
- Host affects vhost and farm selection.
- Check which request headers reach Publish through clientheaders.
- Record response status, Location and cache headers.

## Slide 08 · Who returned 403 or 404?
- Check Apache access logs, Dispatcher decisions and Publish request logs.
- HTTP status alone does not name the layer.

## Slide 09 · Run Dispatcher locally
- Browser at localhost:8080, Dispatcher Tools Docker and Publish at localhost:4503.
- Use the project host and path in curl.

## Slide 10 · Three responses, three checks
- 301/302 from Apache: inspect redirect rule.
- 404 at Dispatcher: inspect farm and filter logs.
- 404 at Publish: inspect resolved content path.

## Slide 11 · Find the first divergence
- Capture Host and URL; inspect status and Location.
- Read Apache and Dispatcher logs; compare the same path on Publish.

## Slide 12 · Questions
- Thank you.
