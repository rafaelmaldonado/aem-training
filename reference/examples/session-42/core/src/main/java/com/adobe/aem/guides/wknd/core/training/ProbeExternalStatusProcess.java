package com.adobe.aem.guides.wknd.core.training;

import com.adobe.granite.workflow.WorkflowException;
import com.adobe.granite.workflow.WorkflowSession;
import com.adobe.granite.workflow.exec.WorkItem;
import com.adobe.granite.workflow.exec.WorkflowProcess;
import com.adobe.granite.workflow.metadata.MetaDataMap;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(service = WorkflowProcess.class, property = "process.label=Training: probe external status")
public class ProbeExternalStatusProcess implements WorkflowProcess {
    private static final Logger LOG = LoggerFactory.getLogger(ProbeExternalStatusProcess.class);

    @Reference
    private ExternalStatusService statusService;

    @Override
    public void execute(WorkItem item, WorkflowSession session, MetaDataMap args)
            throws WorkflowException {
        if (!"JCR_PATH".equals(item.getWorkflowData().getPayloadType())) {
            throw new WorkflowException("Expected a JCR_PATH payload");
        }
        ExternalStatusService.Outcome outcome = statusService.check();
        LOG.info("Session 42 workflow={} outcome={}", item.getWorkflow().getId(), outcome);
        if (outcome != ExternalStatusService.Outcome.OK) {
            throw new WorkflowException("External status check: " + outcome
                    + "; inspect upstream status and configuration before rerunning");
        }
    }
}
