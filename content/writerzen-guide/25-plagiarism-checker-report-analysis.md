# 5.2 Plagiarism Checker: Report Analysis

> **DigiTrust Lab status: HISTORICAL PRODUCT REFERENCE — SUPERSEDED.** This
> lesson documents a WriterZen capability for reference only. The DigiTrust
> Lab workflow prohibits running or requiring the paid WriterZen checker. Use
> `.claude/rules/native-originality-source-gate.md` for the current no-credit
> originality and source-attribution contract. Do not treat this lesson as a
> workflow instruction.

## Overview

This lesson covers the report analysis interface of the Plagiarism Checker tool, using the "nutrition plan" article as an example.

## Interface Layout

The report is split into two panels:

| Panel | Content |
|---|---|
| **Left panel** | Full article text with plagiarised sections highlighted |
| **Right panel** | Results summary, unique score, and source details |

## Left Panel: Plagiarism Highlights

Scroll through your article to find sections with overlaps. These are underlined in two colours:

| Colour | Degree of Plagiarism |
|---|---|
| 🟠 Orange underline | Moderate plagiarism |
| 🔴 Red underline | High plagiarism |

Click any underlined sentence to see the **original source** displayed in the right panel.

## Right Panel: Results Summary

| Metric | Description |
|---|---|
| **Plagiarism score** | Percentage of content identified as copied (e.g. 3% = 97% unique) |
| **Unique score** | Percentage of content that is original |
| **Total words checked** | Word count of the submitted content |
| **Total sentences checked** | Sentence count of the submitted content |

## Exporting the Report

Click **Export** to download a PDF version of the plagiarism report.

Before exporting, select which fields of analysis to include in the report. The PDF includes:
- Highlighted plagiarised content
- Original sources for each flagged section
- Section-by-section analysis of the entire article
- A link back to the original report in the Plagiarism Checker tool

## Exclude Domain Feature

The **Exclude Domain** button lets you exclude one or more URLs from being checked against your content.

> **Use case:** If you are rewriting an old article that is already published on your own site, exclude your own URL so the tool doesn't flag your original content as plagiarised.

## Archived Product Behaviour (Do Not Execute)

The original WriterZen course described copying a completed article into the
checker, reviewing highlights, and exporting a report. Those steps are
retained only to explain the historical screenshots and terminology in this
folder. They are explicitly superseded for DigiTrust Lab: do not run the
WriterZen checker or spend its plagiarism words. Apply
`.claude/rules/native-originality-source-gate.md` instead.
