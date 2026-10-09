package com.adobe.aem.guides.wknd.core.training;

import java.util.Collections;
import org.apache.sling.api.resource.LoginException;
import org.apache.sling.api.resource.ModifiableValueMap;
import org.apache.sling.api.resource.PersistenceException;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.apache.sling.api.resource.ResourceResolverFactory;
import org.apache.sling.event.jobs.Job;
import org.apache.sling.event.jobs.consumer.JobConsumer;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(service = JobConsumer.class,
        property = JobConsumer.PROPERTY_TOPICS + "=" + QueueGuidesProcess.TOPIC)
public class GuideBatchJobConsumer implements JobConsumer {
    private static final Logger LOG = LoggerFactory.getLogger(GuideBatchJobConsumer.class);
    private static final String GUIDES = "/content/session-41-demo/guides/";
    private static final String[] BATCHES = {"guide-a", "guide-b"};

    @Reference
    ResourceResolverFactory resolverFactory;

    @Override
    public JobResult process(Job job) {
        String version = job.getProperty("version", String.class);
        if (version == null || !version.matches("v[0-9]+")) {
            LOG.error("Session 41 job={} has invalid version={}", job.getId(), version);
            return JobResult.CANCEL;
        }

        try (ResourceResolver resolver = resolverFactory.getServiceResourceResolver(
                Collections.singletonMap(ResourceResolverFactory.SUBSERVICE,
                        QueueGuidesProcess.SUBSERVICE))) {
            for (String name : BATCHES) {
                Resource guide = resolver.getResource(GUIDES + name);
                ModifiableValueMap values = guide == null ? null : guide.adaptTo(ModifiableValueMap.class);
                if (values == null) {
                    LOG.error("Session 41 fixture missing or not writable: {}{}", GUIDES, name);
                    return JobResult.CANCEL;
                }
                if (version.equals(values.get("processedVersion", String.class))) {
                    LOG.info("Session 41 job={} skip={} already at {}", job.getId(), name, version);
                    continue;
                }

                int count = values.get("applyCount", 0);
                values.put("processedVersion", version);
                values.put("applyCount", count + 1);
                resolver.commit(); // Effect and checkpoint for this item are saved together.
                LOG.info("Session 41 job={} applied={} version={} count={}",
                        job.getId(), name, version, count + 1);

                if ("guide-a".equals(name) && job.getRetryCount() == 0) {
                    LOG.warn("Session 41 deliberate failure after first committed batch; retry job={}",
                            job.getId());
                    return JobResult.FAILED;
                }
            }
            LOG.info("Session 41 job={} complete version={} retry={}",
                    job.getId(), version, job.getRetryCount());
            return JobResult.OK;
        } catch (LoginException e) {
            LOG.error("Session 41 service mapping failed", e);
            return JobResult.CANCEL;
        } catch (PersistenceException e) {
            LOG.warn("Session 41 repository write failed; job may retry", e);
            return JobResult.FAILED;
        }
    }
}
