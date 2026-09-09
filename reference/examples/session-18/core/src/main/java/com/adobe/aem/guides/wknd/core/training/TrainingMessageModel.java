package com.adobe.aem.guides.wknd.core.training;

import org.apache.sling.api.resource.Resource;
import org.apache.sling.models.annotations.Model;
import org.apache.sling.models.annotations.injectorspecific.InjectionStrategy;
import org.apache.sling.models.annotations.injectorspecific.OSGiService;
import org.apache.sling.models.annotations.injectorspecific.ValueMapValue;

@Model(adaptables = Resource.class)
public class TrainingMessageModel {
    @OSGiService
    private TrainingMessage trainingMessage;

    @ValueMapValue(injectionStrategy = InjectionStrategy.OPTIONAL)
    private String title;

    public String getTitle() {
        return title == null || title.trim().isEmpty() ? "Weekend Guides" : title.trim();
    }

    public String getMessage() {
        return trainingMessage.getMessage();
    }
}
