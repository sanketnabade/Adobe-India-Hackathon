FROM --platform=linux/amd64 python:3.10-slim

WORKDIR /app

# Copy source code only
COPY src/ /app/src/

# Install system dependencies and Python packages
RUN apt-get update && apt-get install -y \
    libenchant-2-2 \
    build-essential \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir \
        pdfminer.six \
        pandas \
        joblib \
        scikit-learn \
        nltk \
    && python -c "import nltk; nltk.download('punkt', download_dir='/usr/local/share/nltk_data'); nltk.download('stopwords', download_dir='/usr/local/share/nltk_data'); nltk.download('averaged_perceptron_tagger', download_dir='/usr/local/share/nltk_data')" \
    && mkdir -p "/app/Collection 1" "/app/Collection 2" "/app/Collection 3"

# Set Python path
ENV PYTHONPATH=/app

# Run the processor
CMD ["python", "src/pdf_processor.py"]
