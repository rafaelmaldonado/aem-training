# Session 33 · Diagnose the Dispatcher cache

Twelve English PNG slides; Spanish guide and local Dispatcher Tools exercise. No PPTX or speaker notes.

## Slide 01 · Diagnose the Dispatcher cache
- Class 33 · Week 7 · September 30, 2026
- Juan Maldonado
- Prove a miss, a hit and a fresh response after publication.

## Slide 02 · One URL, two versions
- Publish serves Version B while Dispatcher still serves Version A.
- Compare the same Host, path and method at both boundaries.
- A public response alone cannot identify the stale layer.

## Slide 03 · What can Dispatcher cache?
- `/cache/rules` selects document paths eligible for storage.
- Check method, extension, query parameters, authentication and response headers.
- A filter allowing a request does not make its response cacheable.

## Slide 04 · Prove a miss and a hit
- First request: inspect Dispatcher log and Publish request log.
- Repeat the identical URL: look for cache delivery and no new Publish request.
- Record Host, URL, status, version marker and timestamps.

## Slide 05 · Storage and invalidation rules
- `/cache/rules` controls which responses enter the cache.
- `/cache/invalidate` controls which stored files become stale after a content update.
- An invalidated file can remain on disk until the next request.

## Slide 06 · How `.stat` marks stale content
- An update touches `.stat` timestamps along the configured path.
- Dispatcher compares the cached file time with the relevant `.stat` time.
- `/statfileslevel` sets the invalidation scope.

## Slide 07 · Publish, flush, refresh
- Publish the changed page to the target.
- Confirm Publish serves Version B and a flush reaches Dispatcher.
- Request the original URL again; verify a fresh fetch and then a hit.

## Slide 08 · TTL is another freshness clock
- `/enableTTL "1"` uses response expiration headers.
- An expired object is fetched again from Publish.
- Standard invalidation may refresh it before TTL expires.

## Slide 09 · Query parameters change the test
- `/ignoreUrlParams` determines whether parameters are ignored for Dispatcher caching.
- An ignored parameter can reuse the same cached page.
- A parameter that changes content must not be ignored.

## Slide 10 · Local lab: A, A, B, B
- Request the same page twice through Dispatcher: miss, then hit.
- Publish a visible change from A to B; confirm B on Publish.
- Repeat the same Dispatcher URL: fresh B, then cached B.

## Slide 11 · Diagnose the stale response
- Publish still A: revisit publication and dependencies.
- Publish B, Dispatcher A: inspect cache eligibility, flush, `.stat` and TTL.
- Dispatcher B, public URL A: continue with browser and CDN in Class 34.

## Slide 12 · Questions
- Thank you.
