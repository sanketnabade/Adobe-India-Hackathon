# Challenge 1b: Multi-Collection PDF Analysis

## Overview

An advanced PDF analysis solution that processes multiple document collections and extracts relevant content based on specific personas and use cases. The solution uses natural language processing and machine learning techniques to identify and rank relevant sections of documents.

## Project Structure

```
Challenge_1b/
├── Collection 1/                    # Travel Planning
│   ├── PDFs/                       # South of France guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 2/                    # Adobe Acrobat Learning
│   ├── PDFs/                       # Acrobat tutorials
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── Collection 3/                    # Recipe Collection
│   ├── PDFs/                       # Cooking guides
│   ├── challenge1b_input.json      # Input configuration
│   └── challenge1b_output.json     # Analysis results
├── src/
│   └── pdf_processor.py            # Main processing logic
├── Dockerfile
└── README.md
```

## Features

- Persona-based content analysis
- Task-specific relevance ranking
- Multi-document processing
- Structured JSON output with metadata
- Font-size based section identification
- TF-IDF based content relevance scoring

## Collections

### Collection 1: Travel Planning

- Challenge ID: round_1b_002
- Persona: Travel Planner
- Task: Plan a 4-day trip for 10 college friends to South of France
- Documents: 7 travel guides

### Collection 2: Adobe Acrobat Learning

- Challenge ID: round_1b_003
- Persona: HR Professional
- Task: Create and manage fillable forms for onboarding and compliance
- Documents: 15 Acrobat guides

### Collection 3: Recipe Collection

- Challenge ID: round_1b_001
- Persona: Food Contractor
- Task: Prepare vegetarian buffet-style dinner menu for corporate gathering
- Documents: 9 cooking guides

## Input/Output Format

### Input JSON Structure

```json
{
  "challenge_info": {
    "challenge_id": "round_1b_XXX",
    "test_case_name": "specific_test_case"
  },
  "documents": [{ "filename": "doc.pdf", "title": "Title" }],
  "persona": { "role": "User Persona" },
  "job_to_be_done": { "task": "Use case description" }
}
```

### Output JSON Structure

```json
{
  "metadata": {
    "input_documents": ["list"],
    "persona": "User Persona",
    "job_to_be_done": "Task description"
  },
  "extracted_sections": [
    {
      "document": "source.pdf",
      "section_title": "Title",
      "importance_rank": 1,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    {
      "document": "source.pdf",
      "refined_text": "Content",
      "page_number": 1
    }
  ]
}
```

## Building and Running

### Build the Docker Image

```bash
docker build --platform linux/amd64 -t pdf-analyzer .
```

### Run the Container

```bash
docker run --rm \
    -v $(pwd)/Collection\ 1:/app/Collection\ 1:ro \
    -v $(pwd)/Collection\ 2:/app/Collection\ 2:ro \
    -v $(pwd)/Collection\ 3:/app/Collection\ 3:ro \
    --network none \
    pdf-analyzer
```

## Technical Details

### Analysis Pipeline

1. PDF Text Extraction

   - Extracts text and metadata using pdfminer.six
   - Preserves font size information for structure analysis

2. Section Identification

   - Uses font size analysis to identify potential headers/titles
   - Splits content into meaningful sections using NLP

3. Relevance Ranking

   - Uses TF-IDF vectorization for content analysis
   - Ranks sections based on relevance to task description
   - Considers both textual content and structural importance

4. Content Refinement
   - Filters out irrelevant sections
   - Organizes content by importance and relevance
   - Maintains document structure and context

## Dependencies

- Python 3.10
- pdfminer.six
- pandas
- scikit-learn
- nltk
- Docker with AMD64 support
