import os
import json
from pathlib import Path
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import joblib
from collections import defaultdict
from enchant import Dict
import pandas as pd

# Constants
INPUT_DIR = Path("/app/input")
OUTPUT_DIR = Path("/app/output")
MODEL_DIR = Path(__file__).parent / "models"
FEATURES = [
    "font_size", "font_weight", "is_all_caps", "word_count", "page",
    "bbox_x0", "bbox_y0", "bbox_x1", "bbox_y1"
]
TARGET_LABELS = ["H1", "H2", "H3", "T"]

class PDFProcessor:
    def __init__(self):
        self.dictionary = Dict("en_US")
        self.model = joblib.load(MODEL_DIR / "trained_model.pkl")
        
    def extract_features_from_pdf(self, pdf_path):
        all_data = []
        for page_number, page_layout in enumerate(extract_pages(pdf_path), start=1):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    for text_line in element:
                        text = text_line.get_text().strip()
                        if not text:
                            continue
                        
                        font_size = 0
                        font_name = ""
                        for char in text_line:
                            if isinstance(char, LTChar):
                                font_size = round(char.size, 2)
                                font_name = char.fontname
                                break
                                
                        is_bold = 1 if "bold" in font_name.lower() else 0
                        is_all_caps = 1 if text.isupper() and text.isalpha() else 0
                        word_count = len(text.split())
                        bbox = [round(x, 2) for x in text_line.bbox]

                        features = {
                            "font_size": font_size,
                            "font_weight": is_bold,
                            "is_all_caps": is_all_caps,
                            "word_count": word_count,
                            "page": page_number,
                            "bbox_x0": bbox[0],
                            "bbox_y0": bbox[1],
                            "bbox_x1": bbox[2],
                            "bbox_y1": bbox[3],
                        }

                        all_data.append({
                            "text": text,
                            "bbox": bbox,
                            "features": features
                        })
        return all_data

    def process_pdf(self, pdf_path):
        data = self.extract_features_from_pdf(pdf_path)
        X = [item["features"] for item in data]

        X_df = pd.DataFrame(X)
        X_df = X_df[FEATURES]

        predictions = self.model.predict(X_df)

        # Organize outputs
        output_dict = {
            "metadata": {
                "filename": pdf_path.name,
                "pages": max(item["features"]["page"] for item in data)
            },
            "content": []
        }

        for item, pred_label in zip(data, predictions):
            page = item["features"]["page"]
            text = item["text"]

            # Validate words
            words = text.split()
            valid_words = [word for word in words if self.dictionary.check(word)]
            if not valid_words:
                continue

            # Special handling for title (H1 on first page)
            content_item = {
                "text": text,
                "page": page,
                "bbox": item["bbox"],
                "type": "title" if pred_label == "H1" and page == 1 else pred_label.lower(),
                "confidence": 1.0  # Add actual confidence if model supports it
            }
            
            output_dict["content"].append(content_item)

        return output_dict

    def process_all_pdfs(self):
        """Process all PDFs in the input directory."""
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        
        for pdf_file in INPUT_DIR.glob("*.pdf"):
            try:
                output = self.process_pdf(pdf_file)
                output_file = OUTPUT_DIR / f"{pdf_file.stem}.json"
                
                with open(output_file, "w", encoding="utf-8") as f:
                    json.dump(output, f, indent=2, ensure_ascii=False)
                    
                print(f"Processed {pdf_file.name} -> {output_file.name}")
            except Exception as e:
                print(f"Error processing {pdf_file.name}: {str(e)}")

def main():
    processor = PDFProcessor()
    processor.process_all_pdfs()

if __name__ == "__main__":
    main()
