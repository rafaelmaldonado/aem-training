package com.adobe.aem.guides.wknd.core.training;

import com.sun.net.httpserver.HttpServer;
import java.net.InetSocketAddress;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

class ExternalStatusServiceTest {
    @Test
    void classifiesResponsesAndTimeout() throws Exception {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 0), 0);
        server.createContext("/ok", exchange -> {
            int status = "training-demo-only".equals(exchange.getRequestHeaders().getFirst("X-API-Key"))
                    ? 200 : 401;
            exchange.sendResponseHeaders(status, -1);
            exchange.close();
        });
        server.createContext("/unavailable", exchange -> {
            exchange.sendResponseHeaders(503, -1);
            exchange.close();
        });
        server.createContext("/slow", exchange -> {
            try {
                Thread.sleep(300);
                exchange.sendResponseHeaders(200, -1);
            } catch (InterruptedException ignored) {
                Thread.currentThread().interrupt();
            } finally {
                exchange.close();
            }
        });
        server.start();
        try {
            String base = "http://127.0.0.1:" + server.getAddress().getPort();
            ExternalStatusService service = new ExternalStatusService();
            service.activate(config(base + "/ok", "training-demo-only", 100));
            assertEquals(ExternalStatusService.Outcome.OK, service.check());
            service.activate(config(base + "/ok", "wrong", 100));
            assertEquals(ExternalStatusService.Outcome.STOP, service.check());
            service.activate(config(base + "/unavailable", "training-demo-only", 100));
            assertEquals(ExternalStatusService.Outcome.RETRY, service.check());
            service.activate(config(base + "/slow", "training-demo-only", 50));
            assertEquals(ExternalStatusService.Outcome.RETRY, service.check());
            assertThrows(IllegalArgumentException.class,
                    () -> service.activate(config("http://example.com/ok", "training-demo-only", 100)));
        } finally {
            server.stop(0);
        }
    }

    private static ExternalStatusService.Configuration config(String endpoint, String key, int readTimeout) {
        ExternalStatusService.Configuration config = mock(ExternalStatusService.Configuration.class);
        when(config.endpoint()).thenReturn(endpoint);
        when(config.apiKey()).thenReturn(key);
        when(config.connectTimeoutMs()).thenReturn(1000);
        when(config.readTimeoutMs()).thenReturn(readTimeout);
        return config;
    }
}
