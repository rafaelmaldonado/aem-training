package com.adobe.aem.guides.wknd.core.training;

import io.wcm.testing.mock.aem.junit5.AemContext;
import io.wcm.testing.mock.aem.junit5.AemContextExtension;
import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.factory.ModelFactory;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;

import static org.junit.jupiter.api.Assertions.assertEquals;

@ExtendWith(AemContextExtension.class)
class TrainingMessageTest {
    private final AemContext context = new AemContext();

    @Test
    void rendersAuthoredTitleAndConfiguredServiceMessage() {
        context.registerInjectActivateService(new TrainingMessage(), "message", "  Local Author  ");
        context.addModelsForClasses(TrainingMessageModel.class);
        Resource resource = context.create().resource("/content/training/message", "title", "  My guide  ");

        TrainingMessageModel model = context.getService(ModelFactory.class)
                .createModel(resource, TrainingMessageModel.class);

        assertEquals("My guide", model.getTitle());
        assertEquals("Local Author", model.getMessage());
    }

    @Test
    void usesFallbackWhenTitleIsMissingAndConfigurationIsBlank() {
        context.registerInjectActivateService(new TrainingMessage(), "message", "   ");
        context.addModelsForClasses(TrainingMessageModel.class);
        Resource resource = context.create().resource("/content/training/message");

        TrainingMessageModel model = context.getService(ModelFactory.class)
                .createModel(resource, TrainingMessageModel.class);

        assertEquals("Weekend Guides", model.getTitle());
        assertEquals("Welcome to Weekend Guides", model.getMessage());
    }
}
