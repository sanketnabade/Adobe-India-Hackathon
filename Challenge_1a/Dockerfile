FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libenchant-2-2 \
    && rm -rf /var/lib/apt/lists/*

# Copy source code and models
COPY src/ /app/src/

# Install Python dependencies
RUN pip install --no-cache-dir \
    pdfminer.six \
    pandas \
    joblib \
    pyenchant \
    scikit-learn

# Create directories
RUN mkdir -p /app/input /app/output

# Set Python path
ENV PYTHONPATH=/app

# Run the processor
CMD ["python", "src/pdf_processor.py"]
