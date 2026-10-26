# Solution design: JPEG 800 rendition for Assets

## Goal and scope

When an image is uploaded or updated under `/content/dam/assets`, generate the `assets.800x800.jpeg` rendition: a JPEG with a maximum width and height of 800 px, preserved aspect ratio, and quality 85. The rule covers subfolders, excludes other asset types, and does not affect folders outside this path.

This example provides two ways to achieve the same observable result. In AEM as a Cloud Service, a **Processing Profile** and Asset Microservices handle processing. In the local SDK Author, a separate workflow reproduces the automatic flow so uploads and renditions can be tested without access to those microservices. The local workflow is not part of the Cloud Manager deployment.

## Design

```text
Cloud:  image uploaded to /content/dam/assets/**
        → Processing Profile assigned to the folder
        → Asset Microservices → assets.800x800.jpeg

Local:  original uploaded or replaced in /content/dam/assets/**
        → create/modify launcher → workflow model → Process Step
        → ImageIO → assets.800x800.jpeg
```

## Files to review

| File in this example | Purpose |
| --- | --- |
| [Profile](ui.content/src/main/content/jcr_root/conf/global/settings/dam/processing/assets-jpeg-800/.content.xml) and [JPEG rule](ui.content/src/main/content/jcr_root/conf/global/settings/dam/processing/assets-jpeg-800/jpeg-800/.content.xml) | Define the Cloud rendition. |
| [Folder assignment](ui.content/src/main/content/jcr_root/content/dam/assets/_jcr_content/.content.xml) and [FileVault filter](ui.content/src/main/content/META-INF/vault/filter.xml) | Apply and package the profile under `/content/dam/assets`. |
| [Process Step](local-tools/workflow/bundle/src/main/java/com/example/assets/local/workflow/Jpeg800WorkflowProcess.java) and [JUnit test](local-tools/workflow/bundle/src/test/java/com/example/assets/local/workflow/Jpeg800WorkflowProcessTest.java) | Generate and verify the rendition in the local Author. |
| [Model](local-tools/workflow/package/src/main/content/jcr_root/conf/global/settings/workflow/models/assets-local-jpeg-800/.content.xml), [create launcher](local-tools/workflow/package/src/main/content/jcr_root/conf/global/settings/workflow/launcher/config/assets-local-jpeg-800-create/.content.xml), and [modify launcher](local-tools/workflow/package/src/main/content/jcr_root/conf/global/settings/workflow/launcher/config/assets-local-jpeg-800-modify/.content.xml) | Run the Process Step when the original is uploaded or replaced. |
| [Local Maven reactor](local-tools/workflow/pom.xml) and [installer](local-tools/workflow/install.py) | Build, install, and synchronize the workflow only in the local SDK. |
| [Manual generator](local-tools/generate-rendition.py) | Diagnostic helper for macOS. |

### Cloud path

- `ui.content/.../conf/global/settings/dam/processing/assets-jpeg-800/` defines the profile and its `jpeg-800` rendition (`fmt=jpeg`, `wid=800`, `hei=800`, `qlt=85`, `includeMimeTypes=image/.*`).
- `ui.content/.../content/dam/assets/_jcr_content/.content.xml` assigns `processingProfile=/conf/global/settings/dam/processing/assets-jpeg-800` to the DAM folder. Subfolders inherit the assignment unless a subfolder has another profile.
- `ui.content/src/main/content/META-INF/vault/filter.xml` must include the profile and folder-property roots. When integrating into another project, **merge** these entries into the existing filter; do not replace the entire filter.
- The definition belongs in the normal AEM reactor's `ui.content` package. Cloud Manager deploys that package, and AEM processes images with its managed services. Existing assets need **Reprocess Assets** to receive the new rendition.

### Local Author path

- `local-tools/workflow/bundle/.../Jpeg800WorkflowProcess.java` implements `WorkflowProcess`. It checks the payload, path, and MIME type; reads the original; scales it to fit within 800 × 800 without distortion; composites transparency onto white; and writes `image/jpeg` at quality 0.85. It does not enlarge small originals.
- `local-tools/workflow/package/` installs the bundle, model, and two launchers on `jcr:content/renditions/original`: one for creation and one for modification. Listening only to the original prevents the new rendition from triggering the workflow again. The launchers use `runModes=author`, so **that setting alone does not distinguish** local Author from Cloud Author.
- `local-tools/workflow/pom.xml` is a separate Maven reactor that inherits from the root AEM POM. It must stay out of the main POM's modules and the `all` package; that separation is the deployment boundary.
- `local-tools/workflow/install.py` builds the package, installs it on the Author SDK at `localhost:4502`, and synchronizes the model. It reads the password from `AEM_ADMIN_PASSWORD` or `../author/.admin-password` relative to the AEM project root.
- `local-tools/generate-rendition.py` is a manual macOS diagnostic command (`sips`). It is not part of the automatic upload flow.

### Asset Compute CLI for local development of custom workers

The `aio asset-compute` commands are for **custom Asset Compute workers** in an Adobe Developer App Builder project. This example has no custom worker: its Cloud rendition uses a built-in Processing Profile rule, and its local rendition uses the Java workflow above. Running the CLI from this example cannot execute either implementation or make the local AEM SDK use Asset Microservices.

If you also develop a custom worker, configure its App Builder project and workspace with the required Adobe services, integration credentials, and S3 or Azure test storage. Keep `.env` and downloaded credentials out of source control. Then run these commands from the **custom worker project's root**:

```sh
npm install
aio app run
```

`aio app run` deploys the worker to Adobe I/O Runtime and opens the Asset Compute Development Tool at `http://localhost:9000`. Select a source image, set the deployed worker URL and rendition name in the tool's profile, then click **Run** to inspect the output and logs. The browser URL needs the token generated by the command. Do not use `aio app run --local`: the Asset Compute service cannot call an action running only on your computer.

To start the Development Tool separately, deploy the worker and run this from its project root instead of keeping an `aio app run` session open:

```sh
aio app deploy
aio asset-compute devtool
```

With Docker running, you can instead execute a custom worker on a local file without the Development Tool:

```sh
aio asset-compute run-worker /path/to/source.jpg /tmp/assets.800x800.jpeg
```

If `aio asset-compute` is unavailable, install the [Asset Compute CLI plugin](https://github.com/adobe/aio-cli-plugin-asset-compute) with `aio plugins:install @adobe/aio-cli-plugin-asset-compute`. All three commands require a custom worker project; they do not test the built-in JPEG rule in this example. See Adobe's [App Builder setup](https://experienceleague.adobe.com/en/docs/asset-compute/using/extend/develop-custom-application) and [Development Tool guide](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/asset-compute/develop/development-tool) for the credentials and profile format. Adobe also notes that the Development Tool currently does not work for custom workers created with OAuth credentials; check the project's authentication setup before relying on it.

## Integration and operation

This training repository stores the files as an example using paths relative to an AEM project. It is not a standalone AEM Maven reactor: copy `ui.content/` and `local-tools/` to the root of an archetype-based project, merging `filter.xml` and the `processingProfile` property with existing content. The local reactor expects `groupId=com.example.assets`, `artifactId=assets`, and `version=1.0.0-SNAPSHOT`; adapt those three values and the Java package if the receiving project uses different coordinates.

1. Build the normal AEM project with `./mvnw clean install` and, locally, install it with `./mvnw clean install -PautoInstallSinglePackage`.
2. To test the local flow, start the Author SDK on port 4502 and run `python3 local-tools/workflow/install.py` from the AEM project root.
3. Upload an image larger than 800 px under `/content/dam/assets`; check `assets.800x800.jpeg` and its dimensions under **Renditions**. Replace the original and check that the rendition is regenerated.
4. Upload an image outside that folder and a non-image file inside it; check that neither receives the rendition.
5. In Cloud, deploy only the normal AEM project. Verify that **Assets JPEG 800** appears under **Tools → Assets → Processing Profiles**, is assigned to the folder, and produces the rendition for a new upload. Reprocess existing assets when appropriate.

## Acceptance criteria and verification status

| Criterion | Local SDK | Cloud |
| --- | --- | --- |
| Image inside the folder produces a JPEG within 800 × 800 | Verified: 1600 × 600 → 800 × 300 in a JUnit test; an actual upload produced the rendition | Pending validation in an AEM as a Cloud Service environment |
| Replacing the original updates the rendition | Verified in local Author | Pending |
| Image outside the folder and non-image file inside it do not produce the rendition | Verified in local Author | Pending |
| Local reactor is separate from the `all` package | Verified in POMs | Check the final package in the pipeline |

The last recorded local test used the SDK available in the original project; the workflow reactor built and passed its two tests before the files were moved. A full archetype rebuild after the move stopped at `npm ci` in `ui.frontend`; the example's XML, links, and scripts were validated. After integrating the files, repeat the build and upload test in the receiving AEM project. The local SDK may omit formats that `ImageIO` cannot decode; validate Asset Microservices behavior separately. A DAM folder can have only one effective Processing Profile: if it already has one, add this rendition to that profile or decide which profile should take precedence.

## References

- Adobe: [Configure and use asset microservices](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/manage/asset-microservices-configure-and-use).
- Adobe: [AEM as a Cloud Service SDK](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/developing/aem-as-a-cloud-service-sdk).
- Adobe: [Process assets using asset microservices](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/assets/asset-microservices-overview).
- Adobe: [Develop a custom Asset Compute application](https://experienceleague.adobe.com/en/docs/asset-compute/using/extend/develop-custom-application).
- Adobe: [Asset Compute Development Tool](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/asset-compute/develop/development-tool).
