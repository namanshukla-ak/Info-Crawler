1. Frontend
Streamlit app
UI allows:
Inputting organization name, role title, search type.
Buttons to “Fetch Bios”, “Fetch Competing Searches”, “Fetch News”, “Trigger Workflow"
Review/edit tables inline.
Export button (CSV, DOCX, PDF).
Deployed: Containerized Streamlit App

2. Backend
Framework: FastAPI
Deployment:
Containerized (Docker) → ECS Fargate


APIs (called from Streamlit via REST):
POST /bios → run org site crawler → return structured bios.
POST /jobs → query job boards → return postings.
POST /news → fetch news → summarize & tag.
POST /trigger → creates a run_id, writes a Run record (DynamoDB), and emits events for the three modules.
GET /status/{run_id} → returns per-module progress and counts.
GET /exports/{run_id} → return presigned S3 URLs for files.
FastAPI emits EventBridge events (or SQS messages) per module; Lambda workers consume them asynchronously.


3. Scraping & Data Retrieval
People Bios:
Crawler
crawl4ai (primary) for smart page discovery & LLM-friendly chunking
Falls back to Playwright (headless Chromium) when JS rendering or tricky navigation is required
Storage: save raw HTML/JSON to S3/raw
Parsing: BeautifulSoup in a Lambda (or FastAPI worker) to extract person cards/sections
respect robots.txt, per-host rate limits, randomized delays


Competing Searches:
If no API: scrape via crawl4ai; Requests + BeautifulSoup; use Playwright for JS-heavy pages (as needed)
Normalize fields, then index to Amazon OpenSearch Serverless for search & de-dup across boards
News:
Use Google News / Bing News / Chronicle APIs (no heavy scraping)
Store raw payloads to **S3/raw`


4. ML/AI (LLM) Processing
Amazon Bedrock (Converse API).
Entity Extraction → For bios (structured JSON: name, title, org, bio_short, bio_long, headshot, tenure).
Summarization→ For news (2–3 sentences).
Tagging→ Classification: Leadership Change / Org Dev / Financial / Scandal / General.
Implementation: FastAPI/Lambda calls boto3 bedrock-runtime; enforce JSON-schema; validate/ retry if malformed
Outputs: write curated JSON to DynamoDB and S3/curated; index searchable fields to OpenSearch


5. Data Layer
S3 (versioned):
raw/ → HTML/news/job payloads.
curated/ → structured JSON results.
exports/ → final DOCX/CSV/PDF files.
DynamoDB (NoSQL, simple for POC):
runs (run_id, status, timestamps).
people, jobs, news tables keyed by run_id.
Amazon OpenSearch Serverless:
Index people & jobs for fast search, filters, and fuzzy de-dup (name/title/institution; cross-board postings)
Store only searchable fields; keep raw/curated sources in S3


6. Export
Exporter Service:
Python script
Export in CSV only
Saves output to S3/exports/.
Streamlit fetches presigned S3 link via FastAPI → user downloads file.


7. Security & Observability
Secrets Manager → API keys.
CloudWatch Logs → Lambda + ECS logs.
Basic IAM policies → least privilege for Lambdas/ECS to S3/Dynamo/Bedrock.
Dynamo TTL → expire data after 90 days.


8. Other Notes
crawl4ai: accelerates discovery + content extraction; integrates well with LLM post-processing
BeautifulSoup: lightweight HTML parsing/cleanup before sending chunks to Bedrock
Amazon OpenSearch: central place for search, filtering, and deduplication; ideal for handling duplicates across multiple job boards and similar names/titles in bios
