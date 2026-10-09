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
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class GuideBatchJobConsumerTest {
    @Test
    void resumesAfterFirstBatchAndSkipsReplay() throws Exception {
        ResourceResolverFactory factory = mock(ResourceResolverFactory.class);
        ResourceResolver resolver = mock(ResourceResolver.class);
        Resource guideA = mock(Resource.class);
        Resource guideB = mock(Resource.class);
        Map<String, Object> stateA = new HashMap<>();
        Map<String, Object> stateB = new HashMap<>();
        ModifiableValueMap valuesA = new ModifiableValueMapDecorator(stateA);
        ModifiableValueMap valuesB = new ModifiableValueMapDecorator(stateB);
        when(factory.getServiceResourceResolver(anyMap())).thenReturn(resolver);
        when(resolver.getResource("/content/session-41-demo/guides/guide-a")).thenReturn(guideA);
        when(resolver.getResource("/content/session-41-demo/guides/guide-b")).thenReturn(guideB);
        when(guideA.adaptTo(ModifiableValueMap.class)).thenReturn(valuesA);
        when(guideB.adaptTo(ModifiableValueMap.class)).thenReturn(valuesB);

        Job job = mock(Job.class);
        when(job.getProperty("version", String.class)).thenReturn("v1");
        when(job.getRetryCount()).thenReturn(0, 1, 0);
        when(job.getId()).thenReturn("job-1");
        GuideBatchJobConsumer consumer = new GuideBatchJobConsumer();
        consumer.resolverFactory = factory;

        assertEquals(JobResult.FAILED, consumer.process(job));
        assertEquals(1, stateA.get("applyCount"));
        assertEquals(null, stateB.get("applyCount"));
        assertEquals(JobResult.OK, consumer.process(job));
        assertEquals(1, stateA.get("applyCount"));
        assertEquals(1, stateB.get("applyCount"));
        assertEquals(JobResult.OK, consumer.process(job));
        assertEquals(1, stateA.get("applyCount"));
        assertEquals(1, stateB.get("applyCount"));
        verify(resolver, times(2)).commit();
    }
}
