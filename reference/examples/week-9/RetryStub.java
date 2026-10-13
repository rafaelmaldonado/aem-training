import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;

public final class RetryStub {
    private static final Map<String, Integer> ATTEMPTS = new ConcurrentHashMap<>();

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 8766), 0);
        server.createContext("/", exchange -> {
            String path = exchange.getRequestURI().getPath();
            int attempt = 0;
            int status;
            try {
                if (!"POST".equals(exchange.getRequestMethod())) {
                    status = 405;
                } else if (!path.startsWith("/guide-") || path.length() == 7) {
                    status = 404;
                } else {
                    attempt = ATTEMPTS.merge(path, 1, Integer::sum);
                    status = attempt == 1 ? 503 : 200;
                }
                exchange.sendResponseHeaders(status, -1);
                System.out.printf("%s %s attempt=%d -> %d%n",
                        exchange.getRequestMethod(), path, attempt, status);
            } finally {
                exchange.close();
            }
        });
        server.start();
        System.out.println("Week 9 retry stub listening on http://127.0.0.1:8766");
    }
}
