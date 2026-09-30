# Session 34 · Separate browser, CDN and Dispatcher caches

Twelve English PNG slides; Spanish guide with local browser/Dispatcher checks and supplied simulated CDN evidence. No CDN or Cloud access required.

## Slide 01 · Browser, CDN and Dispatcher caches
- Class 34 · Week 7 · October 1, 2026 · Juan Maldonado.
- Identify the first layer that still serves Version A after Publish and Dispatcher serve B.

## Slide 02 · One page, three cache decisions
- Browser → CDN → Apache/Dispatcher → Publish.
- A hit at one layer prevents the request from reaching later layers.
- Compare the same Host, path, query and response marker.

## Slide 03 · Headers set different clocks
- `Cache-Control: max-age` controls browser freshness and can also affect shared caches.
- `Surrogate-Control` sets a separate lifetime for the Adobe managed CDN.
- Dispatcher uses its own rules and may use expiration headers when TTL is enabled.

## Slide 04 · A response is more than a status
- Example evidence: `200 · Version A`, `Cache-Control: max-age=300`, `Surrogate-Control: max-age=3600`, `Age: 900`, no `Set-Cookie`.
- Capture URL, status, marker, headers and time.
- HTTP 200 or `Age` alone does not prove which layer served a response.

## Slide 05 · Did the browser make a request?
- Compare normal browser navigation with DevTools Network and a fresh command-line GET.
- Inspect whether the browser used memory/disk cache or made a network request.
- Record whether DevTools "Disable cache" was off and inspect both request and response.

## Slide 06 · CDN log fields
- The illustrated log is simulated: `rid`, Host, URL, `cache`, `res_age` and POP describe one edge response.
- `HIT` serves from edge, `MISS` fetches origin, `PASS` does not cache.
- A local Dispatcher Tools run cannot reproduce the managed CDN.

## Slide 07 · Private content and cookies
- CDN does not cache responses with `private`, `no-cache`, `no-store` or `Set-Cookie`.
- Check Dispatcher separately; a CDN privacy header alone does not make Dispatcher safe.
- Do not put user-specific HTML behind a shared cache rule.

## Slide 08 · Query strings can change the test
- CDN key includes the full URL, subject to configured removal of marketing parameters.
- Dispatcher uses `/ignoreUrlParams`; check its effective rule for the parameter.
- Never assume a random query parameter bypasses both caches.
- Preserve the original URL while diagnosing; inspect effective rules.

## Slide 09 · Versioned client libraries
- AEM Cloud enables strict clientlib versioning; the URL includes an `lc-...-lc` hash selector.
- New CSS/JS gets a new URL; HTML must refresh to reference it.
- Compare the HTML link before blaming the clientlib cache.

## Slide 10 · Case: B, B, A
- At 10:00 Publish B; at 10:01 Dispatcher B; at 10:02 public CDN GET A for the same Host and URL.
- CDN log `HIT`, `res_age: 900`, `pop: MAD` supports a stale edge object.
- If the CDN log says `MISS`, verify origin, Host and marker again.

## Slide 11 · Key Takeaways
- Matching Host, path, and query make responses comparable.
- Browser Network identifies local cache hits.
- The first stale layer determines the proposed fix.

## Slide 12 · Questions
- Explain how local browser and Dispatcher evidence identifies the first stale layer.
