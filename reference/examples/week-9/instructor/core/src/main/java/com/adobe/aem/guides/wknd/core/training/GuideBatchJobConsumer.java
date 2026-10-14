package com.adobe.aem.guides.wknd.core.training;

import java.util.Collections;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
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
    private static final String GUIDES = "/content/session-41-demo/guides";
    private static final int TOTAL = 300;
    private static final int BATCH_SIZE = 25;

    @Reference
    ResourceResolverFactory resolverFactory;

    @Override
    public JobResult process(Job job) {
        String version = job.getProperty("version", String.class);
        if (version == null || !version.matches("v[0-9]+")) {
            LOG.error("Week 9 job={} has invalid version={}", job.getId(), version);
            return JobResult.CANCEL;
        }

        try (ResourceResolver resolver = resolverFactory.getServiceResourceResolver(
                Collections.singletonMap(ResourceResolverFactory.SUBSERVICE,
                        QueueGuidesProcess.SUBSERVICE))) {
            Resource guides = resolver.getResource(GUIDES);
            ModifiableValueMap progress = guides == null ? null : guides.adaptTo(ModifiableValueMap.class);
            if (progress == null) {
                LOG.error("Week 9 guides folder missing or not writable: {}", GUIDES);
                return JobResult.CANCEL;
            }

            for (int end = BATCH_SIZE; end <= TOTAL; end += BATCH_SIZE) {
                boolean changed = false;
                for (int number = end - BATCH_SIZE + 1; number <= end; number++) {
                    String name = String.format(Locale.ROOT, "guide-%04d", number);
                    Resource guide = resolver.getResource(GUIDES + "/" + name);
                    if (guide == null) {
                        Map<String, Object> properties = new HashMap<>();
                        properties.put("jcr:primaryType", "nt:unstructured");
                        properties.put("processedVersion", version);
                        properties.put("applyCount", 1);
                        resolver.create(guides, name, properties);
                        changed = true;
                    } else {
                        ModifiableValueMap values = guide.adaptTo(ModifiableValueMap.class);
                        if (values == null) {
                            LOG.error("Week 9 guide not writable: {}", guide.getPath());
                            return JobResult.CANCEL;
                        }
                        if (!version.equals(values.get("processedVersion", String.class))) {
                            values.put("processedVersion", version);
                            values.put("applyCount", values.get("applyCount", 0) + 1);
                            changed = true;
                        }
                    }
                }

                if (changed || !version.equals(progress.get("processedVersion", String.class))
                        || progress.get("completed", 0) < end) {
                    progress.put("processedVersion", version);
                    progress.put("completed", end);
                    progress.put("lastGuide", String.format(Locale.ROOT, "guide-%04d", end));
                    resolver.commit(); // Batch and checkpoint must survive or fail together.
                    LOG.info("Week 9 job={} version={} completed={}/{}", job.getId(), version, end, TOTAL);
                }

                if (end == 100 && changed && job.getRetryCount() == 0) {
                    LOG.warn("Week 9 deliberate failure after 100 committed Guides; job={}", job.getId());
                    return JobResult.FAILED;
                }
            }
            LOG.info("Week 9 job={} complete version={} retry={}",
                    job.getId(), version, job.getRetryCount());
            return JobResult.OK;
        } catch (LoginException e) {
            LOG.error("Week 9 service mapping failed", e);
            return JobResult.CANCEL;
        } catch (PersistenceException e) {
            LOG.warn("Week 9 repository write failed; job may retry", e);
            return JobResult.FAILED;
        }
    }
}
