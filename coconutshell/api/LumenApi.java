import com.sun.net.httpserver.*;
import java.io.*;
import java.net.InetSocketAddress;

public class LumenApi {
    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(8080), 0);
        server.createContext("/status", new MyHandler("status"));
        server.createContext("/metrics", new MyHandler("metrics"));
        server.setExecutor(null);
        server.start();
        System.out.println("Lumen API: http://localhost:8080");
    }
    
    static class MyHandler implements HttpHandler {
        String type;
        MyHandler(String t) { type = t; }
        
        public void handle(HttpExchange t) throws IOException {
            String resp;
            if (type.equals("status")) {
                resp = "Status: alive, OS: Lumen";
            } else {
                resp = "CPU: 50%, MEM: 75%";
            }
            t.sendResponseHeaders(200, resp.length());
            OutputStream os = t.getResponseBody();
            os.write(resp.getBytes());
            os.close();
        }
    }
}