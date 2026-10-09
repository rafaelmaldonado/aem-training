package com.adobe.aem.guides.wknd.core.training;

import java.util.Collections;
import org.apache.sling.api.resource.LoginException;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.apache.sling.api.resource.ResourceResolverFactory;
import org.apache.sling.event.jobs.Job;
import org.apache.sling.event.jobs.JobManager;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import com.adobe.granite.workflow.WorkflowException;
import com.adobe.granite.workflow.WorkflowSession;
import com.adobe.granite.workflow.exec.WorkItem;
import com.adobe.granite.workflow.exec.WorkflowProcess;
import com.adobe.granite.workflow.metadata.MetaDataMap;

@Component(service = WorkflowProcess.class, property = "process.label=Training: queue Guide batches")
public class QueueGuidesProcess implements WorkflowProcess {
    static final String TOPIC = "training/session41/guides";
    static final String CONTROL = "/content/session-41-demo/control";
    static final String SUBSERVICE = "training-session-41";
    private static final Logger LOG = LoggerFactory.getLogger(QueueGuidesProcess.class);

    @Reference
    private JobManager jobManager;

    @Reference
    private ResourceResolverFactory resolverFactory;

    @Override
    public void execute(WorkItem item, WorkflowSession session, MetaDataMap args)
            throws WorkflowException {
        if (!"JCR_PATH".equals(item.getWorkflowData().getPayloadType())
                || !CONTROL.equals(String.valueOf(item.getWorkflowData().getPayload()))) {
            throw new WorkflowException("Expected JCR_PATH payload " + CONTROL);
        }

        try (ResourceResolver resolver = resolverFactory.getServiceResourceResolver(
                Collections.singletonMap(ResourceResolverFactory.SUBSERVICE, SUBSERVICE))) {
            Resource control = resolver.getResource(CONTROL);
            if (control == null) {
                throw new WorkflowException("Control node missing or unreadable: " + CONTROL);
            }
            String version = control.getValueMap().get("requestedVersion", String.class);
            if (version == null || !version.matches("v[0-9]+")) {
                throw new WorkflowException("requestedVersion must look like v1, v2, ...");
            }
            Job job = jobManager.addJob(TOPIC, Collections.singletonMap("version", version));
            if (job == null) {
                throw new WorkflowException("Sling did not accept the Guide job");
            }
            LOG.info("Session 41 queued job={} version={} workflow={}",
                    job.getId(), version, item.getWorkflow().getId());
        } catch (LoginException e) {
            throw new WorkflowException("Session 41 service mapping failed", e);
        }
    }
}
