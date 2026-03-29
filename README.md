# United Way Survey Analysis — Pipeline

## 1. Introduction

This project processes and analyzes transcripts from community session collected by United Way. The raw input consists of 31 structured `.docx` files, each representing a recorded conversation with a community group. The pipeline transforms these files into a clean, structured dataset suitable for NLP analysis, topic modeling, and question-based semantic retrieval.

---

## 2. Project Description

Each source document contains metadata (facilitator name, date, organization), summary keywords, and a full conversation transcript. The pipeline reads these files, extracts and normalizes their content, and stores the output in a tabular DataFrame format.

The end goal is to answer specific research questions about community sentiment, values, and challenges — segmented by county, ALICE (Asset Limited, Income Constrained, Employed) status, and other demographic dimensions. The approach draws inspiration from Common Crawl-style text preprocessing, applying tokenization, whitespace normalization, deduplication, and embedding-based topic clustering to surface meaningful patterns across the corpus.

---

## 3. High-Level Goal

**Core Objective:** For each of the research questions posed in the assignment, generate:
- A summary of aggregate answers across all 31 conversations
- A general sentiment reading (positive, neutral, negative, mixed)
- Identification of differences by:
  - **County** — Are certain geographic areas expressing distinct concerns or strengths?
  - **ALICE Status** — Do asset-limited, income-constrained populations report different challenges, values, or levels of connectedness than higher-income groups?
  - **Other Demographics** — Age groups, organizational type (senior living, community group, etc.), meeting size, and population identifiers flagged in the data (e.g., groups identifying with one or more marginalized categories)

The output should make it straightforward to compare, for example, how transportation challenges are discussed in one county vs. another, or whether ALICE populations consistently report feeling more disconnected from community resources.

---

## 4. Initial Steps

### Step 1 — Read Source Files
- Iterate over all 31 `.docx` files
- Use `doc2txt` or `python-docx` to extract raw text
- Preserve document structure: INFO-TABLE block, IMAGE references, Summary Keywords section, and Transcript section

### Step 2 — Convert to `.txt`
- Write each document's extracted content to a corresponding `.txt` file
- Structure each `.txt` consistently:
  - Facilitator name
  - Date of conversation
  - Organization/group name
  - Summary keywords
  - Full transcript text

### Step 3 — Store Tabular Data
- Parse each `.txt` file and populate a Pandas DataFrame with the following columns:
  - `Name of Facilitator`
  - `Date of Conversation`
  - `Name of Organisation/Group`
  - `Meeting Location`
  - `Length of Time`
  - `Number of Attendees`
  - `Population — Identify for One or More Groups`
  - `Connected / Disconnected`
  - `Full Text`
  - `Number of Words in Full Text`
  - `Number of Sentences`

### Step 4 — Text Cleaning
Apply the following preprocessing in order:
1. **Whitespace removal** — strip leading/trailing whitespace, normalize internal spacing
2. **Sentence tokenization + filtering** — remove sentences with fewer than 3 words *unless* they contain a named entity
3. **Intra-sentence deduplication** — remove repeated words within a single sentence

### Step 5 — Embeddings and Topic Clustering
- Generate sentence or document embeddings (e.g., using `sentence-transformers`)
- Apply clustering (e.g., K-Means or HDBSCAN) to identify latent topics across conversations
- Label clusters manually or via keyword extraction to align with known themes (e.g., transportation, cost of living, aging in place, social isolation)

### Step 6 — Question-Based Semantic Matching
- For each of the 4 research questions from the assignment instructions, use semantic similarity (embedding cosine distance) to retrieve the most relevant passages from each document
- Aggregate answers at the corpus level, then slice by county, ALICE status, and other demographic fields
- Output summaries and sentiment scores per question per demographic segment