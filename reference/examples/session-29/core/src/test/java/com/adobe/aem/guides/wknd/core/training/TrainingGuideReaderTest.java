package com.adobe.aem.guides.wknd.core.training;

import org.apache.sling.api.resource.Resource;
import org.apache.sling.api.resource.ResourceResolver;
import org.apache.sling.api.resource.ResourceResolverFactory;
import org.apache.sling.api.resource.ValueMap;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.never;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

class TrainingGuideReaderTest {
    @Test
    void closesOnlyTheResolverItCreates() throws Exception {
        ResourceResolverFactory factory = mock(ResourceResolverFactory.class);
        ResourceResolver resolver = mock(ResourceResolver.class);
        Resource resource = mock(Resource.class);
        ValueMap values = mock(ValueMap.class);
        when(factory.getServiceResourceResolver(argThat(this::usesExpectedSubservice))).thenReturn(resolver);
        when(resolver.getResource("/content/training-permissions/guides")).thenReturn(resource);
        when(resource.getValueMap()).thenReturn(values);
        when(values.get("jcr:title", "guides")).thenReturn("Training guides");
        when(resource.getName()).thenReturn("guides");

        TrainingGuideReader reader = new TrainingGuideReader();
        reader.resolverFactory = factory;

        assertEquals("Training guides", reader.readWithService());
        verify(resolver).close();
    }

    @Test
    void leavesBorrowedResolverOpen() {
        ResourceResolver resolver = mock(ResourceResolver.class);
        Resource resource = mock(Resource.class);
        ValueMap values = mock(ValueMap.class);
        when(resolver.getResource("/content/training-permissions/guides")).thenReturn(resource);
        when(resource.getValueMap()).thenReturn(values);
        when(resource.getName()).thenReturn("guides");
        when(values.get("jcr:title", "guides")).thenReturn("guides");

        assertEquals("guides", new TrainingGuideReader().readWith(resolver));
        verify(resolver, never()).close();
    }

    private boolean usesExpectedSubservice(Map<String, Object> authInfo) {
        return "training-guide-read".equals(authInfo.get(ResourceResolverFactory.SUBSERVICE));
    }
}
