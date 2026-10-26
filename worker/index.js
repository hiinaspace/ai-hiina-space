// ai.hiina.space edge: static assets plus Markdown content negotiation.
//
// - `Accept: text/markdown` on an HTML path serves the sibling `.md` file.
// - Every response gets `Vary: Accept` and a `Content-Signal` header; HTML
//   responses also get a `Link` header pointing at their Markdown version.
// - One JSON log line per request (path, user agent, Accept, Signature-Agent)
//   feeds Workers Logs for the agent-traffic measurement.

const CONTENT_SIGNAL = "search=yes, ai-input=yes, ai-train=yes";
const MARKDOWN_TYPE = "text/markdown; charset=utf-8";

function markdownPathFor(pathname) {
  if (pathname === "/" || pathname === "/index.html") return "/index.md";
  if (/\.[a-z0-9]+$/i.test(pathname) && !pathname.endsWith(".html")) return null;
  const stem = pathname.replace(/\/index\.html$/, "").replace(/\.html$/, "").replace(/\/+$/, "");
  return stem ? `${stem}.md` : "/index.md";
}

function wantsMarkdown(accept) {
  // Prefer Markdown only when it is asked for explicitly; `*/*` alone keeps HTML.
  return /(^|,)\s*text\/(markdown|x-markdown)\b/i.test(accept || "");
}

function decorate(resp, { pathname, mdPath }) {
  const out = new Response(resp.body, resp);
  const h = out.headers;
  h.append("Vary", "Accept");
  h.set("Content-Signal", CONTENT_SIGNAL);
  h.set("Access-Control-Allow-Origin", "*");
  if (pathname.endsWith(".md")) h.set("Content-Type", MARKDOWN_TYPE);
  const type = h.get("Content-Type") || "";
  if (type.startsWith("text/html") && mdPath) {
    h.set("Link", `<${mdPath}>; rel="alternate"; type="text/markdown"`);
  }
  return out;
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const accept = request.headers.get("Accept") || "";
    const mdPath = markdownPathFor(url.pathname);
    let served = "asset";
    let resp;

    if (mdPath && wantsMarkdown(accept)) {
      const mdUrl = new URL(mdPath, url);
      const mdResp = await env.ASSETS.fetch(new Request(mdUrl, request));
      if (mdResp.ok) {
        served = "negotiated-md";
        resp = decorate(mdResp, { pathname: mdPath, mdPath });
      }
    }
    if (!resp) {
      resp = decorate(await env.ASSETS.fetch(request), { pathname: url.pathname, mdPath });
    }

    console.log(
      JSON.stringify({
        path: url.pathname,
        status: resp.status,
        served,
        ua: request.headers.get("User-Agent") || "",
        accept,
        signatureAgent: request.headers.get("Signature-Agent") || "",
      }),
    );
    return resp;
  },
};
