package com.adobe.aem.guides.wknd.core.training;

import java.util.HashMap;
import java.util.Map;
import org.apache.sling.api.resource.ModifiableValueMap;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.apache.sling.api.resource.ResourceResolverFactory;
import org.apache.sling.api.wrappers.ModifiableValueMapDecorator;
import org.apache.sling.event.jobs.Job;
import org.apache.sling.event.jobs.consumer.JobConsumer.JobResult;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.anyMap;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class GuideBatchJobConsumerTest {
    @Test
    void createsThreeHundredGuidesResumesAndSkipsReplay() throws Exception {
        ResourceResolverFactory factory = mock(ResourceResolverFactory.class);
        ResourceResolver resolver = mock(ResourceResolver.class);
        Resource guides = mock(Resource.class);
        Map<String, Object> progressState = new HashMap<>();
        Map<String, Map<String, Object>> children = new HashMap<>();
        when(factory.getServiceResourceResolver(anyMap())).thenReturn(resolver);
        when(guides.adaptTo(ModifiableValueMap.class))
                .thenReturn(new ModifiableValueMapDecorator(progressState));
        when(resolver.getResource(anyString())).thenAnswer(invocation -> {
            String path = invocation.getArgument(0);
            if ("/content/session-41-demo/guides".equals(path)) {
                return guides;
            }
            Map<String, Object> state = children.get(path);
            if (state == null) {
                return null;
            }
            Resource child = mock(Resource.class);
            when(child.adaptTo(ModifiableValueMap.class))
                    .thenReturn(new ModifiableValueMapDecorator(state));
            return child;
        });
        when(resolver.create(eq(guides), anyString(), anyMap())).thenAnswer(invocation -> {
            String name = invocation.getArgument(1);
            Map<String, Object> state = new HashMap<>(invocation.getArgument(2));
            children.put("/content/session-41-demo/guides/" + name, state);
            return mock(Resource.class);
        });

        Job job = mock(Job.class);
        when(job.getProperty("version", String.class)).thenReturn("v1");
        when(job.getRetryCount()).thenReturn(0, 1, 0);
        when(job.getId()).thenReturn("job-1");
        GuideBatchJobConsumer consumer = new GuideBatchJobConsumer();
        consumer.resolverFactory = factory;

        assertEquals(JobResult.FAILED, consumer.process(job));
        assertEquals(100, children.size());
        assertEquals(100, progressState.get("completed"));
        assertEquals("guide-0100", progressState.get("lastGuide"));

        assertEquals(JobResult.OK, consumer.process(job));
        assertEquals(300, children.size());
        assertEquals(300, progressState.get("completed"));
        assertEquals("guide-0300", progressState.get("lastGuide"));
        assertEquals("v1", children.get("/content/session-41-demo/guides/guide-0300")
                .get("processedVersion"));

        assertEquals(JobResult.OK, consumer.process(job));
        assertEquals(300, children.size());
        assertEquals(1, children.get("/content/session-41-demo/guides/guide-0001")
                .get("applyCount"));
        verify(resolver, times(12)).commit();
    }
}
