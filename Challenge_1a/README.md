# PDF Processing Solution - Challenge 1a

This solution implements a machine learning-based PDF processing system that extracts structured data from PDF documents and outputs JSON files. The system uses a trained model to identify and classify different text elements within the PDF.

## Features

- Automatic processing of all PDFs in input directory
- ML-based text classification (headers, titles, body text)
- Word validation using English dictionary
- Structured JSON output with metadata
- Docker containerization for easy deployment

## Project Structure

```
Challenge_1a/
├── src/
│   ├── pdf_processor.py    # Main processing logic
│   └── models/            # Trained models
│       ├── trained_model.pkl
│       └── label_encoder.pkl
├── Dockerfile
└── README.md
```

## Requirements

- Python 3.10+
- Docker with AMD64 support
- 16GB RAM
- 8 CPU cores

## Dependencies

- pdfminer.six: PDF text extraction
- pandas: Data processing
- joblib: Model loading
- pyenchant: Word validation

## Usage

### Building the Docker Image

```bash
docker build --platform linux/amd64 -t pdf-processor .
```

### Running the Container

```bash
docker run --rm \
    -v $(pwd)/input:/app/input:ro \
    -v $(pwd)/output:/app/output \
    --network none \
    pdf-processor
```

## Output Format

The solution generates a JSON file for each processed PDF with the following structure:

```json
{
    "metadata": {
        "filename": "example.pdf",
        "pages": 5
    },
    "content": [
        {
            "text": "Sample Text",
            "page": 1,
            "bbox": [x0, y0, x1, y1],
            "type": "h1",
            "confidence": 1.0
        }
    ]
}
```

## Performance

- Processing Time: ≤ 10 seconds for 50-page PDF
- Model Size: ≤ 200MB
- No internet access required during runtime
- CPU-only execution (no GPU required)

## Limitations

- English language support only
- PDF must be text-based (not scanned images)
- Limited support for complex layouts
