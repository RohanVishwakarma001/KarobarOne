import http from "node:http";
import https from "node:https";

/**
 * The WHATWG Fetch spec forbids a body on GET/HEAD requests, so fetch() (browser
 * or Node) throws a TypeError before the request is even sent. Two backend routes
 * (`GET /shiprocket/serviceability`, `GET /shiprocket/couriers`) genuinely read a
 * JSON body on a GET, so they're unreachable via fetch from anywhere. A raw socket
 * request has no such restriction — use this from a Next.js Route Handler instead.
 */
export function httpGetWithBody<T>(url: string, body: unknown): Promise<{ status: number; data: T }> {
  return new Promise((resolve, reject) => {
    const target = new URL(url);
    const payload = Buffer.from(JSON.stringify(body));
    const client = target.protocol === "https:" ? https : http;

    const req = client.request(
      target,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          "Content-Length": payload.length,
        },
      },
      (res) => {
        const chunks: Buffer[] = [];
        res.on("data", (chunk) => chunks.push(chunk));
        res.on("end", () => {
          const text = Buffer.concat(chunks).toString("utf-8");
          try {
            resolve({ status: res.statusCode ?? 500, data: (text ? JSON.parse(text) : undefined) as T });
          } catch {
            reject(new Error("Invalid JSON response from backend"));
          }
        });
      }
    );
    req.on("error", reject);
    req.write(payload);
    req.end();
  });
}
