package com.adobe.aem.guides.wknd.core.training;

import com.adobe.granite.workflow.WorkflowSession;
import com.adobe.granite.workflow.exec.WorkItem;
import com.adobe.granite.workflow.exec.WorkflowProcess;
import com.adobe.granite.workflow.metadata.MetaDataMap;
import org.osgi.service.component.annotations.Component;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(
        service = WorkflowProcess.class,
        property = "process.label=Training: log payload")
public class LogPayloadProcess implements WorkflowProcess {
    private static final Logger LOG = LoggerFactory.getLogger(LogPayloadProcess.class);

    @Override
    public void execute(WorkItem item, WorkflowSession session, MetaDataMap args) {
        LOG.info("Training workflow: instance={}, payloadType={}, payload={}",
                item.getWorkflow().getId(),
                item.getWorkflowData().getPayloadType(),
                item.getWorkflowData().getPayload());
    }
}
