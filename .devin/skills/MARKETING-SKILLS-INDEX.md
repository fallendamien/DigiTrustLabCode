# Marketing Skills Index (Pruned for DigiTrust Lab)

> **Purpose:** Lightweight routing table for Claude Desktop. When a user request matches a trigger below, read the corresponding skill file from the marketing skills folder before executing. These are content/SEO/strategy skills — paid ads skills have been excluded (not running ads yet).

## How to Use

1. Match the user's request against the trigger phrases below
2. Read the full skill .md from the listed file path
3. Follow the skill's process/workflow
4. Only load one skill at a time (the matching one)

## Skills Available

### 📝 Content Repurposer
- **Triggers:** "repurpose my blog post", "turn this into social posts", "atomize this content", "create content derivatives", "repurpose content for linkedin", "repurpose for twitter", "make video script from blog"
- **File:** `G:\Zamzam Biznez\marketing-skills-main-for-LLMs\Skills for Claude\34-google-and-meta-content-repurposer.md`
- **What:** Transform one blog post into LinkedIn posts, tweet threads, email snippets, ad hooks, and video scripts while maintaining voice consistency

### ✉️ Email Sequence Writer
- **Triggers:** "write email sequence", "create nurture sequence", "welcome email flow", "promotional email", "email campaign", "write email series", "email nurture flow"
- **File:** `G:\Zamzam Biznez\marketing-skills-main-for-LLMs\Skills for Claude\36-google-and-meta-email-sequence-writer.md`
- **What:** Complete nurture email sequences with subject lines, preview text, and body copy using proven copywriting formulas

### 🎯 ICP Research Assistant
- **Triggers:** "research my ideal customer", "build buyer persona", "who is my target audience", "icp research", "customer profile", "buyer persona", "understand my audience"
- **File:** `G:\Zamzam Biznez\marketing-skills-main-for-LLMs\Skills for Claude\38-google-and-meta-icp-research-assistant.md`
- **What:** Build detailed buyer personas with pain points, objections, buying triggers, and messaging angles for the Malaysian business audience

### 🏗️ Programmatic SEO Builder
- **Triggers:** "build seo page templates", "programmatic seo", "scale content with templates", "create page template pattern", "bulk seo pages", "seo content templates"
- **File:** `G:\Zamzam Biznez\marketing-skills-main-for-LLMs\Skills for Claude\42-google-programmatic-seo-builder.md`
- **What:** Create scalable SEO page templates with title patterns, internal linking logic, schema markup, and thin content avoidance (e.g., "AI tools for [industry] in Malaysia")

### 📊 UTM Tracking Generator
- **Triggers:** "generate utm links", "create tracking parameters", "utm builder", "ga4 event naming", "conversion tracking setup", "standardize tracking", "campaign tracking"
- **File:** `G:\Zamzam Biznez\marketing-skills-main-for-LLMs\Skills for Claude\44-google-and-meta-utm-tracking-generator.md`
- **What:** Generate consistent UTM parameters, GA4 event naming, and conversion tracking specs following taxonomy best practices

### 🔍 Competitor Teardown
- **Triggers:** "analyze competitor", "competitor teardown", "competitor analysis", "what are competitors doing", "positioning analysis", "compare my site to competitors", "competitor messaging"
- **File:** `G:\Zamzam Biznez\marketing-skills-main-for-LLMs\Skills for Claude\33-google-and-meta-competitor-teardown.md`
- **What:** Systematic competitive analysis covering positioning, messaging hierarchy, objection handling, and CTA strategy from competitor URLs or screenshots

### 🚀 E2E SEO Assistant
- **Triggers:** "full seo audit", "end to end seo", "seo workflow", "complete seo analysis", "seo content plan", "seo strategy", "backlink opportunities", "content gap analysis"
- **File:** `G:\Zamzam Biznez\marketing-skills-main-for-LLMs\Skills for Claude\35-google-e2e-seo-assistant.md`
- **What:** Full SEO workflow covering technical audits, content gaps, backlink opportunities, on-page fixes, and content briefs — broader strategy than Respira's on-page SEO skill

## How These Complement Respira Skills

| Marketing Skill | Respira Skill | Relationship |
|----------------|---------------|--------------|
| E2E SEO Assistant | SEO & AEO Amplifier | Marketing = broader strategy (backlinks, gaps); Respira = on-page fixes + schema |
| Competitor Teardown | Conversion Audit | Marketing = competitor positioning; Respira = own-site CRO |
| ICP Research Assistant | Brand Voice Synthesizer | Marketing = who you're targeting; Respira = how you sound |
| Content Repurposer | Activity Report Composer | Marketing = create derivatives; Respira = report what was done |
| Programmatic SEO Builder | Internal Link Builder | Marketing = template structure; Respira = link existing content |
| Email Sequence Writer | — | No Respira equivalent — fills the email gap |
| UTM Tracking Generator | — | No Respira equivalent — fills the tracking gap |

## Rules

- **Read before executing:** Always read the full skill .md before following its workflow
- **One skill per request:** Don't load multiple skills simultaneously
- **Combine with Respira when relevant:** E.g., run E2E SEO Assistant for strategy, then Respira SEO Amplifier for on-page fixes
- **No paid ads skills:** 37 paid ads management skills were excluded — add them when you start running ads
