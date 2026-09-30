# Session 36 · Choose the delivery path

Twelve English PNG slides in the established **technical atlas courseware** style; Spanish theoretical study guide and a simulated Cloud Manager case. No Cloud Manager access, terminal lab or PPTX required.

## Slide 01 · Choose the delivery path
- Class 36 · Week 8 · October 5, 2026 · Juan Maldonado.
- For a proposed change, identify its source commit, pipeline, artifact and destination.

## Slide 02 · Code delivery has four coordinates
- Program → environment → repository/branch → pipeline run.
- Record the commit SHA and the code location selected by the pipeline.
- A successful local build does not show what Cloud Manager deployed.

## Slide 03 · Production or non-production?
- A non-production deployment pipeline targets a development environment.
- A standard production pipeline deploys to stage, then to production after its gates and approval.
- A code-quality pipeline scans without deploying; never call its result a release.

## Slide 04 · Choose by the changed files
- Java, OSGi, Repo Init or AEM packages → full-stack.
- A separately managed site theme/static UI → front-end, if the site uses that contract.
- Apache/Dispatcher configuration → web tier config.
- Supported log forwarding configuration → config pipeline.

## Slide 05 · Full-stack owns the AEM application
- Builds and deploys server code and packaged clientlibs.
- Can also deploy Dispatcher configuration when no web tier pipeline owns it.
- Separate content publication from code deployment.

## Slide 06 · Front-end has a distinct artifact
- Cloud Manager runs the front-end build and deploys the resulting static files.
- Check that the site references that theme and that its HTML/JSON contract remains compatible.
- A CSS file packaged as an AEM clientlib in the full-stack project follows the full-stack path.

## Slide 07 · Web tier and config are different
- Web tier config deploys Apache/Dispatcher files.
- Config deploys supported CDN, log-forwarding and maintenance configuration.
- If a web tier pipeline exists for an environment, its full-stack pipeline ignores Dispatcher files.

## Slide 08 · Trace one release
- Change → commit SHA → selected repository, branch and code location.
- Pipeline run → built artifact → target environment.
- Verify the active result at the affected boundary; status alone is insufficient.

## Slide 09 · Case: the fix is in Git, but not in dev
- Commit `c36b2` changes a Dispatcher vhost on `feature/host-fix`.
- The development web tier pipeline reads `main`, whose tip is still `a36f1`.
- The green run proves only that `main` was deployed; a future run would need `c36b2` to include the fix.

## Slide 10 · Four change cards
- Sling Model + OSGi config → full-stack.
- Standalone site theme → front-end; packaged clientlib → full-stack.
- Dispatcher vhost → web tier; log forwarding → config.
- For each card, state repository/branch, artifact owner and destination.

## Slide 11 · Key takeaways
- Select the pipeline from the changed asset and its current owner.
- Match the expected commit to the source used by the run.
- Deployment, publication and cache refresh are separate observations.

## Slide 12 · Questions
- Thank you.

## Official sources
- [Cloud Manager CI/CD pipelines](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/introduction-ci-cd-pipelines)
- [Production pipelines](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/cicd-pipelines/configuring-production-pipelines)
- [Repositories](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/using-cloud-manager/managing-code/managing-repositories)
