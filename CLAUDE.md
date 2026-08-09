# Agent Instructions — oldschool-engineer.dev

Instructions for AI agents assisting with Tom Pounders' personal brand site.

---

## 1. Identity and Mission

**Site:** https://oldschool-engineer.dev
**Owner:** Tom Pounders

Tom is a Principal Engineer (Principal IAM Software Engineer) at ServiceNow. He has three decades of experience: roughly two decades of civilian enterprise engineering at **Amazon/AWS** and **Microsoft**, plus a decade of **U.S. Navy Signals Intelligence** before that. He left Amazon as a Senior Software Development Engineer in March 2025, took a career break (active trading, built Kuhl Haus MDP), and joined ServiceNow in June 2026.

This repository is Tom's personal brand "front door." It contains:
- The **canonical source** for all his technical writing (blog posts)
- His **GitHub profile page** (README.md)
- Links to every profile he actively maintains

The site must maintain **search dominance** for the query **"tom pounders engineer"**.

### Voice Split — Read This Before Writing Anything

This site (blog, GitHub profile, Medium) and LinkedIn are **deliberately different voices**. Do not homogenize them.

- **LinkedIn** is Tom's professional record: exact HR title (Principal IAM Software Engineer), "Principal Engineer" brand framing, employer-forward. Maintained by Tom directly.
- **This site + GitHub profile + Medium** are Tom's personal notebook: old-school engineer, geek with credentials, employer-aware but not employer-first. **Never** introduce "organizational leader," "engineering leadership," hiring/recruiter-facing pitches, or job-seeking CTAs here — that framing was retired and belongs on LinkedIn only, if anywhere.

If a task asks you to make this site sound more like a resume or a LinkedIn headline, stop and ask Tom first — that's very likely the wrong direction.

### Brand Name Rules

| Context | Form | Example |
|---------|------|---------|
| Domain/URL | `oldschool-engineer` | `oldschool-engineer.dev` |
| Proper noun | Oldschool Engineer | "I'm the Oldschool Engineer" |
| Casual adjective | old school | "old school approach" |
| **Never in branding** | ~~old-school~~ | Merriam-Webster says this, but DNS says no |

The name was given to Tom by his team at AWS EC2 when they discovered he runs a 13-node Proxmox cluster and builds certified 10Gbps ethernet cables from raw spools of CAT6A.

### Agent Responsibilities

1. **Code maintenance** — Jekyll config, theme customization, builds, dependencies
2. **Content editing** — Formatting, proofreading, cross-references, images, Medium import cleanup
3. **Content creation** — Drafting posts, excerpts, SEO-optimized front matter
4. **Brand strategy** — SEO, search dominance, profile consistency, link management
5. **Platform strategy** — Advise when Jekyll/GitHub Pages limitations are reached

---

## 2. Repository Architecture

```
_config.yml                  # Jekyll config: theme, author, defaults, plugins
README.md                    # GitHub profile page (NO front matter — renders on GitHub)
CNAME                        # Custom domain: oldschool-engineer.dev
Gemfile                      # github-pages gem, jekyll-remote-theme, jekyll-include-cache
docker-compose.yml           # Local dev: ruby:3.2, jekyll serve, ports 4000 + 35729
robots.txt                   # Allow all crawlers, sitemap ref (has front matter for Jekyll)
blog.md                      # Blog listing page (layout: home)
404.md                       # Custom 404 (permalink: /404.html)
categories.md                # Auto-generated category index (permalink: /categories/)
tags.md                      # Auto-generated tag index (permalink: /tags/)
_data/navigation.yml         # Main nav: Home, Blog, Categories, Tags, Medium, GitHub
_includes/head/custom.html   # Favicon, GoatCounter analytics, Mermaid.js (dark theme)
_posts/                      # Blog posts (Markdown)
assets/images/posts/{slug}/  # Post images: img-NN.ext + optional manifest.json
convert_medium.py            # One-time Medium HTML-to-Jekyll converter (utility)
download_images.py           # One-time Medium CDN image downloader (utility)
```

### Key Configuration

- **Theme:** `remote_theme: mmistakes/minimal-mistakes` (Minimal Mistakes), skin: `dark`
- **Search:** Lunr.js client-side (`search: true`, `search_full_content: true`)
- **Analytics:** GoatCounter at `oldschool-engineer.goatcounter.com` (privacy-first, no cookies)
- **Diagrams:** Mermaid.js via CDN, dark theme, auto-converts `language-mermaid` code blocks
- **Feed:** Atom/RSS at `/feed.xml` via jekyll-feed
- **Sitemap:** Auto-generated at `/sitemap.xml` via jekyll-sitemap
- **SEO:** Meta tags, canonical URLs, Open Graph via jekyll-seo-tag
- **Plugins:** jekyll-remote-theme, jekyll-include-cache, jekyll-feed, jekyll-sitemap, jekyll-seo-tag

### Front Matter Defaults (from _config.yml)

All pages get: `layout: single`, `author_profile: true`, `toc: true`, `toc_sticky: true`

Posts additionally get: `read_time: true`, `share: true`, `related: true`

README.md specifically gets: `title: " "` (blank space — prevents layout issues on GitHub)

**Do not add these values to individual post front matter** unless intentionally overriding.

---

## 3. Writing Voice and Style

Tom's writing voice is the single most important thing to get right. Content that doesn't sound like Tom is worse than no content at all.

### Characteristics

- **Direct and conversational.** First person. Talks to the reader like a colleague at a whiteboard.
- **Irreverent when it fits.** Strategic profanity, self-deprecation, dry humor. Never forced.
- **Transparent about mistakes.** "Part 2 bombed. The engagement numbers don't lie."
- **Technical without talking down.** Assumes smart readers. Explains complex systems accessibly.
- **Short punchy sentences for emphasis.** "Not 15 minutes ago." / "Too. Damn. Slow."
- **No filler.** Every sentence carries weight. Cut anything that doesn't.
- **Forward-looking closings.** Series posts end with a "What's Next" section teasing the next topic.
- **Addresses the reader directly.** "If you made it this far, you're either deploying this thing or you're a masochist."

### DO

- Write like explaining something at a whiteboard to a smart colleague
- Use first person ("I", "my", "we" when including the reader)
- Include real numbers, real tool names, real links
- Admit when something is a guess or untested
- Use `**bold**` for emphasis on key technical insights
- Use humor when it lands naturally

### DON'T

- Use AI filler phrases ("In today's fast-paced world...", "Let's dive in!", "Without further ado", "In this article, we will...")
- Use corporate buzzwords without substance
- Over-qualify statements to sound safe ("It could potentially perhaps be considered...")
- Write in passive voice when active is clearer
- Use emojis in post body text (emojis appear only in series nav blocks and README badges)
- Call Tom a "thought leader", "influencer", or "content creator"
- Use "engineering leadership," "organizational leader," or any hiring/recruiter-facing pitch — that's LinkedIn's job, not this site's (see Section 1, Voice Split)
- Add superlatives that Tom wouldn't use ("amazing", "incredible", "game-changing")
- Use the word "journey" to describe career or project progression

---

## 4. Post Formatting Rules

### Heading Hierarchy

The Table of Contents (ToC) sidebar is generated from headings. The **first heading in a post sets the ToC baseline level**. All subsequent headings at that level or below appear in the ToC. Headings above the baseline are excluded.

| Level | Usage | Example |
|-------|-------|---------|
| `###` (h3) | Main section headings | `### The Stampeding Herd Problem` |
| `####` (h4) | Subsections within an h3 | `#### Prerequisites` |
| `##` (h2) | **Do not use** in posts | — |
| `#` (h1) | **Do not use** in posts | — |

**Critical rule:** The first heading in a post MUST be `###` (h3). If the first heading is `####` (h4), the ToC will only show h4 headings and exclude all h3 headings.

### Opening Subtitles

Some posts have a one-line subtitle immediately after the front matter. This MUST be styled text, not a heading:

```markdown
---
title: "Post Title"
...
---

***This is a subtitle rendered as bold italic text***
```

Using `####` for a subtitle poisons the ToC by setting h4 as the baseline. Use `***bold italic***` instead — it renders visually but creates no ToC entry.

### Code Blocks

Use triple-backtick fenced blocks with the correct language identifier:

````
```python
def example():
    pass
```
````

Use appropriate identifiers: `python`, `bash`, `yaml`, `json`, `html`, `css`, `javascript`, `go`, `ruby`.

**Note:** Some imported Medium posts use `python` as the language tag for non-Python content (bash, YAML, etc.). This is a legacy artifact. New posts should use the correct identifier.

### Image Captions

```markdown
![](/assets/images/posts/{post-slug}/img-01.png)

*Caption text in italics on the next line*
```

### Unicode — CRITICAL

Posts must contain only ASCII spaces (U+0020). Two specific Unicode characters are forbidden:

| Character | Code Point | Source |
|-----------|-----------|--------|
| Non-breaking space | U+00A0 | Medium HTML import artifact |
| Hair space | U+200A | Medium HTML import artifact |

When editing imported posts, scan for and replace these with regular spaces. Do **not** collapse double spaces when replacing — indentation in code blocks and YAML front matter must be preserved.

### Markdown Line Breaks

Use trailing double-space (`  `) at the end of lines that need soft line breaks within a block. This is used in series navigation blocks where each list item ends with two spaces before the newline.

---

## 5. Front Matter Specification

### Template

```yaml
---
title: "Post Title Here"
excerpt: "One sentence summary for meta description and blog listing."
categories:
  - Category Name
tags:
  - tag-name
  - another-tag
---
```

### Field Rules

| Field | Required | Notes |
|-------|----------|-------|
| `title` | Yes | Quoted string. Title case. Em dashes: ` — ` (with spaces). |
| `excerpt` | Yes | Quoted string. One sentence. Used for `<meta description>` and blog listing previews. Include relevant keywords naturally. |
| `categories` | Yes | YAML list. **One category per post.** |
| `tags` | Yes | YAML list. Lowercase, hyphenated. Prefer existing tags. |
| `canonical_url` | Rare | Only set when the canonical source is NOT this site. jekyll-seo-tag generates canonical URLs automatically. |

### Post Filename Convention

```
_posts/YYYY-MM-DD-title-words-separated-by-hyphens.md
```

For series posts, append `-part-N`: e.g., `...-part-2.md`, `...-part-3.md`.

### Categories (pick one)

| Category | Use For |
|----------|---------|
| Side Projects | Fun builds, dad jokes site, stock scanner features |
| Infrastructure | Deployment, Kubernetes, networking, TLS, cost optimization |
| Software Engineering | Code architecture, patterns, performance, testing |
| AI | AI/LLM tools, chatbots, prompt engineering |
| Meta | Blog meta-posts, site updates, personal/career |
| Home Lab | Proxmox cluster, home network, hardware |

### Tags (existing — prefer these before creating new ones)

`ai`, `ansible`, `asyncio`, `automation`, `aws`, `bedrock`, `brainfuck`, `budget`, `caching`, `career`, `certbot`, `chatbot`, `cost-optimization`, `dad-jokes`, `deployment`, `docker`, `documentation`, `fastapi`, `github-pages`, `home-lab`, `hybrid-cloud`, `infrastructure`, `javascript`, `kubernetes`, `kuhl-haus-mdp`, `langflow`, `litellm`, `llm`, `market-data`, `mattermost`, `navy`, `networking`, `observability`, `open-source`, `opentelemetry`, `performance`, `personal`, `prompt-engineering`, `proxmox`, `python`, `rabbitmq`, `redis`, `route53`, `site-updates`, `testing`, `tls`, `vibe-coding`, `vue`

---

## 6. Image Handling

### Directory Structure

```
assets/images/posts/{post-slug}/
  img-01.png
  img-02.jpeg
  img-03.png
  manifest.json    ← only for Medium imports, not needed for new posts
```

`{post-slug}` = filename without date prefix and `.md` extension.

### Rules

- Number images sequentially: `img-01`, `img-02`, etc. (zero-padded to two digits)
- Use the original file format (`.png`, `.jpeg`, `.jpg`, `.gif`)
- Reference with absolute paths from site root:

```markdown
![](/assets/images/posts/my-post-slug/img-01.png)
```

- **Do not** use relative paths
- **Do not** use `{{ site.url }}` in image paths
- **Do not** reference external image CDNs (Medium, Unsplash, etc.) — all images must be local

### manifest.json

Present only in directories for posts imported from Medium. Maps original CDN filenames to local filenames. New posts do not need this file.

---

## 7. Series Navigation Blocks

Multi-part series use a consistent navigation block. It appears after the opening subtitle (if any) or directly after the front matter.

### Template

```markdown
📖 **Series Name:**
- [Part 1: Short Title]({% post_url YYYY-MM-DD-slug %})
- [Part 2: Short Title]({% post_url YYYY-MM-DD-slug %})
- Part 3: Short Title (you are here)
- [Part 4: Short Title]({% post_url YYYY-MM-DD-slug %})
```

### Rules

- Starts with 📖 emoji and bold series name
- Each line (except the last) ends with **two trailing spaces** for markdown line breaks
- The current post is **plain text** (no link) with `(you are here)` marker
- All other posts are linked using `{% post_url %}` Liquid tags
- `{% post_url %}` takes the filename **without** the `.md` extension

### When Adding to a Series

Update **all** posts in the series to include the new entry in their navigation blocks. Ensure each post's `(you are here)` marker is on its own entry.

---

## 8. Cross-References and Links

### Internal Post Links

Always use Jekyll's `{% post_url %}` tag:

```markdown
[Part 2]({% post_url 2026-01-21-what-i-built-after-quitting-amazon-spoiler-its-a-stock-scanner-part-2 %})
```

**Do not** hardcode URLs for internal post links. `{% post_url %}` is verified at build time — broken references cause build failures, which is a safety net.

### Tag and Category Links

Link to tag pages using the `/tags/#tag-name` format:

```markdown
[home lab posts](/tags/#home-lab)
```

### External Links

Use inline markdown links. Tom frequently links to:
- GitHub repos and specific files/issues/commits in the kuhl-haus org
- Official documentation (ReadTheDocs, vendor docs)
- Pricing pages when discussing cost tradeoffs

---

## 9. Content Creation Workflow

1. **Choose filename:** `_posts/YYYY-MM-DD-title-slug.md`
2. **Write front matter:** Follow Section 5 exactly
3. **Add opening subtitle** (optional): `***Bold italic one-liner***`
4. **Add series nav block** (if applicable): Follow Section 7 template
5. **Write content:** Follow voice (Section 3) and formatting (Section 4) rules
6. **Add images:** Create `assets/images/posts/{slug}/` directory, name images `img-01`, `img-02`, etc.
7. **Add cross-references:** Use `{% post_url %}` for all internal links
8. **Update series posts:** If this post is part of a series, add its link to all sibling posts
9. **Verify locally:** Run `docker compose up` and check `http://localhost:4000`
10. **Check for issues:**
    - Scan for Unicode artifacts (U+00A0, U+200A)
    - Verify first heading is `###` (h3)
    - Verify ToC renders correctly
    - Verify all images load
    - Verify all `{% post_url %}` links resolve (build will fail if they don't)

---

## 10. Content Editing Checklist

- [ ] No non-breaking spaces (U+00A0) or hair spaces (U+200A)
- [ ] All internal links use `{% post_url %}` — not hardcoded URLs
- [ ] Image paths are absolute from site root (`/assets/images/posts/...`)
- [ ] All images are stored locally — no external CDN references
- [ ] First heading is `###` (h3), not `####` (h4)
- [ ] Opening subtitles use `***bold italic***` — not `####` headings
- [ ] Headings: `###` for main sections, `####` for subsections only
- [ ] Series nav blocks: trailing double-spaces, `(you are here)` on current post
- [ ] Code blocks use fenced syntax with correct language identifier
- [ ] Front matter has `title`, `excerpt`, `categories`, `tags`
- [ ] Image captions are in italics on the line immediately after the image
- [ ] No broken external links

---

## 11. Code Maintenance

### Theme

- Remote theme: `mmistakes/minimal-mistakes` (no version pin — always latest)
- Skin: `dark` — do not change without explicit approval
- Only customization: `_includes/head/custom.html` (favicon, GoatCounter, Mermaid.js)
- No other theme overrides exist

### Dependencies

- `Gemfile` uses the `github-pages` group gem (ensures GitHub Pages compatibility)
- Added gems: `jekyll-remote-theme`, `jekyll-include-cache`
- **Do not** add gems unsupported by GitHub Pages unless migrating away from it

### Local Development

```bash
docker compose up
# Site:       http://localhost:8001
# LiveReload: port 35729
```

Uses Ruby 3.2, `bundle install && bundle exec jekyll serve --host 0.0.0.0 --force_polling --livereload`.

### Build and Deployment

- GitHub Pages builds automatically on push to `main`
- Custom domain: `oldschool-engineer.dev` (CNAME file)
- DNS must remain pointed to GitHub Pages servers

### Files to Handle With Care

| File | Why |
|------|-----|
| `_config.yml` | Changes affect the entire site. Test locally first. |
| `CNAME` | Changing this breaks the custom domain. |
| `README.md` | Dual-purpose: GitHub profile AND Jekyll homepage. MUST NOT have front matter. |
| `robots.txt` | Has empty front matter delimiters (`---`/`---`) so Jekyll processes Liquid. Do not remove them. |

### Utility Scripts

These are one-time tools, not part of the site:

| Script | Purpose |
|--------|---------|
| `convert_medium.py` | Converts Medium HTML exports to Jekyll markdown. Run only when importing new Medium posts. |
| `download_images.py` | Downloads Medium CDN images locally. Idempotent — uses `manifest.json` to track downloads. |

---

## 12. SEO and Brand Strategy

### Primary Objective

Dominate search results for **"tom pounders engineer"**.

### SEO Infrastructure (already in place)

| Component | What It Does |
|-----------|-------------|
| jekyll-seo-tag | Generates `<title>`, `<meta description>`, `<link rel="canonical">`, Open Graph, Twitter cards |
| jekyll-sitemap | Generates `sitemap.xml` at `/sitemap.xml` |
| jekyll-feed | Generates Atom/RSS feed at `/feed.xml` |
| robots.txt | Allows all crawlers, references sitemap |
| GoatCounter | Privacy-first analytics (no cookies, GDPR-compliant) |

### Content SEO Guidelines

- **Excerpts are meta descriptions.** Write them for both humans and search engines — include relevant keywords naturally.
- **Titles should be specific.** Tom's titles are great examples: descriptive, intriguing, sometimes with a parenthetical punchline.
- **Use existing tags** for consistency. They drive the tag pages which are themselves indexed.
- **Cross-link between posts.** Internal linking strengthens site structure for crawlers.
- **Link back to earlier posts** when writing about topics Tom has covered before.

### Brand Signals to Reinforce

When creating content, naturally reinforce these differentiators:

- Three decades of experience: U.S. Navy Signals Intelligence, then Microsoft, Amazon/AWS, and now ServiceNow
- Hands-on experience building and operating Internet systems at planetary scale
- Home lab: 13-node Proxmox cluster, 42U rack, triple-redundant Internet
- Open source: kuhl-haus organization, MIT license, real CI/CD and test coverage
- "Intentional simplicity" philosophy — build the simplest thing that works, measure, iterate
- Production engineering with real numbers and real metrics (not theoretical)

Employer names (Amazon/AWS, Microsoft, ServiceNow) may appear as plain factual history in body text. They should **not** be bolded, headlined, or led with — see Section 1, Voice Split. This site's brand is the person, not the resume.

### Canonical URL Strategy

- All posts on `oldschool-engineer.dev` are the canonical source
- jekyll-seo-tag generates `<link rel="canonical">` automatically
- **Do not** set `canonical_url` in front matter unless pointing to a rare external canonical
- When cross-posting to Medium, their import tool reads the canonical tag automatically

---

## 13. Publishing Workflow (Jekyll → Medium)

### Process

1. **Publish on Jekyll first.** Push to `main` branch. Wait for GitHub Pages build to complete.
2. **Verify the post is live.** Check page source for `<link rel="canonical">` pointing to `oldschool-engineer.dev`.
3. **Import to Medium.** Use `https://medium.com/p/import` — paste the post URL.
4. **Medium reads the canonical tag** and sets `rel=canonical` back to the Jekyll site automatically.
5. **Review on Medium** for formatting issues before publishing.
6. **Publish on Medium** under `the.oldschool.engineer`.

### Medium Import Gotchas

| Issue | Workaround |
|-------|-----------|
| Code blocks lose syntax highlighting | Review and fix manually on Medium |
| Mermaid diagrams don't render | Replace with screenshot images in the Medium version |
| `{% post_url %}` tags don't resolve | Replace with absolute URLs (`https://oldschool-engineer.dev/...`) |
| Series nav blocks may break | Reformat for Medium's editor |
| Image paths may not resolve | They should — images are served from GitHub Pages — but verify |

---

## 14. Platform Strategy and Limitations

### Current Platform Strengths

- Free hosting on GitHub Pages
- Static site: fast, secure, no server maintenance
- Markdown-native workflow (ideal for AI agent editing)
- Built-in SEO plugins
- Custom domain with HTTPS

### Known Limitations

| Limitation | Current Impact | Threshold |
|-----------|---------------|-----------|
| Build time | Negligible at 16 posts | GitHub Pages has a 10-minute timeout; may hit at 100+ posts |
| Plugin restrictions | Manageable | Only GitHub Pages-supported plugins; no custom Ruby |
| No dynamic content | Client-side only (Lunr.js, GoatCounter) | Need for server-side features would require migration |
| No comments | None built in | Would need Utterances (GitHub Issues) or Giscus (Discussions) |
| No newsletter | No subscriber management | Would need external service (Buttondown, ConvertKit) |
| Repository size | Well under limit | GitHub Pages limit: 1 GB; image-heavy posts accumulate |
| No server-side redirects | None needed yet | Would need `jekyll-redirect-from` plugin |

### When to Consider Migration

- Build times regularly exceed 5 minutes
- Server-side functionality becomes necessary (API, database, authentication)
- Image storage approaches 1 GB
- Need for A/B testing or content personalization
- Need plugins not supported by GitHub Pages

### Migration Paths

| Option | Tradeoff |
|--------|----------|
| **Netlify or Vercel** | Same static model, more plugin flexibility, larger build limits |
| **Self-hosted Jekyll/Hugo on Proxmox** | Full control, consistent with Tom's infrastructure ethos |
| **Keep Jekyll, add microservices** | Best of both — static content with dynamic features via API |

---

## 15. Profile Consistency

### Active Profiles

| Platform | Handle / URL | Purpose | Voice |
|----------|-------------|---------|-------|
| Blog (canonical) | `https://oldschool-engineer.dev` | Primary content home | Personal notebook |
| GitHub | `https://github.com/oldschool-engineer` | Code, profile README | Personal notebook |
| GitHub (org) | `https://github.com/kuhl-haus` | Open source projects | Personal notebook |
| Medium | `https://the.oldschool.engineer` | Content distribution | Personal notebook |
| LinkedIn | `https://www.linkedin.com/in/thomaspounders` | Professional network | Professional record |
| Dad Jokes | `https://ur.janky.click` | Side project | N/A |

### Consistency Requirements

The **personal-notebook trio** (blog, GitHub profile, Medium) and **LinkedIn** are two separate voice tracks. Do not cross-pollinate them.

**Blog + GitHub + Medium — keep these three in sync with each other:**
- Identity framing: old-school engineer, geek with credentials. No "leadership," "organizational," or hiring-facing language.
- History: three decades — U.S. Navy Signals Intelligence, then Microsoft, Amazon/AWS, and now ServiceNow. Employers named once in body text, not bolded or headlined.
- Signature phrase: "building and operating Internet systems at planetary scale" — reuse it, it's load-bearing (it echoes the origin story in the README's "Why oldschool-engineer?" section).
- Disclaimer, present on all three: opinions are personal and don't represent any employer, past or present; nothing here is professional advice (needed because of trading content).
- No job-seeking CTA. Tom is not looking for a role.

**LinkedIn — maintained by Tom directly, deliberately different:**
- Exact HR title where precision matters (e.g., "Principal IAM Software Engineer" on the experience entry).
- Headline and About use "Principal Engineer" brand framing, employer-forward is fine there.
- Agents should not attempt to rewrite LinkedIn copy to match the blog's geek-notebook voice, or vice versa.

- Profile links should **cross-reference** each other where the platform allows (links are fine across voice tracks; prose style is not).
- When updating brand copy, change the blog/GitHub/Medium trio together. Do not touch LinkedIn copy without Tom's explicit direction — he treats it as a separate, hands-on-maintained surface.

### README.md Special Rules

This file serves double duty as both the GitHub profile page and the Jekyll homepage.

- **MUST NOT** have front matter (`---` delimiters). The `_config.yml` scope handles this with `title: " "`.
- Must render correctly on **both** GitHub (as profile) and Jekyll (as homepage).
- Uses GitHub badge shields (`img.shields.io`) for profile link badges.
- Featured project section currently highlights **Kuhl Haus MDP** — update when major projects change.
- Hero paragraph and closing CTA must follow the Voice Split rule in Section 1 — no leadership/hiring framing, no bolded employer names in the identity line.

---

## 16. Quick Reference

### New Post Template

```yaml
---
title: "Post Title"
excerpt: "One sentence excerpt."
categories:
  - Category Name
tags:
  - tag-name
---

***Optional subtitle in bold italic***

### First Section Heading

Content goes here.
```

### Series Nav Template

```markdown
📖 **Series Name:**
- [Part 1: Title]({% post_url YYYY-MM-DD-slug %})
- Part 2: Title (you are here)
- [Part 3: Title]({% post_url YYYY-MM-DD-slug %})
```

### Image Reference Template

```markdown
![](/assets/images/posts/{post-slug}/img-NN.ext)

*Caption text*
```

### Image Directory Template

```
assets/images/posts/{post-slug}/img-NN.ext
```

### Local Development

```bash
docker compose up
# Site: http://localhost:8001
```

### Post Filename Convention

```
_posts/YYYY-MM-DD-title-words-with-hyphens.md
```