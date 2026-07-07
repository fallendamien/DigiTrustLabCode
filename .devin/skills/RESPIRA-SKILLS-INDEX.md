# Respira Skills Index

> **Purpose:** Lightweight routing table for Claude Desktop. When a user request matches a trigger below, read the corresponding SKILL.md from the workspace before executing. Never guess a skill's workflow without reading the file first.

## How to Use

1. Match the user's request against the trigger phrases below
2. Read the full SKILL.md from the listed file path
3. Follow the skill's execution workflow using Respira MCP tools
4. Only load one skill at a time (the matching one)

## Skills Available

### 🔍 SEO & AEO Amplifier
- **Triggers:** "amplify my seo", "seo audit", "optimize for search engines", "improve search visibility", "scan for seo opportunities", "aeo audit"
- **File:** `.devin/skills/seo-aeo-amplifier/SKILL.md`
- **What:** On-page SEO + Answer Engine Optimization audit with schema markup generation and auto-fix on duplicates

### 🎙️ Brand Voice Synthesizer
- **Triggers:** "extract my brand voice", "what's my writing style", "analyze my tone", "build a voice guide", "synthesize my voice", "capture my writing style"
- **File:** `.devin/skills/brand-voice-synthesizer/SKILL.md`
- **What:** Reads 5-10 published posts, extracts brand voice (tone, lexicon, sentence patterns), persists to site memory

### 🔗 Internal Link Builder
- **Triggers:** "build internal links", "improve internal linking", "find internal link opportunities", "interlink my content", "fix orphaned pages", "create topic clusters", "internal link audit"
- **File:** `.devin/skills/internal-link-builder/SKILL.md`
- **What:** Analyzes all content, maps topic relationships, finds linking opportunities, presents plan for approval before changes

### 📅 Stale Content Detector
- **Triggers:** "find old content", "what's stale", "what needs refreshing", "audit my content age", "find content to update", "stale content scan", "what should i archive"
- **File:** `.devin/skills/stale-content-detector/SKILL.md`
- **What:** Categorizes content as fresh/aging/stale/archive-candidate, suggests refresh/redirect/archive per item

### 🎯 Conversion Audit
- **Triggers:** "audit my conversion rate", "cro check", "find conversion leaks", "review my landing pages", "audit for conversion", "what's hurting my conversion", "conversion audit"
- **File:** `.devin/skills/conversion-audit/SKILL.md`
- **What:** Audits 6 dimensions (above-the-fold clarity, CTA hierarchy, form length, social proof, page speed, trust signals) with prioritized fixes

### 🖼️ WordPress AI Image Optimizer
- **Triggers:** "optimize my images", "compress my media library", "convert images to webp", "my images are too big", "image optimization audit", "reduce image file sizes", "fix my slow images"
- **File:** `.devin/skills/wordpress-ai-image-optimizer/SKILL.md`
- **What:** Compress, WebP-convert, resize, and rename images locally — no external uploads, no API keys

### 📱 Mobile Experience Report
- **Triggers:** "audit mobile experience", "check mobile layout", "mobile responsive issues", "what do mobile users see", "mobile design problems", "responsive audit", "site broken on phones", "mobile ux audit"
- **File:** `.devin/skills/mobile-experience-report/SKILL.md`
- **What:** Real mobile metrics (Core Web Vitals + Lighthouse) plus structural analysis of responsive breakpoint issues

### 📊 Activity Report Composer
- **Triggers:** "generate activity report", "what did we do this month", "monthly report", "client report", "summarize recent activity", "activity summary", "what changed on my site"
- **File:** `.devin/skills/activity-report-composer/SKILL.md`
- **What:** Turns Respira's audit log into a polished client-ready report with totals, highlights, and timeline

### 🎨 Design System Synthesizer
- **Triggers:** "build a design system for my site", "extract my brand", "synthesize a design system", "create my design tokens", "what does my site look like", "capture my brand", "build my style guide", "extract design tokens"
- **File:** `.devin/skills/design-system-synthesizer/SKILL.md`
- **What:** Extracts logo, color palette, typography, spacing, component patterns from existing pages, persists as design tokens + builds visible style-guide page

### 🧬 WordPress Site DNA
- **Triggers:** "analyze my wordpress site", "wordpress site audit", "site dna", "what's running on my site", "wordpress archaeology", "scan my wordpress installation", "check my wordpress health", "audit my wordpress"
- **File:** `.devin/skills/wordpress-site-dna/SKILL.md`
- **What:** Full archaeological X-ray — builders, plugins, content structure, orphaned shortcodes, performance, security posture, health score

### 📋 Technical Debt Audit
- **Triggers:** "audit my wordpress technical debt", "find orphaned shortcodes", "scan for unused plugins", "check database bloat", "wordpress cleanup audit", "find legacy code issues", "wordpress technical debt", "clean up my wordpress", "what's bloating my wordpress"
- **File:** `.devin/skills/technical-debt-audit/SKILL.md`
- **What:** Finds orphaned content, unused plugins, database bloat, unused media, dormant builders — with snapshot-gated cleanup playbooks

### 🚀 Prime the Agent
- **Triggers:** "prime yourself", "prime the agent", "get ready to work on this site", "understand my site setup", "before we start", "prepare to work on wordpress", "warm up on this site", "load context for this site", "what builder does this site use", "give me a site briefing"
- **File:** `.devin/skills/prime-the-agent/SKILL.md`
- **What:** 30-second session starter — loads site context, identifies builder, loads schemas, primes on do-not-write-raw-HTML rule, reads site memory

## Rules

- **Read before executing:** Always read the full SKILL.md before following its workflow
- **One skill per request:** Don't load multiple skills simultaneously
- **Respira MCP required:** All skills require the Respira WordPress MCP server to be connected
- **SafeEdit by default:** Skills that make changes use duplicate-first workflow with snapshots
- **Telemetry is fire-and-forget:** Never block report delivery on telemetry failure
