# Dual-Challenge PDF Processing Suite

A comprehensive PDF analysis solution combining machine learning classification with persona-based content extraction. This hackathon project tackles both structured text classification and intelligent document analysis for multiple use cases.

## What We Built

- *Challenge 1a*: ML-powered PDF text classifier that identifies headers, titles, and body text with confidence scoring
- *Challenge 1b*: Multi-collection document analyzer that extracts relevant content based on user personas and specific tasks

## Key Features

- *Smart Text Classification*: ML model distinguishes between different text elements (headers vs body text)
- *Persona-Based Analysis*: Tailored content extraction for travel planners, HR professionals, and food contractors
- *Multi-Document Processing*: Handles entire document collections simultaneously
- *Offline Operation*: No internet required during processing
- *Docker Containerized*: Easy deployment and consistent performance

## Project Structure


PDF_Processing_Suite/
├── Challenge_1a/
│   ├── src/pdf_processor.py        # ML classification engine
│   └── models/                     # Trained models
├── Challenge_1b/
│   ├── Collection 1/               # Travel Planning docs
│   ├── Collection 2/               # Adobe Acrobat guides  
│   ├── Collection 3/               # Recipe collections
│   └── src/pdf_processor.py        # Persona-based analyzer
├── docker-compose.yml
└── README.md


## Quick Start

bash
# Build both solutions
docker build -t pdf-classifier ./Challenge_1a
docker build -t pdf-analyzer ./Challenge_1b

# Run Classification (Challenge 1a)
docker run --rm \
    -v $(pwd)/input:/app/input:ro \
    -v $(pwd)/output:/app/output \
    pdf-classifier

# Run Analysis (Challenge 1b)  
docker run --rm \
    -v $(pwd)/Collections:/app/Collections:ro \
    pdf-analyzer


## Performance Highlights

- *Processing Speed*: ≤10 seconds for 50-page documents
- *Model Efficiency*: <200MB total model size
- *Resource Requirements*: 16GB RAM, 8 CPU cores
- *Accuracy*: High-confidence text classification with dictionary validation

## Use Cases Demonstrated

1. *Travel Planning*: Extract relevant info for group trips from travel guides
2. *HR Documentation*: Process Adobe Acrobat tutorials for form creation workflows  
3. *Catering Services*: Analyze recipe collections for vegetarian menu planning

## Dependencies

- Python 3.10+
- Docker with AMD64 support
- pdfminer.six
- pandas
- scikit-learn
- nltk
- joblib
- pyenchant

## Output Format

Both challenges generate structured JSON outputs with metadata, content classification, and relevance scoring for easy integration into downstream applications.

Built for efficiency, designed for real-world applications, and packaged for seamless deployment.
