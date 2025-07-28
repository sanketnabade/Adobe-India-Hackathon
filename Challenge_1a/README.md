
PDF Processing Solution - Challenge 1a
Greetings from the headquarters of the PDF Processing Superhero! This isn't your typical PDF processor; it's a document detective driven by machine learning that can look at a PDF and exclaim, "Aha! That squiggly thing is probably not a word, but that is a header and body text. 
Imagine having an exceptionally intelligent intern who reads fifty pages faster than you can say "machine learning magic!" and who never gets tired or needs coffee.
Features (AKA Our Superpowers)
•	Automatic processing of all PDFs - Throw PDFs at it like confetti, it'll handle them all!
•	ML-based text classification - Smarter than your average bear, can tell headers from body text (and won't get confused by Comic Sans)
•	Word validation using English dictionary - Has a built-in spell-checker that's more judgmental than your high school English teacher
•	Structured JSON output with metadata - Because messy data is like a messy room, but for computers
•	Docker containerization - Packaged like a Happy Meal, but for developers
Project Structure (Our Digital Real Estate)
Challenge_1a/
├── src/
│   ├── pdf_processor.py    # The brain of the operation
│   └── models/            # Where the AI magic lives
│       ├── trained_model.pkl      # The wise oracle
│       └── label_encoder.pkl      # The translator
├── Dockerfile              # The recipe for digital success
└── README.md              # You are here! (Again!)

Requirements (The Bare Minimums for Greatness)
•	Python 3.10+ - Because we're not living in the stone age
•	Docker with AMD64 support - The fancy container stuff
•	16GB RAM - More memory than a goldfish (barely)
•	8 CPU cores - More brains = better thinking power!
Dependencies (Our Trusty Sidekicks)
•	pdfminer.six - The PDF whisperer who speaks fluent document
•	pandas - The data wrangler extraordinaire (like a cowboy, but for spreadsheets)
•	joblib - The model loader (heavy lifting specialist)
•	pyenchant - The word police (stops nonsense from getting through)
Usage (The Magic Incantations)
Building the Docker Image (Summoning the Container)
docker build --platform linux/amd64 -t pdf-processor .
# Warning: May cause sudden urges to process ALL the PDFs

Running the Container (Releasing the Beast!)
docker run --rm \
    -v $(pwd)/input:/app/input:ro \
    -v $(pwd)/output:/app/output \
    --network none \
    pdf-processor
# --network none because this baby works offline (trust issues included)

Output Format (The Golden Treasure)
Each PDF gets transformed into a beautiful JSON butterfly:
{
    "metadata": {
        "filename": "once_boring_now_awesome.pdf",
        "pages": 5
    },
    "content": [
        {
            "text": "Look Ma, I'm Structured Data!",
            "page": 1,
            "bbox": [x0, y0, x1, y1],
            "type": "h1",
            "confidence": 1.0
        }
    ]
}

Translation: Each piece of text comes with its own little ID card telling you where it lives, what it is, and how confident our AI is about its classification (spoiler: it's usually pretty confident)
Performance (The Bragging Rights Section)
•	Processing Time: ≤ 10 seconds for 50-page PDF (faster than ordering pizza!)
•	Model Size: ≤ 200MB (smaller than most cat videos)
•	Internet Independence: Works offline (because the internet is overrated anyway)
•	CPU-only execution: No fancy GPU required (your laptop can handle this!)
Fun Fact: This system can process documents faster than most people can complain about having to process documents manually!
Remember: With great PDF processing power comes great responsibility. Use it wisely, and may all your documents be forever structured!
P.S. - Side effects may include: sudden productivity increases, reduced document-related stress, and an inexplicable urge to convert everything to JSON format.
