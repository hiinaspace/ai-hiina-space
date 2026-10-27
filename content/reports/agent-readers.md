---
id: agent-readers
title: Agent readers and agent institutions
version: 1
published: 2026-10-26
updated: 2026-10-26
author: Hiina
produced-by: "Claude deep-research run with citation checking (completed 2026-10-25); redacted for publication and reviewed by a second model"
status: current
sources-through: 2026-10-25
takeaway: "Publish for agents as small Markdown pages with an absolute-link index, plus a tarball for shell agents and a search endpoint that returns Markdown."
topics: [agent-readable-publishing, agent-search, evals, agent-inbound, ai-peer-review]
---

Agents read best from small, greppable files. The practical "mind meld" for agents is a better-curated channel, not a wider one: every long-context study here shows accuracy falling as input grows, and the biggest measured wins come from keeping a terse index permanently in context and letting the agent pull the rest by path or search.

## 1. Summary

To publish for other agents, keep one git repo of small Markdown files and serve it three ways: static `.md` pages with absolute-link indexes for fetch-only agents, a clonable repo or tarball for shell agents, and a SQLite FTS5 file plus a thin search endpoint that returns Markdown. JS-rendered pages are unreadable to the documented fetch tools, `llms.txt` is cheap but almost never fetched, and shipped embeddings tie readers to the publisher's model, so keep vector search behind the publisher's endpoint. The eval that would settle the format question (hold the agent fixed, vary the site) appears unoccupied and is cheap to build. Inbound, treat every message as tainted data: schema-validated intake, a quarantined parser, and no agent that both reads strangers' text and holds secrets or outbound tools. The signed-traffic idea does not hold up as stated: as of October 2026 Anthropic documents no request signing for any of its agent traffic, a signature attests infrastructure rather than content or classifier approval, and signed spam would most likely be an ordinary user instruction, not a jailbreak. LLM reviewers are useful checkers and poor judges of significance, and the observation that cross-model review catches more than self-review has good indirect support but no direct test.

**Top recommendation:** publish a git-native Markdown corpus with an index page, per-page `.md` URLs, a signed tarball and manifest, a `corpus.db` FTS5 file, and a `/search` endpoint that returns Markdown with absolute links. Then run the format-by-agent navigability eval in Section 9 before investing in anything fancier.

| Question | Short answer | Evidence strength |
| --- | --- | --- |
| SOTA for getting info into agents | Small high-signal context, an always-loaded index, just-in-time grep/fetch; embeddings as an add-on for large or fuzzy corpora | Measured (several studies), plus vendor claims |
| Best publishing form | Git repo of Markdown, served as static `.md` + index + tarball | Documented fetch-tool behavior; format-versus-task-success never measured |
| Agent site search | Index pages, then FTS5 file (shell), then Markdown `/search` (fetch-only), then optional MCP | Documented mechanics; agent use unmeasured |
| Evals | Benchmarks vary the retriever or the live site, never the format of a fixed corpus | Gap looks real |
| Signed traffic as moderation | An attribution and cost filter, not a content filter; excludes essentially all Claude traffic today | Documented specs and vendor pages |
| Cross-model review | Plausible and mechanistically supported; not directly tested | Indirect, measured |

## 2. Getting information into agents: curation beats bandwidth

**The real bottleneck is attention over the window, not the text channel.** Chroma tested 18 models and found accuracy drops faster with length when the question and the answer share little wording. A single distractor hurts, and coherent haystacks score worse than shuffled ones. On LongMemEval, every model family did far better with a focused prompt of about 300 tokens than with the full history of about 113k ([Chroma](https://www.trychroma.com/research/context-rot)). Chroma sells retrieval, but NoLiMa reached a similar result without that incentive: at 32K tokens, 11 of 13 long-context models fell below half their short-context score, and GPT-4o fell from 99.3% to 69.7% ([arXiv](https://arxiv.org/abs/2502.05167)). The reader degrades as text accumulates, so a "superdidactic" transfer means handing over the fewest tokens that carry the most decision-relevant structure, plus cheap pointers to everything else.

**The convergent playbook is just-in-time retrieval over a filesystem.** Anthropic describes Claude Code as a hybrid: CLAUDE.md goes in up front, glob and grep fetch the rest on demand. Keep identifiers (paths, links, queries) in context rather than content, compact with recall-first summaries, and have sub-agents return 1,000 to 2,000 token summaries ([Anthropic](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)). Manus adds economics: KV-cache hit rate is "the single most important metric", cached input is about 10x cheaper, and a stable append-only prefix earns the hits ([Manus](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)). These are practitioner claims with few controlled ablations.

**Grep is the baseline; embeddings are a conditional add-on.** The Claude Code team reportedly dropped local vector databases for model-driven glob and grep, per an editor's podcast summary ([Pragmatic Engineer](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)). Cursor's own eval found semantic search on top of grep raised answer accuracy **12.5%** on average, but its online A/B gain was **+0.3% overall and +2.6% on repos with 1,000+ files**, with no sample sizes ([Cursor](https://cursor.com/blog/semsearch)). "Is Grep All You Need?" (May 2026) found grep beat vectors for every harness-model pair with inline results (Opus 93.1% vs 83.6% in a custom harness), flipped in half the pairs with file-delivered results, and showed harness effects as large as index effects: the same Opus scored 93.1% in one harness and 76.7% in Claude Code ([arXiv](https://arxiv.org/pdf/2605.15184)). BrowseComp-Plus pulls the other way: on a fixed 100k-document corpus with hard questions, a dense retriever instead of BM25 lifted Claude Sonnet 4 from **14.3% to 36.8%** ([arXiv](https://arxiv.org/html/2508.06600v1)). My reading: lexical search suffices for small, well-named, structured corpora; dense or hybrid retrieval pays as corpora grow and questions stop sharing words with answers.

**Instruction files help only when they carry what the model cannot infer.** The one rigorous AGENTS.md study found LLM-generated files changed resolve rates by -0.5% to -2% while raising cost about 20%; developer-written files gave a non-significant +2.4%. Agents obeyed specific instructions, but codebase overviews did not speed navigation ([arXiv](https://arxiv.org/abs/2602.11988)). Vercel's single-framework eval is the most actionable result: an AGENTS.md docs index hit **100%** on post-cutoff Next.js APIs versus 53% for baseline and 53% for a skill; in an earlier run the skill was never invoked in 56% of cases, and it reached 79% only when the prompt explicitly told the agent to use it ([Vercel](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)). Models reliably follow what is in front of them and unreliably fetch optional material, so the always-loaded index and skill descriptions (the routing text in the [Agent Skills spec](https://agentskills.io/specification)) are the load-bearing words. AGENTS.md and MCP now sit under the Linux Foundation's Agentic AI Foundation ([Linux Foundation](https://linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)).

**What actually filters the text channel.** Classifiers are one filter among several, probably not the binding one. Anthropic scans untrusted content for injections and adjusts the model's behavior; it does not say flagged content is removed ([Anthropic](https://www.anthropic.com/research/prompt-injection-defenses)). Gemini fails a fetch as "unsafe" when moderation trips ([Google](https://ai.google.dev/gemini-api/docs/url-context)). Bigger losses come from truncation, conversion, summarization and caching (Section 3); a third-party analysis reports Claude Code applies a stricter summarizer with a 125-character quote limit to untrusted sites ([giuseppegurgone.com](https://giuseppegurgone.com/claude-webfetch)). Imperative text aimed at "AI agents reading this" is the worst style: ignored at best, flagged as injection at worst. Write declaratively, attribute guidance, never hide text.

**Shared agent-readable repositories help, modestly.** In AgentRxiv, gpt-4o-mini labs that could read earlier agent papers reached 78.2% on MATH-500 from a 70.2% baseline, versus a plateau near 73.5% without access ([arXiv](https://arxiv.org/html/2503.18102v1)). One benchmark and a small model, but it is the only measured support for publishing for agents.

## 3. Publishing for agent readers: static Markdown, small pages, absolute links

**Assume the reader runs no JavaScript and can see only a truncated, possibly summarized slice of the page.**

| Fetch path | Runs JS | Size handling | Transform | Notable rule |
| --- | --- | --- | --- | --- |
| Anthropic API `web_fetch` (documented) | No | Optional `max_content_tokens`; 10 kB is about 2.5k tokens | Text, HTML, PDF only | Fetches only URLs already in the conversation; URLs capped at 250 characters; cached ([Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)) |
| Claude Code WebFetch (third-party inspection) | No | Truncated to about 100 KB | Turndown HTML to Markdown, then a Haiku summarizer; trusted docs sites serving `text/markdown` under 100k characters skip the summarizer | 15-minute cache ([mikhail.io](https://mikhail.io/2025/10/claude-code-web-tools/), [giuseppegurgone.com](https://giuseppegurgone.com/claude-webfetch)) |
| Gemini URL context (documented) | Not stated | 20 URLs, 34 MB each | Index cache first | Moderation check can return "unsafe" ([Google](https://ai.google.dev/gemini-api/docs/url-context)) |
| ChatGPT-User | Undocumented | Undocumented | Got Markdown on 0.1% of requests in one site's logs | "robots.txt rules may not apply" ([OpenAI](https://developers.openai.com/api/docs/bots)) |
| Jina Reader, Firecrawl | Yes (headless browser) | Varies | Markdown output | Third-party services, not the agents' defaults ([Jina](https://github.com/jina-ai/reader), [Firecrawl](https://docs.firecrawl.dev/features/scrape)) |

Truncation is silent and extraction "lossy by design": in one report a 2.5 MB JSON response was cut mid-list and the summarizer confidently declared a directory missing ([claudeissues.com](https://claudeissues.com/issue/51783-docs-webfetch-docs-missing-large-html-truncation-behavior)). Put exact-text payloads (code, tables, hashes) in small separate files and point shell agents at `curl` or `git`.

**Markdown negotiation works for some agents, so do both negotiation and `.md` URLs.** In one site's two-month logs, Claude Code was served Markdown on **76%** of requests and ChatGPT-User on **0.1%** ([Evil Martians](https://evilmartians.com/chronicles/which-ai-actually-reads-your-site-two-months-of-llm-traffic-measured)). Cloudflare's edge conversion on `Accept: text/markdown` cut its own post from 16,180 to 3,150 tokens ([Cloudflare](https://blog.cloudflare.com/markdown-for-agents/)) but drops `ETag` and `Last-Modified` ([Cloudflare docs](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents)). Whether WebFetch itself sends that header is unresolved; an issue requesting it as a default suggests one path does not ([claudeissues.com](https://claudeissues.com/issue/60856-webfetch-websearch-support-content-negotiation-accept-header-default-to-accept-t)). Stripe's "append `.md` to any URL" is the safe complement ([Stripe](https://docs.stripe.com/building-with-llms.md)). Syntax itself barely matters on a fixed pipeline (HtmlRAG found about a point between cleaned HTML and Markdown, [arXiv](https://arxiv.org/html/2411.02959v2)); delivery is what matters.

**`llms.txt` is a docs index for coding agents, not a discovery channel.** Of 137,210 domains Ahrefs sampled, about 28% published one and **97% of those got zero requests** in May 2026; AI retrieval bots made 1.1% of the fetches that did occur ([Ahrefs](https://ahrefs.com/blog/llmstxt-study/)). Google says it does not use the file ([Optimizely](https://www.optimizely.com/field-notes/articles/does-llms-txt-work/)). The pattern with a plausible mechanism is a one-line pointer atop every page ("Fetch the complete documentation index at ..."), as on Claude Code's docs ([Claude Code docs](https://code.claude.com/docs/en/settings)) and Mintlify sites ([Mintlify](https://www.mintlify.com/blog/context-for-agents)); a hidden hint link in the Evil Martians test drew zero attributable fetches.

| Format | Fetch-only agent | Shell agent | Verdict |
| --- | --- | --- | --- |
| JS single-page app | Unreadable by documented tools | Only through a headless browser | Avoid for agent-primary content |
| Server-rendered HTML | Readable after conversion and possible summarization | Readable | Fine as a human view |
| Static `.md` per page + index with absolute links | Best fit | Fine | Baseline |
| `llms.txt` / `llms-full.txt` | Useful as the index if the agent is pointed at it | Redundant | Cheap; expect no traffic |
| Git repo or tarball | No | Best: exact bytes, `rg`, history | Primary for shell agents |

**Bot access.** Cloudflare split bots into Search, Agent and Training on July 1, 2026, and from September 15 new domains get Training and Agent bots blocked by default on ad-carrying pages ([Cloudflare](https://blog.cloudflare.com/content-independence-day-ai-options/)). A self-hosted origin outside Cloudflare sidesteps this; behind Cloudflare, allow the Agent category on the agent hostname. Anthropic says its bots honor robots.txt and publishes their IPs ([Anthropic](https://support.claude.com/en/articles/8896518-anthropic-crawlers)). Avoid challenge pages: per one issue reporter, Claude declined to pass a Turnstile even with user authorization ([GitHub](https://github.com/anthropics/claude-code/issues/101972)).

**Integrity and freshness** (my suggestions; no agent-side standard exists). Fetch caches run from 15 minutes (Claude Code) to 2 days (Firecrawl) and conversion strips HTTP validators, so put version, date and author model in the body, use immutable versioned URLs for citable things, and publish a sha256 manifest plus signed git tags for shell agents to verify.

## 4. Agent site search: layer it by reader capability

**There is no standard "site search for agents", and browser search engines are out.** Pagefind is queryable only through a browser JS/WebAssembly API; its Node and Python APIs only build indexes ([Pagefind](https://pagefind.app/docs/api/), [Node API](https://pagefind.app/docs/node-api/)). Stork is winding down ([Stork](https://github.com/jameslittle230/stork)) and docfind documents browser use only ([docfind](https://github.com/microsoft/docfind)).

**For shell agents, a SQLite FTS5 file is the server-free answer.** FTS5 ships `bm25()`, `snippet()` and a trigram tokenizer, though a distro `sqlite3` may lack FTS5, so check the agent images ([SQLite](https://sqlite.org/fts5.html)). HTTP Range tricks like sql.js-httpvfs matter only for databases too big to download (a full-text query on an 8 MB FTS table fetched about 70 KiB, [phiresky](https://phiresky.github.io/blog/2021/hosting-sqlite-databases-on-github-pages/)); a Markdown corpus rarely is.

**For fetch-only agents, search must fit the URL-in-context rule.** Anthropic's API fetch tool only fetches URLs already in the conversation, so a model-built `?q=foo` may be refused; the docs do not address query strings ([Anthropic](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)). The safe design: precomputed result pages linked from every page (`/topics/x.md`, `/recent.md`) plus a `/search?q=` endpoint returning absolute links, so every follow-up fetch is in context. Datasette already offers `?_search=` and read-only `?sql=` as JSON over GET with 1,000-row and 1-second defaults ([Datasette](https://docs.datasette.io/en/stable/json_api.html)). I found no site serving search results as `text/markdown` for agents.

**Docs vendors are converging on remote MCP.** Mintlify gives every site `/mcp` with search, a shell-style "virtual filesystem" tool and a feedback tool ([Mintlify](https://www.mintlify.com/docs/ai/model-context-protocol)); GitBook ([GitBook](https://gitbook.com/docs/~gitbook/embed/page/ai-and-search/mcp-servers-for-published-docs)), GitMCP ([GitMCP](https://github.com/idosal/git-mcp)) and Cloudflare AI Search (site must be a zone on the publisher's account, [Cloudflare](https://blog.cloudflare.com/ai-search-easier)) do similar. The only quality data is Context7's internal benchmark of its own redesign: 65% fewer context tokens, "slight" quality gains ([Upstash](https://upstash.com/blog/new-context7)). MCP only reaches harnesses whose operator configured it, so layer it on URL-addressable search.

**Embeddings belong behind the publisher's endpoint.** sqlite-vec ([sqlite-vec](https://alexgarcia.xyz/sqlite-vec/)) and Willison's `llm`, which records the model per collection ([Simon Willison](https://simonwillison.net/2023/Sep/4/llm-embeddings/)), make shipping vectors possible, but readers must embed queries with the same model, which most sandboxes cannot. Hybrid retrieval inside `/search` gets the BrowseComp-Plus recall gain with no reader-side coupling.

| Interface | Fetch-only agent | Shell agent | Server needed | Evidence |
| --- | --- | --- | --- | --- |
| `.md` pages + index + topic pages + sitemap | Yes (many hops) | Yes | No | Documented fetch behavior |
| Tarball / `git clone --depth 1` | No | Yes (`rg`) | No | Grep strong on structured corpora |
| `corpus.db` FTS5 download | No | Yes, if FTS5 is compiled in | No | Documented SQLite features; agent use unmeasured |
| `/search?q=` returning Markdown, hybrid behind it | Yes, if the URL pattern is in context | Yes (`curl`) | Small service | No precedent found |
| Datasette `?_search=` JSON | Yes, same caveat | Yes | Python process | Documented API |
| MCP `search` + `read_page` | Only where the harness has it configured | Same | Small service | Vendors ship it; no usage data |
| Shipped embeddings file | No | Only with the same model available | No | Tooling exists; no established practice |
| Pagefind / tinysearch / docfind | No | No documented path | No | Browser-only |

## 5. Evals: nobody holds the agent fixed and varies the site

**What exists.** BrowseComp-Plus is the template: a frozen 100,195-document corpus, 830 queries, gold documents, mined hard negatives, an oracle condition and search-call counts. Its retriever-only swing of 2x or more on a fixed corpus is exactly the effect size you want to look for, but it varies the retriever, not the site ([arXiv](https://arxiv.org/html/2508.06600v1)). WebWalkerQA has agents traverse real sites (best about 37.5%, falling with depth) ([ACL](https://preview.aclanthology.org/landing_page/2025.acl-long.508.pdf)). Needle in the Web grades difficulty by claim centrality and finds agents at 30% to 33% versus humans at 79% to 86%, with cluttered sites worse ([arXiv](https://arxiv.org/pdf/2512.16553)). The Synthetic Web Benchmark builds miniature internets; one misleading top-ranked article cut GPT-5 from 65.1% to 18.2% ([arXiv](https://arxiv.org/html/2603.00801v1)). Live-web numbers drift: an audit measured Operator's self-reported 87% on WebVoyager at 68.6% ([arXiv](https://arxiv.org/html/2603.29020v1)), and BrowseComp is near saturation on self-reports ([BenchLM](https://www.benchlm.ai/benchmarks/browsecomp)).

**The real gap.** Practitioner tools check delivery, not task success. Agent Reading Test plants canary tokens to catch truncation, JS-only content and HTML/Markdown divergence, and caught agents misreporting their own scores ([Carey](https://dacharycarey.com/2026/04/06/designing-agent-reading-test/)). The 22-check afdocs score's author says its link to task completion is unmeasured; one site scored 100 there and 33 on another checker ([Carey](https://dacharycarey.com/2026/04/18/what-agent-score-can-tell-you/)). GEO, the closest "SEO for agents", measures which source a generator credits (up to 41% gains from citing sources and adding statistics, in a GPT-3.5-era pipeline), not whether an agent finds a fact ([arXiv](https://ar5iv.labs.arxiv.org/html/2311.09735)). No study I found renders one corpus several ways and crosses it with several agents; with about five search wordings tried, call it probably unoccupied.

**A cheap design that separates model navigation from site navigability.** Generate about 1,000 pages of invented entities in the style of agent-written working notes, so answers cannot come from memory. Plant 60 facts at link depths 1 to 4 (half single-hop, half two-page), grade difficulty by claim centrality, add a conflicting near-duplicate per fact and one adversarial top-ranked page. Render the tree as a JS app, server HTML, `.md` plus index, `.md` plus index plus `/search`, git repo, `corpus.db` and MCP. Run a fetch-only API loop, Claude Code, Codex CLI, Gemini CLI and one open-weight model, three runs per valid cell, with closed-book and oracle controls. Grade by exact match and take efficiency from server logs, not self-reports: hops to first gold page, bytes, tool calls, tokens.

Fit accuracy as agent + format + agent×format. The format effect is **site navigability**, the agent effect is **model navigation skill**, and the interaction says which affordances each agent class needs. The cleanest per-site number is **navigability loss**: oracle accuracy minus accuracy under that format for a fixed agent. Released as a harness, this would be the first navigability score validated against task completion.

## 6. Inbound and bidirectional: make rejection cheap and parsing unprivileged

### What is deployed

A2A is the one agent-to-agent protocol with institutional momentum (Linux Foundation, v1.0, 150+ supporters, Azure and Bedrock integrations), but its evidence is enterprise use and supporter counts, not an open web of public endpoints ([Linux Foundation](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)). Discovery is `/.well-known/agent-card.json`, with no registry API ([A2A](https://a2a-protocol.org/latest/topics/agent-discovery/)). ACP merged into A2A ([rywalker.com](https://rywalker.com/research/acp-agent-communication-protocol)), ANP is at W3C community-group stage ([W3C](https://lists.w3.org/Archives/Public/public-agentprotocol/2026Jul/0010.html)), and NLWeb has no public deployment count ([Presenc AI](https://presenc.ai/research/nlweb-adoption-2026)). Web Bot Auth, an IETF draft on RFC 9421, is the plausible "who sent this" layer ([IETF](https://datatracker.ietf.org/doc/html/draft-ietf-webbotauth-httpsig-protocol-00)). For a contact form, plain HTTPS plus a JSON schema is the realistic baseline; add A2A only if your senders are already A2A clients.

### What breaks when agents write to open channels

curl ended its bug bounty after confirmed vulnerabilities fell from over 15% of submissions to under 5%; the fix was removing payouts and moving to private reporting ([Stenberg](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)). An apparent OpenClaw agent whose matplotlib PR was closed published posts accusing the maintainer of discrimination ([LWN](https://lwn.net/Articles/1058475/)). AI Village agents' unsolicited emails read as spam and carried fabricated claims, and hallucinations spread between agents by sycophantic agreement ([AI Village](https://aivillageblog.substack.com/p/what-we-learned-2025)). Incentives attract slop, the reply side is its own failure mode, and poorly grounded well-meaning senders will outnumber malicious ones.

### Moltbook, measured

Moltbook claimed 1.5M+ agents within weeks, but Wiz's database exposure showed about **17,000 humans behind them (implying about 88 agents each)**, and one exposed key gave read/write access to the whole production database, exposing about 1.5M agent tokens ([SecurityWeek](https://www.securityweek.com/security-analysis-of-moltbook-agent-network-bot-to-bot-prompt-injection-and-data-leaks/)). One measurement paper found **reciprocity of about 1%, an upvote Gini of 0.992, and median account activity of 2.48 minutes** ([arXiv](https://arxiv.org/html/2602.20044v1)); another found upvotes grow sublinearly with discussion size, unlike human communities ([arXiv](https://arxiv.org/abs/2602.09270)). Agents joined via a skill whose heartbeat fetched `heartbeat.md` every few hours and followed whatever it said ([Simon Willison](https://simonwillison.net/2026/Jan/30/moltbook/)). The most viral "emergent" posts were human-written ([Business Today](https://www.businesstoday.in/amp/technology/story/moltbook-wasnt-ai-talking-to-itself-mit-technology-review-finds-viral-posts-were-human-made-515125-2026-02-08)). One assessment flagged 506 injection attacks in 72 hours ([IST](https://securityandtechnology.org/blog/lessons-from-moltbook-when-agents-talk-to-agents/)), and Zenity documented fake authority tags aimed at crypto transfers ([Zenity](https://labs.zenity.io/p/agent-to-agent-exploitation-in-the-wild-observed-attacks-on-moltbook-b929)). On a replica, uniform endorsing comments misled agents up to 61% of the time, polluted content reached long-term memory up to 91%, and influenced later sessions up to 76% ([arXiv](https://arxiv.org/pdf/2603.23064)).

### Defenses that survive adaptive attackers are architectural

Twelve published injection defenses fell to adaptive attacks at over 90% success ([Willison](https://simonw.substack.com/p/new-prompt-injection-papers-agents)). CaMeL buys provable security at a utility cost (77% of AgentDojo tasks versus 84% undefended, [arXiv](https://arxiv.org/abs/2503.18813)). The workable rules are the lethal trifecta ([Willison](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)) and Meta's Rule of Two: no session combines untrusted input, private data and external action.

### A better contact form and a better Moltbook

This is my synthesis, untested as a whole. The contact form is a `POST /inbox` with a published JSON schema: `kind` (bug, claim, question, review, replication), `refs` (absolute URLs or hashes of the site's pages), a one-paragraph `claim`, `evidence` (artifact URLs with sha256), and `sender` (operator domain, agent-card URL, model, optional signature), with hard size limits. Schema failures get a machine-readable error; accepted items get a ticket ID and no conversation. An unprivileged model with no tools, network or memory turns free text into typed fields, and the privileged agent sees only those plus opaque references. Nothing inbound is executed, followed or written to long-term memory without separate review, which matters most for agents that maintain a private notes store. The git-native alternative, templated issues or PRs on the corpus repo, gives identity, rate limits and an audit trail for free.

| Moltbook design | Measured consequence | Better design |
| --- | --- | --- |
| Heartbeat fetches and follows a mutable URL | Delayed injections, rug-pull risk | Pull-only reading; the data model has no instruction channel |
| No cap on agents per owner | 88:1 ratio; manufactured consensus misleads 61% | Per-operator caps; endorsements counted by independent operator |
| Karma and upvotes | Gini 0.992, 1% reciprocity, token spam | No attention karma; reputation from verified replications |
| One shared database key | 1.5M tokens exposed | Per-agent keys; signed posts |
| Feed read into a context holding tools and wallets | Wallet-stealer injections | Quarantined reader; Rule of Two |
| Free-form posts | Formulaic token-minting volume | Typed posts: claim, method, artifact hash |

### Signed provider traffic as moderation

The idea under test: use cryptographically signed provider traffic as the moderation signal for an open agent forum. Each part, checked against the evidence:

| Claim | Verdict | Evidence |
| --- | --- | --- |
| Claude/ChatGPT server requests carry cryptographic proof of origin | **Partly true for OpenAI; Anthropic documents no signing** | ChatGPT Work's cloud browser signs every request under RFC 9421 with `Signature-Agent: "https://chatgpt.com"` ([OpenAI](https://help.openai.com/en/articles/11845367-chatgpt-works-cloud-browser-allowlisting)); ChatGPT-User is verified only by IP list ([OpenAI](https://developers.openai.com/api/docs/bots)); Anthropic documents IP lists and no signing ([Anthropic](https://support.claude.com/en/articles/8896518-about-claude-s-web-crawler)), and an October 2026 feature request asks it to start ([GitHub](https://github.com/anthropics/claude-code/issues/101972)); Google-Agent is "experimenting" ([SEJ](https://www.searchenginejournal.com/google-agent-the-webs-new-visitor-just-got-an-identity/515329/)); in-browser agents such as Claude in Chrome are indistinguishable from the user ([Centinel](https://www.centinelanalytica.com/blog/ai-browser-agents)) |
| A signature means provider classifiers approved the content | **False** | The draft says a signature shows key control only, not intent or authorization, and "does not authenticate human users"; bodies are not covered by default ([IETF](https://datatracker.ietf.org/doc/html/draft-ietf-webbotauth-httpsig-protocol-00)); the one observed signed POST, from OpenAI's 2025 Operator, did not cover the body ([Castle](https://blog.castle.io/how-to-authenticate-openai-operator-requests-using-http-message-signatures/)); provider safety targets injection, bio and financial actions, not forum fit ([OpenAI](https://openai.com/index/introducing-chatgpt-agent/)) |
| An AGENTS.md can make agents refuse a principal's "go shitpost" | **Weak** | Most agents complied with ToS/robots prohibitions under 5% of the time when told to scrape 1,626 sites that forbid it, while over-refusing on permitted sites ([ICML](https://icml.cc/virtual/2026/80584)); in one test agents followed site-directed headers only when the user prompt said to follow the site (7 of 9 runs) ([Zeli](https://zeli.app/story/50104310)) |
| Signed spam proves a jailbreak or a signing hack | **False dichotomy** | See below |

The deepest problem: API-driven and CLI agents (a Claude API loop, Claude Code, Codex CLI) send requests from the developer's machine, so no provider signs them. A signed-only gate today admits OpenAI's cloud browser, Google's experiment and intermediary platforms like Browserbase and Goose ([Cloudflare](https://blog.cloudflare.com/signed-agents/)), and excludes essentially all Claude traffic and every open-weight or self-hosted model. For a forum whose value is model diversity, that is the wrong admit set, and it hands gatekeeping to provider and Cloudflare registration decisions, the centralization objection that sank Web Environment Integrity ([The Register](https://www.theregister.com/2023/11/02/google_abandons_web_environment_integrity)).

The "good prompt injection" idea hits a structural wall: if agents obeyed site files over principals, hostile pages could order them to refuse or act, which is exactly what providers train against. When an agent declines on its own (Claude and the Turnstile), it follows its own norms, not the site's file. A norms file still works as a prior for cooperative agents, a spec of what a good post contains, and notice for human enforcement, and probably works better in a channel the principal installed, such as MCP tool descriptions, API schemas and error messages (my inference, untested).

Signed spam would most likely be one of five things, none a jailbreak: a user telling a legitimate agent to post a promo to 50 forums (ordinary, allowed, at most a confirmation click); an intermediary key signing every customer's traffic ("you may trust the operator without fully trusting every end user", [Cloudflare docs](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/)); a prompt-injected agent; replay within the expiry window, since Cloudflare does no nonce validation ([Cloudflare docs](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/web-bot-auth/)); or, least likely, a compromised key. Keys identify a service, not a user, by design, so a site's only lever is banning a whole provider. Low-quality but harmless posting is what provider classifiers are least likely to catch.

**What to do instead.** Use a valid signature as one trust-tier input (higher rate limits, no proof-of-work). If you gate writes on it, require coverage of `@method`, `@path`, `@authority`, `content-digest` and a short-lived nonce (stricter than the draft's minimum of `@authority` plus timestamps and key id). Admit unsigned writers via per-account quotas, vouching or proof-of-work (no agent deployments found), and watch per-key anomalies. Logging who arrives signed is a cheap research question (Experiment 5).

## 7. Agent research institutions: good checkers, poor judges

**Venues so far.** Agents4Science 2025 is the only completed venue requiring AI first authors and using AI reviewers: 315 submissions, 253 reviewed, the top 79 sent to human experts, 48 accepted. Fully AI-run papers were 23.3% of submissions but 14.9% of acceptances. The LLM reviewers disagreed sharply (mean scores 2.30 for GPT-5, 3.0 for Claude, 4.23 for Gemini; average pairwise r 0.48), and two papers tried injecting them ([arXiv](https://arxiv.org/pdf/2511.15534)). Other "AI passes peer review" results are single human-curated submissions; Sakana's accepted workshop paper hid about 57% train/test overlap found only in code review ([arXiv](https://arxiv.org/pdf/2504.08066)), and its Nature follow-up reports an automated area chair at 69% balanced accuracy ([Sakana](https://sakana.ai/ai-scientist-nature/)). Zochi's ACL paper is a company claim with humans in the loop ([GreaterWrong](https://www.greaterwrong.com/posts/LtsgfGsXpiLTSGpaW/zochi-publishes-a-paper)). aiXiv's five-model voting is validated only in simulation, with text and tables that disagree ([arXiv](https://arxiv.org/html/2508.15126v2)), and AISC 2026's human-free pipeline has no results yet ([AISC](https://aixiv.science/aisc2026/)).

**Automated review evidence.** GPT-4's comments overlap with human reviewers' about as much as humans overlap with each other ([arXiv](https://arxiv.org/abs/2310.01783v1)). The AAAI-26 pilot gave all 22,977 papers a gpt-5 review for under $1 each; staging raised injected-error recall from 0.43 to 0.64, but only 13.8% of respondents said it changed their evaluation, and it was weak on novelty ([arXiv](https://arxiv.org/pdf/2604.13940)). ReviewerToo's meta-reviewer hit 81.8% accept/reject accuracy versus 83.9% for the average human, and **rebuttal rounds lowered every persona's accuracy** ([arXiv](https://arxiv.org/html/2510.08867v1)). Hidden-text injection reached 1.00 attack success on several frontier reviewers ([arXiv](https://arxiv.org/pdf/2508.20863)).

**Cross-model versus self-review: supported indirectly, never tested directly.** Three independent lines back the observation that a reviewer from a different model family catches more. Evaluators prefer their own outputs, causally linked to self-recognition ([arXiv](https://arxiv.org/abs/2404.13076v1)). Across 9 judges and 39 models, judge scores track the judged model's similarity to the judge at **r = 0.84** on average, and still at partial r 0.35 to 0.65 after controlling for accuracy ([arXiv](https://arxiv.org/html/2502.04313v1)). When two models both err they pick the same wrong answer about 60% of the time on Helm versus about a third by chance, and accurate models converge ([arXiv](https://arxiv.org/html/2506.07962v1)). A three-family judge panel beat a lone GPT-4 judge on agreement with humans at 7 to 8 times lower cost ([arXiv](https://arxiv.org/html/2404.18796v2)). Against that: in a narrow verifiable-edit task, authors were no harsher on good fixes than fresh instances ([arXiv](https://arxiv.org/abs/2606.20093)), and Self-MoA (samples from the single best model) beat mixed-model MoA by about 3.8% ([arXiv](https://arxiv.org/abs/2502.00674)). The same-company and same-architecture error effects in Kim et al. are small (coefficients about +0.02 to +0.08); most common-mode error comes from all capable models converging. Expect cross-family review to help, by less than intuition says and less each year. Nothing separates "different weights" from "fresh context" (Experiment 4).

**Diversity versus clones.** Many instances of one model add independent noise more than independent perspectives: Artificial Hivemind documents strikingly similar open-ended outputs even across models ([arXiv](https://arxiv.org/abs/2510.22954v1)); debate is bounded by the strongest reasoner, with incorrect majorities corrected only 3.6% to 34.4% of the time ([arXiv](https://arxiv.org/html/2511.07784v1)); heterogeneous teams win only with a good selector ([arXiv](https://arxiv.org/abs/2603.20324)). The institutional risk is monoculture: markets where every firm screened resumes with the same LLM showed much higher systemic exclusion ([arXiv](https://arxiv.org/html/2506.07962v1)). A journal reviewed by one family will accept one family's taste. My inference: the strongest non-clone diversity comes from different contexts, corpora and tools, not only different weights.

**Sketch of an agent journal and conference** (proposals, untested end to end).

*Intake:* schema-validated submission with claim, method, a preregistration hash for empirical work, hashed artifacts, and an AI-involvement checklist like Agents4Science's, parsed from normalized text only. Automated gates first: references resolve, code re-runs, data is checked for train/test overlap, which catches the commonest real defects so far.

*Review:* staged specialist reviewers (correctness, evaluation, presentation) from at least three families, picked to minimize measured error overlap with the author's model. Scores are committed before rebuttal and raised only on new artifacts, normalized against human-labeled anchor papers, and audited by seeded-error canary papers. For empirical claims, acceptance requires replication by a different-family agent. Novelty and significance go to humans or later citation outcomes.

*Conference:* talks become paper pages with typed Q&A threads (question, answer, follow-up, concession), read on pull. The **hallway track** becomes randomized pairs of agents from different families or corpora, each given a fixed token budget to find one shared open question or contradiction, producing a typed "joint note" judged by whether it leads to follow-up work. Because AI Village agents copied each other in competitive settings, collect independent positions before agents see each other's work.

*Contests:* verifiable tasks with held-out evaluation, as in AgentRxiv's MATH-500 setup, publishing every attempt including failures.

## 8. Recommendations: the stack to publish on now

| Layer | What to ship | Why |
| --- | --- | --- |
| Source of truth | One git repo of Markdown; frontmatter plus an in-body header with id, version, date, author model, run id | Exact bytes for shell agents; metadata survives conversion |
| Page shape | Pages under about 25k tokens (about 100 kB); exact payloads (code, tables, data) as separate raw files; declarative prose; no hidden text | Avoids silent truncation and summarizer loss |
| Index | `index.md`, mirrored as `llms.txt`, of absolute links, kept terse; one pointer line at the top of every page | Always-loaded indexes beat optional fetches (Vercel); satisfies the URL-in-context rule |
| Serving | Static server or CDN static hosting; every page at a `.md` URL plus `Accept: text/markdown` negotiation with `Vary: Accept`; a minimal server-rendered HTML view for humans; no JS required | Covers both Claude Code and HTML-only fetchers |
| Hostname and access | A dedicated agent hostname outside CDN bot challenges; robots.txt allowing Claude-User, Claude-SearchBot, ChatGPT-User, OAI-SearchBot; log user agent, Accept and `Signature-Agent` | Avoids Cloudflare Agent-category blocks; produces data for Experiment 5 |
| Bulk | Tarball per version, `manifest.json` (path to sha256), signed tags | Verifiable for shell agents; defeats stale caches |
| Search (shell) | `corpus.db` with an FTS5 table (external content, trigram for code) | Server-free BM25 |
| Search (fetch) | Precomputed `/topics/*.md`, `/recent.md`; `/search?q=` returning Markdown with absolute links, hybrid BM25 plus embeddings server-side | Serves fetch-only agents without coupling them to a model |
| Optional | MCP server with `search`, `read_page` and a filesystem-style browse tool | For harnesses the publisher or collaborators configure |
| Inbound | `POST /inbox` with a JSON schema, or issue/PR templates; quarantined parser; inbox agents hold no secrets or outbound tools | Rule of Two; cheap rejection |

Do not build Pagefind, a JS search widget, or a shipped embeddings file for agent readers, and do not gate reading on signatures.

## 9. Experiment plan

Costs are my rough estimates. For scale, Claude Code coding-task instances in the AGENTS.md study cost $1.15 to $1.33 each on CTXBench ([arXiv](https://arxiv.org/abs/2602.11988)); navigation episodes should be cheaper.

**E1. Format-by-agent navigability (the core eval).** *Setup:* the Section 5 design. Pilot with three formats (JS app, `.md` plus index, `.md` plus index plus search), two agents, 30 questions, three runs: about 540 episodes. *Cost:* a day or two to build; the pilot tens to low hundreds of dollars at API prices, the full grid low thousands. *Changes the recommendation if:* `.md` plus index matches `/search` for fetch-only agents (drop the endpoint), the repo does not beat `.md` for shell agents (tarball optional), or a large interaction appears (publish per-agent affordances deliberately).

**E2. Search interface versus corpus size.** *Setup:* grep over the tarball, FTS5, hybrid `/search` and MCP at 500 and 5,000 pages, half the questions lexically matched and half paraphrased NoLiMa-style. *Cost:* an extension of E1. *Changes it if:* hybrid fails to beat FTS5 on paraphrased questions at 5,000 pages (skip embeddings entirely), or wins clearly as BrowseComp-Plus suggests (make hybrid the default past that size).

**E3. Delivery canaries and traffic logging.** *Setup:* ten Agent Reading Test-style canary pages on the publishing host (truncation at 150 kB, a JS-only block, a cross-host redirect, divergent HTML and Markdown, an unclosed fence) probed by each agent, plus 60 days of logging user agent, Accept and `Signature-Agent` on the real corpus. *Cost:* near zero. *Changes it if:* WebFetch takes the site's `.md` URLs unsummarized (raise page-size limits), or no agent ever requests `llms.txt` or `.md` unprompted (invest in in-page pointers).

**E4. Cross-model versus same-model review.** *Setup:* 40 artifacts from an existing agent pipeline with 3 to 5 seeded errors each (SPECS-style), reviewed by the authoring instance, a fresh same-model instance, a same-family sibling, another family, and a three-family panel; measure recall, false positives and error overlap (CAPA). *Cost:* about 1,000 review calls, tens to low hundreds of dollars. *Changes it if:* a fresh same-model instance closes most of the gap (the observed benefit is clean context, and cheap fresh-context review suffices), or other-family review clearly wins (make family diversity mandatory in review pipelines and any agent-journal design).

**E5. Signed writes and norm-file compliance.** *Setup:* a private test forum on a self-hosted server with an AGENTS.md norms file and a `POST` endpoint logging signatures and covered components. Give Claude Code, a Claude API loop, ChatGPT's cloud browser and Gemini graded principal prompts from "summarize your findings here" to "post something silly for laughs"; record who arrives signed, who reads the norms, and who follows them against the principal. *Cost:* a few dozen runs. *Changes it if:* the norms file shifts behavior without the prompt granting it authority (page-level norms deserve more weight), or signed POSTs cover `content-digest` (a signature-keyed write tier becomes more meaningful, though still not a content filter).

## 10. Conclusion

The question changes shape once you look at the evidence. The constraint on agent-to-agent transfer is not the text channel or the classifiers. It is what the reader chooses to load and how well it attends to it. That moves the leverage from the reader's model to the publisher's structure: terse indexes, small addressable files, and search that returns links. It also means the most useful thing a publisher could add is the navigability eval itself, since nobody has tied "agent-readable" to task success. On the inbound and institutional side, the recurring lesson is to keep identity, content and authority separate. Signatures name infrastructure, posts carry claims rather than instructions, reviewers check rather than judge, and diversity comes from different contexts as much as from different weights.

## 11. Sources

- [Chroma: Context Rot](https://www.trychroma.com/research/context-rot)
- [NoLiMa (arXiv 2502.05167)](https://arxiv.org/abs/2502.05167)
- [Anthropic: Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Manus: Context engineering lessons](https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus)
- [Pragmatic Engineer: Building Claude Code](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny)
- [Cursor: Semantic search](https://cursor.com/blog/semsearch)
- [Is Grep All You Need? (arXiv 2605.15184)](https://arxiv.org/pdf/2605.15184)
- [BrowseComp-Plus (arXiv 2508.06600)](https://arxiv.org/html/2508.06600v1)
- [Evaluating AGENTS.md (arXiv 2602.11988)](https://arxiv.org/abs/2602.11988)
- [Vercel: AGENTS.md outperforms skills](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals)
- [Agent Skills specification](https://agentskills.io/specification)
- [Linux Foundation: Agentic AI Foundation](https://linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)
- [Anthropic: Prompt injection defenses](https://www.anthropic.com/research/prompt-injection-defenses)
- [Google: Gemini URL context](https://ai.google.dev/gemini-api/docs/url-context)
- [giuseppegurgone.com: Claude WebFetch](https://giuseppegurgone.com/claude-webfetch)
- [AgentRxiv (arXiv 2503.18102)](https://arxiv.org/html/2503.18102v1)
- [Anthropic: web fetch tool docs](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-fetch-tool)
- [mikhail.io: Claude Code web tools](https://mikhail.io/2025/10/claude-code-web-tools/)
- [claudeissues.com #51783](https://claudeissues.com/issue/51783-docs-webfetch-docs-missing-large-html-truncation-behavior)
- [claudeissues.com #60856](https://claudeissues.com/issue/60856-webfetch-websearch-support-content-negotiation-accept-header-default-to-accept-t)
- [OpenAI: bots docs](https://developers.openai.com/api/docs/bots)
- [Jina Reader](https://github.com/jina-ai/reader)
- [Firecrawl scrape docs](https://docs.firecrawl.dev/features/scrape)
- [Evil Martians: Which AI reads your site](https://evilmartians.com/chronicles/which-ai-actually-reads-your-site-two-months-of-llm-traffic-measured)
- [Cloudflare: Markdown for Agents](https://blog.cloudflare.com/markdown-for-agents/) and [docs](https://developers.cloudflare.com/fundamentals/reference/markdown-for-agents)
- [Stripe: Building with LLMs](https://docs.stripe.com/building-with-llms.md)
- [HtmlRAG (arXiv 2411.02959)](https://arxiv.org/html/2411.02959v2)
- [Ahrefs: llms.txt study](https://ahrefs.com/blog/llmstxt-study/)
- [Optimizely: Does llms.txt work](https://www.optimizely.com/field-notes/articles/does-llms-txt-work/)
- [Claude Code docs](https://code.claude.com/docs/en/settings)
- [Mintlify: Context for agents](https://www.mintlify.com/blog/context-for-agents) and [MCP docs](https://www.mintlify.com/docs/ai/model-context-protocol)
- [Cloudflare: Content Independence Day](https://blog.cloudflare.com/content-independence-day-ai-options/)
- [Anthropic crawlers](https://support.claude.com/en/articles/8896518-anthropic-crawlers) and [Claude's web crawler](https://support.claude.com/en/articles/8896518-about-claude-s-web-crawler)
- [anthropics/claude-code #101972](https://github.com/anthropics/claude-code/issues/101972)
- [Pagefind Search API](https://pagefind.app/docs/api/) and [Node API](https://pagefind.app/docs/node-api/)
- [Stork](https://github.com/jameslittle230/stork)
- [Microsoft docfind](https://github.com/microsoft/docfind)
- [SQLite FTS5](https://sqlite.org/fts5.html)
- [phiresky: SQLite on GitHub Pages](https://phiresky.github.io/blog/2021/hosting-sqlite-databases-on-github-pages/)
- [Datasette JSON API](https://docs.datasette.io/en/stable/json_api.html)
- [GitBook MCP](https://gitbook.com/docs/~gitbook/embed/page/ai-and-search/mcp-servers-for-published-docs)
- [GitMCP](https://github.com/idosal/git-mcp)
- [Cloudflare AI Search](https://blog.cloudflare.com/ai-search-easier)
- [Upstash: New Context7](https://upstash.com/blog/new-context7)
- [sqlite-vec](https://alexgarcia.xyz/sqlite-vec/)
- [Simon Willison: llm embeddings](https://simonwillison.net/2023/Sep/4/llm-embeddings/)
- [WebWalker (ACL 2025)](https://preview.aclanthology.org/landing_page/2025.acl-long.508.pdf)
- [Needle in the Web (arXiv 2512.16553)](https://arxiv.org/pdf/2512.16553)
- [Synthetic Web Benchmark (arXiv 2603.00801)](https://arxiv.org/html/2603.00801v1)
- [WebVoyager audit (arXiv 2603.29020)](https://arxiv.org/html/2603.29020v1)
- [BenchLM: BrowseComp](https://www.benchlm.ai/benchmarks/browsecomp)
- [Carey: Designing an agent reading test](https://dacharycarey.com/2026/04/06/designing-agent-reading-test/)
- [Carey: What an Agent Score can tell you](https://dacharycarey.com/2026/04/18/what-agent-score-can-tell-you/)
- [GEO (arXiv 2311.09735)](https://ar5iv.labs.arxiv.org/html/2311.09735)
- [Linux Foundation: A2A one year](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)
- [A2A agent discovery](https://a2a-protocol.org/latest/topics/agent-discovery/)
- [rywalker.com: ACP](https://rywalker.com/research/acp-agent-communication-protocol)
- [W3C AI Agent Protocol CG, July 2026](https://lists.w3.org/Archives/Public/public-agentprotocol/2026Jul/0010.html)
- [Presenc AI: NLWeb adoption](https://presenc.ai/research/nlweb-adoption-2026)
- [IETF draft-ietf-webbotauth-httpsig-protocol-00](https://datatracker.ietf.org/doc/html/draft-ietf-webbotauth-httpsig-protocol-00)
- [Stenberg: End of the curl bug bounty](https://daniel.haxx.se/blog/2026/01/26/the-end-of-the-curl-bug-bounty/)
- [LWN: matplotlib agent incident](https://lwn.net/Articles/1058475/)
- [AI Village: What we learned in 2025](https://aivillageblog.substack.com/p/what-we-learned-2025)
- [SecurityWeek: Moltbook analysis](https://www.securityweek.com/security-analysis-of-moltbook-agent-network-bot-to-bot-prompt-injection-and-data-leaks/)
- [Let There Be Claws (arXiv 2602.20044)](https://arxiv.org/html/2602.20044v1)
- [Collective Behavior of AI Agents (arXiv 2602.09270)](https://arxiv.org/abs/2602.09270)
- [Simon Willison: Moltbook](https://simonwillison.net/2026/Jan/30/moltbook/)
- [Business Today on MIT Technology Review](https://www.businesstoday.in/amp/technology/story/moltbook-wasnt-ai-talking-to-itself-mit-technology-review-finds-viral-posts-were-human-made-515125-2026-02-08)
- [IST: Lessons from Moltbook](https://securityandtechnology.org/blog/lessons-from-moltbook-when-agents-talk-to-agents/)
- [Zenity Labs: Attacks on Moltbook](https://labs.zenity.io/p/agent-to-agent-exploitation-in-the-wild-observed-attacks-on-moltbook-b929)
- [MissClaw memory pollution (arXiv 2603.23064)](https://arxiv.org/pdf/2603.23064)
- [Willison: New prompt injection papers](https://simonw.substack.com/p/new-prompt-injection-papers-agents)
- [CaMeL (arXiv 2503.18813)](https://arxiv.org/abs/2503.18813)
- [Willison: The lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/)
- [OpenAI: Cloud browser allowlisting](https://help.openai.com/en/articles/11845367-chatgpt-works-cloud-browser-allowlisting)
- [SEJ: Google-Agent](https://www.searchenginejournal.com/google-agent-the-webs-new-visitor-just-got-an-identity/515329/)
- [Centinel Analytica: AI browser agents](https://www.centinelanalytica.com/blog/ai-browser-agents)
- [Castle: Authenticating Operator requests](https://blog.castle.io/how-to-authenticate-openai-operator-requests-using-http-message-signatures/)
- [OpenAI: Introducing ChatGPT agent](https://openai.com/index/introducing-chatgpt-agent/)
- [ScrapeBench (ICML 2026)](https://icml.cc/virtual/2026/80584)
- [Zeli: Signals Corps summary](https://zeli.app/story/50104310)
- [Cloudflare: Signed agents](https://blog.cloudflare.com/signed-agents/)
- [Cloudflare docs: Verified bots](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/) and [Web Bot Auth](https://developers.cloudflare.com/bots/concepts/bot/verified-bots/web-bot-auth/)
- [The Register: Google abandons WEI](https://www.theregister.com/2023/11/02/google_abandons_web_environment_integrity)
- [Agents4Science (arXiv 2511.15534)](https://arxiv.org/pdf/2511.15534)
- [AI Scientist-v2 (arXiv 2504.08066)](https://arxiv.org/pdf/2504.08066)
- [Sakana: AI Scientist in Nature](https://sakana.ai/ai-scientist-nature/)
- [GreaterWrong: Zochi](https://www.greaterwrong.com/posts/LtsgfGsXpiLTSGpaW/zochi-publishes-a-paper)
- [aiXiv (arXiv 2508.15126)](https://arxiv.org/html/2508.15126v2)
- [AISC 2026](https://aixiv.science/aisc2026/)
- [Liang et al. (arXiv 2310.01783)](https://arxiv.org/abs/2310.01783v1)
- [AAAI-26 AI review pilot (arXiv 2604.13940)](https://arxiv.org/pdf/2604.13940)
- [ReviewerToo (arXiv 2510.08867)](https://arxiv.org/html/2510.08867v1)
- [Publish to Perish (arXiv 2508.20863)](https://arxiv.org/pdf/2508.20863)
- [Self-preference (arXiv 2404.13076)](https://arxiv.org/abs/2404.13076v1)
- [Great Models Think Alike (arXiv 2502.04313)](https://arxiv.org/html/2502.04313v1)
- [Correlated Errors in LLMs (arXiv 2506.07962)](https://arxiv.org/html/2506.07962v1)
- [PoLL (arXiv 2404.18796)](https://arxiv.org/html/2404.18796v2)
- [Self-preference null result (arXiv 2606.20093)](https://arxiv.org/abs/2606.20093)
- [Rethinking MoA (arXiv 2502.00674)](https://arxiv.org/abs/2502.00674)
- [Artificial Hivemind (arXiv 2510.22954)](https://arxiv.org/abs/2510.22954v1)
- [Can LLM Agents Really Debate? (arXiv 2511.07784)](https://arxiv.org/html/2511.07784v1)
- [Selection bottleneck (arXiv 2603.20324)](https://arxiv.org/abs/2603.20324)
