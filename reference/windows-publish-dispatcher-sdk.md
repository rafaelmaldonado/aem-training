# AEM Publish and Dispatcher on Windows: Docker, WSL, or IIS

Choose the first available route:

| Priority | Dispatcher route | Where Dispatcher runs | Cloud configuration fidelity |
|---|---|---|---|
| 1 | Docker Desktop | **Cloud SDK Dispatcher Tools** container on Windows | Runs the project's `dispatcher/src` configuration |
| 2 | WSL, without Docker | Apache and the **standalone Linux Dispatcher module** inside Ubuntu | Uses a separate Apache/`dispatcher.any` setup; does not run the Cloud SDK container |
| 3 | IIS, without Docker or WSL | **Standalone Windows IIS Dispatcher module** | Uses a separate IIS/`dispatcher.any` setup |

**Choose Docker when available.** Adobe's AEM as a Cloud Service SDK provides its local Dispatcher runtime as a Docker image. WSL alone does not run that image; the WSL and IIS routes below use Adobe's separately distributed Dispatcher modules. They can exercise local requests and cache behavior but do **not** prove that a Cloud project's Apache and Dispatcher configuration will deploy. This is an inference from Adobe's [Cloud Dispatcher Tools](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools) and [standalone Dispatcher installation](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/getting-started/dispatcher-install). Adobe does not document either standalone module paired with Cloud SDK Publish as a supported Cloud setup.

This repository contains course material, not an AEM Maven project. Replace `C:\dev\my-project` with the path to your actual project. Download the current AEM as a Cloud Service SDK ZIP from [Adobe Software Distribution](https://experience.adobe.com/#/downloads/content/software-distribution/en/aemcloud.html), then extract it. Use the JDK required by that SDK version (JDK 21 for the current SDK). [Adobe local SDK guide](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/aem-runtime)

## Shared prerequisite: Publish runs on Windows

Your local Author already runs on port 4502. Run a **separate Publish instance on Windows** on port 4503 for any Dispatcher route below. Create `C:\aem-sdk\publish`, copy the SDK Quickstart JAR into it, rename the copy `aem-publish-p4503.jar`, and start it from Command Prompt:

```cmd
cd /d C:\aem-sdk\publish
java -jar aem-publish-p4503.jar
```

Set the local admin password on first startup, then verify a known published page at `http://localhost:4503`. Keep this terminal open. If `C:\aem-sdk` is not writable, choose another folder and adjust the command. A fresh Publish instance may have no sample site. [Adobe Publish setup](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/aem-runtime)

## 1. Docker Desktop available: use the Cloud SDK Dispatcher Tools

1. Install and start Docker Desktop. Check `docker info` in Command Prompt.
2. Extract the SDK's `aem-sdk-dispatcher-tools-XXX-windows.zip` so `C:\aem-sdk\dispatcher\bin\docker_run.cmd` and `src` exist. Use a path without spaces or special characters; Adobe warns that the Windows runner can fail otherwise.
3. In a second Command Prompt, run the default configuration:

   ```cmd
   cd /d C:\aem-sdk\dispatcher
   bin\docker_run src host.docker.internal:4503 8080
   ```

4. Open `http://localhost:8080`. To test your project's configuration, stop the runner with `Ctrl+C` and rerun it with the actual project path:

   ```cmd
   bin\docker_run C:\dev\my-project\dispatcher\src host.docker.internal:4503 8080
   ```

Test the same published page through ports 4503 and 8080. Restart `docker_run` after configuration edits on Windows; the hot-reload script is not available there. If `host.docker.internal` does not resolve, Adobe says to use the Windows host IPv4 address from `ipconfig`. [Adobe Dispatcher Tools setup](https://experienceleague.adobe.com/en/docs/experience-manager-learn/cloud-service/local-development-environment-set-up/dispatcher-tools) · [Validation and Windows hot-reload limit](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/validation-debug)

## 2. WSL available, Docker unavailable: use Apache and the Linux module

This route runs **only Dispatcher inside Ubuntu on WSL** and connects it to the Publish instance on Windows. It adapts Adobe's Linux Apache instructions to WSL; Adobe does not list WSL as a tested Dispatcher platform. It uses the standalone Linux Dispatcher package, **not** the Cloud SDK Dispatcher container.

1. If WSL is not installed, run `wsl --install -d Ubuntu-24.04` in an elevated Windows terminal, restart Windows, and finish Ubuntu's first-run setup. If it is already installed, open Ubuntu. Check `wsl --list --online` if `Ubuntu-24.04` is not offered. [Microsoft WSL installation](https://learn.microsoft.com/en-us/windows/wsl/install)
2. In Ubuntu, install Apache and the tools needed to check the Windows connection:

   ```bash
   sudo apt update
   sudo apt install apache2 curl openssl
   ```

3. From Ubuntu, find an address that reaches **Windows Publish**. Try loopback first; it works with WSL mirrored networking. If it fails, get the Windows host IP used by WSL's default NAT mode and test that address:

   ```bash
   curl -I http://127.0.0.1:4503/
   ip route show | grep -i default | awk '{ print $3}'
   curl -I http://WINDOWS_HOST_IP:4503/
   ```

   Replace `WINDOWS_HOST_IP` with the address printed by the middle command. Use whichever address responds in this step. If neither works, confirm Publish is running and that Windows allows connections to port 4503 on the selected interface. On Windows 11 22H2 or later, [WSL mirrored networking](https://learn.microsoft.com/en-us/windows/wsl/networking) is another way to make `127.0.0.1` work. Do not proceed until Ubuntu can reach Publish.
4. Download Adobe's latest **Apache 2.4 Linux Dispatcher** archive matching your WSL architecture and OpenSSL version from the [Dispatcher release notes](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/getting-started/release-notes). In Ubuntu, check `uname -m` and `openssl version` before selecting the archive. This is a separate download from the Cloud SDK. Extract it inside Ubuntu and read its README. Copy its Dispatcher `.so` file to `/usr/lib/apache2/modules/mod_dispatcher.so` and its sample `dispatcher.any` to `/etc/apache2/dispatcher.any`. [Adobe Apache module installation](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/getting-started/dispatcher-install)
5. Edit the sample `/etc/apache2/dispatcher.any`: set its existing `/renders /hostname` to the **working Windows address from step 3** and `/port` to `4503`; set `/cache /docroot` to `/var/www/html` (Apache's document root). Keep the sample's filter rules. Do not copy the Cloud project's `dispatcher/src` into this standalone setup. [Adobe renderer and cache configuration](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/configuring/dispatcher-configuration)
6. Create `/etc/apache2/mods-available/dispatcher.load` containing:

   ```apache
   LoadModule dispatcher_module /usr/lib/apache2/modules/mod_dispatcher.so
   ```

   Create `/etc/apache2/conf-available/dispatcher.conf` containing:

   ```apache
   <IfModule disp_apache2.c>
     DispatcherConfig /etc/apache2/dispatcher.any
     DispatcherLog /var/log/apache2/dispatcher.log
     DispatcherLogLevel 3
   </IfModule>
   ```

   Inside the existing `<VirtualHost *:80>` in `/etc/apache2/sites-available/000-default.conf`, add:

   ```apache
   <Directory /var/www/html>
     Options FollowSymLinks
     AllowOverride None
     Require all granted
     <IfModule disp_apache2.c>
       SetHandler dispatcher-handler
       ModMimeUsePathInfo On
     </IfModule>
   </Directory>
   ```

7. Enable the module and configuration, then check Apache before restarting it:

   ```bash
   sudo a2enmod dispatcher
   sudo a2enconf dispatcher
   sudo chown -R www-data:www-data /var/www/html
   sudo apache2ctl -t
   sudo service apache2 restart
   ```

8. Open a known published page at `http://localhost:4503/...`, then the same path at `http://localhost/...` from Windows. Microsoft documents localhost forwarding from WSL to Windows. If Apache fails its syntax check or module load, check the archive architecture and shared-library dependencies with `ldd /usr/lib/apache2/modules/mod_dispatcher.so`; use `/var/log/apache2/dispatcher.log` for request errors. [Microsoft WSL networking](https://learn.microsoft.com/en-us/windows/wsl/networking) · [Ubuntu Apache configuration](https://ubuntu.com/server/docs/how-to/web-services/install-apache2/) · [Adobe Dispatcher directives](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/getting-started/dispatcher-install)

## 3. Neither Docker nor WSL available: use IIS on Windows

This route needs permission to enable IIS 10 and its ISAPI Extensions Windows feature. It uses Adobe's standalone IIS Dispatcher ZIP, **not** the Cloud SDK Dispatcher Tools.

1. In **Turn Windows features on or off**, enable **Internet Information Services → World Wide Web Services → Application Development Features → ISAPI Extensions**. [Adobe supported platforms](https://experienceleague.adobe.com/en/docs/experience-manager-65/content/implementing/deploying/introduction/technical-requirements) · [Microsoft ISAPI setup](https://learn.microsoft.com/en-us/iis/configuration/system.webServer/security/isapiCgiRestriction/add)
2. Download the latest **Windows x64 IIS Dispatcher ZIP** from [Adobe Dispatcher release notes](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/getting-started/release-notes). Read its README. Extract `disp_iis.dll`, `disp_iis.ini`, and the supplied publish `dispatcher.any` into `C:\inetpub\Scripts`.
3. Set `C:\inetpub\Scripts\disp_iis.ini` to point to that sample:

   ```ini
   [main]
   configpath=C:\inetpub\Scripts\dispatcher.any
   loglevel=3
   servervariables=1
   replaceauthorization=0
   ```

4. In the sample `dispatcher.any`, set its existing `/renders` host to `127.0.0.1` and port to `4503`. Set `/cache /docroot` to the IIS site's physical path. Keep its filter rules. Do not copy the Cloud project's `dispatcher/src` into IIS.
5. Create `C:\inetpub\wwwroot\aem-local`. In IIS Manager, create a site bound to **127.0.0.1:8080** with that physical path. Set `/cache /docroot` to the same path and grant the site's application-pool identity write access to it. [Adobe cache permissions](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/getting-started/dispatcher-install) · [Microsoft site creation](https://learn.microsoft.com/en-us/iis/get-started/getting-started-with-iis/create-a-web-site)
6. On that site, open **Handler Mappings → Add Wildcard Script Map**: request path `*`, executable `C:\inetpub\Scripts\disp_iis.dll`, name `Dispatcher`. Allow the module in **ISAPI and CGI Restrictions** when prompted and enable **Anonymous Authentication** for public Publish pages. [Adobe IIS handler setup](https://experienceleague.adobe.com/en/docs/experience-manager-dispatcher/using/getting-started/dispatcher-install)
7. Check a known public page at `http://localhost:4503/...`, then at `http://127.0.0.1:8080/...`. The second request goes through IIS Dispatcher. With no `logfile` setting, check the Windows Event Log if it fails.

If IIS also cannot be enabled, there is no local Dispatcher runtime from these three routes. Publish at port 4503 and the SDK's standalone `validator.exe` can still be used, but neither simulates Dispatcher requests or caching. [Adobe validation phases](https://experienceleague.adobe.com/en/docs/experience-manager-cloud-service/content/implementing/content-delivery/validation-debug)
