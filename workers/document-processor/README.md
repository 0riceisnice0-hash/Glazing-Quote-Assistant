# GQA Document Processor Worker

Optional Cloudflare Worker for internal Glazing Quote Assistant document intake.

The main app still runs on GitHub Pages. This Worker is used only when the upload screen has **Use Cloudflare Worker for unsupported documents** enabled and a Worker URL configured.

## What It Does

- Expands ZIP tender packs.
- Reads DOCX text from `word/document.xml`.
- Reads EML subject/body text.
- Emits normalised document objects, intake records, risks, and proposed supplier evidence.
- Leaves PDF and Excel extraction to the browser app.

## Current Limits

- MSG parsing is not implemented yet.
- JPG/PNG OCR is not implemented in the Worker yet. Browser Tesseract remains the free OCR path.
- The Worker does not price anything. It only normalises document input.

## Local Dev

```powershell
cd workers\document-processor
npm install
npm run dev
```

Use the local Worker URL in the app upload settings.

## Deploy

```powershell
cd workers\document-processor
npm install
npm run deploy
```

Then paste the deployed `https://...workers.dev` URL into the app.

Current deployed internal Worker:

```text
https://gqa-document-processor.0riceisnice0.workers.dev
```

## API

- `GET /health`
- `POST /process-file`
- `POST /process-pack`

Both POST endpoints accept `multipart/form-data` with one or more `files` entries and return:

```json
{
  "documents": [],
  "risks": [],
  "supplierEvidence": [],
  "intakeRecords": []
}
```
