package com.adobe.aem.guides.wknd.core.training;

import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URI;
import java.net.URL;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.ConfigurationPolicy;
import org.osgi.service.component.annotations.Modified;
import org.osgi.service.metatype.annotations.AttributeDefinition;
import org.osgi.service.metatype.annotations.AttributeType;
import org.osgi.service.metatype.annotations.Designate;
import org.osgi.service.metatype.annotations.ObjectClassDefinition;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

@Component(service = ExternalStatusService.class, configurationPolicy = ConfigurationPolicy.REQUIRE)
@Designate(ocd = ExternalStatusService.Configuration.class)
public class ExternalStatusService {
    public enum Outcome { OK, RETRY, STOP }

    @ObjectClassDefinition(name = "Training: external status probe")
    public @interface Configuration {
        String endpoint() default "";
        @AttributeDefinition(name = "API key", type = AttributeType.PASSWORD)
        String apiKey() default "";
        int connectTimeoutMs() default 1000;
        int readTimeoutMs() default 2000;
    }

    private static final Logger LOG = LoggerFactory.getLogger(ExternalStatusService.class);
    private URL endpoint;
    private String apiKey;
    private int connectTimeoutMs;
    private int readTimeoutMs;

    @Activate
    @Modified
    protected void activate(Configuration config) {
        URI uri = URI.create(config.endpoint());
        boolean local = "http".equals(uri.getScheme())
                && ("localhost".equals(uri.getHost()) || "127.0.0.1".equals(uri.getHost()));
        if (!("https".equals(uri.getScheme()) || local) || uri.getHost() == null
                || uri.getUserInfo() != null || uri.getFragment() != null
                || config.apiKey().isEmpty() || config.connectTimeoutMs() <= 0
                || config.readTimeoutMs() <= 0) {
            throw new IllegalArgumentException("Configure a valid HTTPS endpoint (or local stub), key and positive timeouts");
        }
        try {
            endpoint = uri.toURL();
        } catch (IOException e) {
            throw new IllegalArgumentException("Invalid endpoint", e);
        }
        apiKey = config.apiKey();
        connectTimeoutMs = config.connectTimeoutMs();
        readTimeoutMs = config.readTimeoutMs();
    }

    public Outcome check() {
        HttpURLConnection connection = null;
        try {
            connection = (HttpURLConnection) endpoint.openConnection();
            connection.setConnectTimeout(connectTimeoutMs);
            connection.setReadTimeout(readTimeoutMs);
            connection.setInstanceFollowRedirects(false);
            connection.setRequestMethod("GET");
            connection.setRequestProperty("X-API-Key", apiKey);
            int status = connection.getResponseCode();
            Outcome outcome = status == 200 ? Outcome.OK
                    : status == 429 || status >= 500 ? Outcome.RETRY : Outcome.STOP;
            LOG.info("Session 42 upstreamStatus={} outcome={}", status, outcome);
            return outcome;
        } catch (IOException e) {
            LOG.warn("Session 42 transportFailure={} outcome=RETRY", e.getClass().getSimpleName());
            return Outcome.RETRY;
        } finally {
            if (connection != null) {
                connection.disconnect();
            }
        }
    }
}
