package com.adobe.aem.guides.wknd.core.training;

import java.util.Collections;
import org.apache.sling.api.resource.LoginException;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.apache.sling.api.resource.ResourceResolverFactory;
import org.apache.sling.serviceusermapping.ServiceUserMapped;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.ConfigurationPolicy;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(service = TrainingGuideReader.class, immediate = true,
    configurationPolicy = ConfigurationPolicy.REQUIRE,
    reference = @Reference(name = "serviceMapping", service = ServiceUserMapped.class,
        target = "(subServiceName=training-guide-read)"))
public class TrainingGuideReader {
    private static final Logger LOG = LoggerFactory.getLogger(TrainingGuideReader.class);
    private static final String PATH = "/content/training-permissions/guides";

    @Reference
    ResourceResolverFactory resolverFactory;

    public String readWithService() throws LoginException {
        try (ResourceResolver resolver = resolverFactory.getServiceResourceResolver(
                Collections.singletonMap(ResourceResolverFactory.SUBSERVICE, "training-guide-read"))) {
            return readWith(resolver);
        }
    }

    // Borrowed resolver: its caller owns the lifecycle.
    public String readWith(ResourceResolver resolver) {
        Resource resource = resolver.getResource(PATH);
        if (resource == null) {
            throw new IllegalStateException("Folder missing or unreadable: " + PATH);
        }
        return resource.getValueMap().get("jcr:title", resource.getName());
    }

    @Activate
    protected void activate() {
        try {
            LOG.info("Training guide title: {}", readWithService());
        } catch (LoginException e) {
            LOG.error("Training service login failed; inspect mapping and principal", e);
        } catch (IllegalStateException e) {
            LOG.error("Training read failed; inspect fixture and read permissions", e);
        }
    }
}
