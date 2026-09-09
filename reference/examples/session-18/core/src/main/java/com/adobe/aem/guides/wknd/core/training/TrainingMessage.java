package com.adobe.aem.guides.wknd.core.training;

import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Modified;
import org.osgi.service.metatype.annotations.AttributeDefinition;
import org.osgi.service.metatype.annotations.Designate;
import org.osgi.service.metatype.annotations.ObjectClassDefinition;

@Component(service = TrainingMessage.class)
@Designate(ocd = TrainingMessage.Config.class)
public class TrainingMessage {
    @ObjectClassDefinition(name = "AEM Training - Message")
    public @interface Config {
        @AttributeDefinition(name = "Message")
        String message() default "Welcome to Weekend Guides";
    }

    private volatile String message;

    @Activate
    @Modified
    protected void activate(Config config) {
        String value = config.message();
        message = value == null || value.trim().isEmpty()
                ? "Welcome to Weekend Guides" : value.trim();
    }

    public String getMessage() {
        return message;
    }
}
