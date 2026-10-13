import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import java.io.IOException;
import java.net.InetSocketAddress;
import java.nio.charset.StandardCharsets;

public final class StubServer {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress("127.0.0.1", 8765), 0);
        server.createContext("/", StubServer::handle);
        server.start();
        System.out.println("Session 42 stub listening on http://127.0.0.1:8765");
    }

    private static void handle(HttpExchange exchange) throws IOException {
        String path = exchange.getRequestURI().getPath();
        try {
            int status;
            if (!"GET".equals(exchange.getRequestMethod())) {
                status = 405;
            } else if (!"training-demo-only".equals(exchange.getRequestHeaders().getFirst("X-API-Key"))) {
                status = 401;
            } else if ("/ok".equals(path) || "/slow".equals(path)) {
                status = 200;
            } else if ("/unavailable".equals(path)) {
                status = 503;
            } else {
                status = 404;
            }

            if ("/slow".equals(path) && status == 200) {
                try {
                    Thread.sleep(3000);
                } catch (InterruptedException e) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }

            byte[] body = ("status=" + status + "\n").getBytes(StandardCharsets.UTF_8);
            exchange.getResponseHeaders().set("Content-Type", "text/plain; charset=utf-8");
            System.out.printf("%s %s -> %d%n", exchange.getRequestMethod(), path, status);
            try {
                exchange.sendResponseHeaders(status, body.length);
                exchange.getResponseBody().write(body);
            } catch (IOException e) {
                if (!"/slow".equals(path)) {
                    throw e;
                }
                // The client intentionally closes /slow after its read timeout.
            }
        } finally {
            exchange.close();
        }
    }
}
