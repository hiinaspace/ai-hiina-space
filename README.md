# ai.hiina.space

Source for https://ai.hiina.space/, an agent-first corpus of research reports and
project status from Hiina (hiina@hiina.space). Agents should start at
https://ai.hiina.space/index.md, or clone this repo and read `content/`.

## Layout

- `content/reports/*.md`: reports, one Markdown file each, with frontmatter
  (`id`, `version`, `published`, `updated`, `produced-by`, `takeaway`, `topics`).
- `tools/build.py`: builds `dist/`: `.md` and no-JS HTML per page, versioned
  report copies, `index.md` (also served as `llms.txt`), `robots.txt`,
  `sitemap.xml`, `corpus.tar.gz` and `manifest.json` (sha256 of every file).
- `tools/publish_lint.py`: fail-closed check for private terms, stray emails,
  local paths, private IPs, page size, and commit identity. Its denylist is kept
  outside this repo; point `AIHS_DENYLIST` at it or place it at
  `lint/denylist.txt` (git-ignored).
- `worker/index.js`: Cloudflare Worker in front of the static assets. It serves
  the `.md` sibling for `Accept: text/markdown`, sets `Vary: Accept` and
  `Content-Signal`, and logs request metadata (path, user agent, Accept,
  Signature-Agent).

## Build and deploy

```
uv run tools/build.py --lint
npx wrangler deploy
```

## License

Text under `content/` is CC BY 4.0; code is MIT. See `LICENSE`.
