import os
import json
from pathlib import Path
from typing import List, Dict, Any
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
import joblib
from collections import defaultdict
import pandas as pd
import nltk
from nltk.tokenize import sent_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

class PersonaBasedAnalyzer:
    def __init__(self):
        self.stop_words = set(stopwords.words('english'))
        self.vectorizer = TfidfVectorizer(stop_words='english')
        
        # Load the trained model from Challenge 1a
        challenge1a_model_path = Path(__file__).parent.parent.parent / "Challenge_1a/src/models/trained_model.pkl"
        if challenge1a_model_path.exists():
            self.structure_classifier = joblib.load(challenge1a_model_path)
        else:
            print("Warning: Challenge 1a model not found. Will use font-size based classification only.")
            self.structure_classifier = None
            
        # Features required by Challenge 1a model
        self.FEATURES = [
            "font_size", "font_weight", "is_all_caps", "word_count", "page",
            "bbox_x0", "bbox_y0", "bbox_x1", "bbox_y1"
        ]
        
    def extract_text_from_pdf(self, pdf_path: str) -> List[Dict[str, Any]]:
        """Extract text and metadata from PDF using both Challenge 1a model and enhanced analysis."""
        sections = []
        
        for page_num, page_layout in enumerate(extract_pages(pdf_path), 1):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    text = element.get_text().strip()
                    if not text:
                        continue
                        
                    # Extract features using Challenge 1a approach
                    font_size = 0
                    font_name = ""
                    for char in element:
                        if isinstance(char, LTChar):
                            font_size = round(char.size, 2)
                            font_name = char.fontname
                            break
                    
                    # Calculate features
                    is_bold = 1 if "bold" in font_name.lower() else 0
                    is_all_caps = 1 if text.isupper() and text.isalpha() else 0
                    word_count = len(text.split())
                    bbox = [round(x, 2) for x in element.bbox]
                    
                    # Create feature dictionary
                    features = {
                        "font_size": font_size,
                        "font_weight": is_bold,
                        "is_all_caps": is_all_caps,
                        "word_count": word_count,
                        "page": page_num,
                        "bbox_x0": bbox[0],
                        "bbox_y0": bbox[1],
                        "bbox_x1": bbox[2],
                        "bbox_y1": bbox[3],
                    }
                    
                    # Get structure prediction if model is available
                    structure_type = None
                    if self.structure_classifier is not None:
                        X = pd.DataFrame([features])[self.FEATURES]
                        structure_type = self.structure_classifier.predict(X)[0]
                    
                    sections.append({
                        "page_number": page_num,
                        "text": text,
                        "features": features,
                        "structure_type": structure_type,
                        "font_size": font_size
                    })
                
        return sections

    def identify_sections(self, sections: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Identify and label different sections using both Challenge 1a model and enhanced analysis."""
        if not sections:
            return []
            
        structured_sections = []
        for section in sections:
            # Use Challenge 1a model classification if available
            is_title = False
            if section["structure_type"] in ["H1", "H2", "H3"]:
                is_title = True
            elif section["structure_type"] is None:
                # Fallback to font size analysis if model not available
                font_sizes = [s["font_size"] for s in sections]
                median_font = sorted(font_sizes)[len(font_sizes)//2]
                is_title = section["font_size"] > median_font
            
            # Split into sentences for better analysis
            sentences = sent_tokenize(section["text"])
            
            for sent in sentences:
                structured_sections.append({
                    "text": sent,
                    "page_number": section["page_number"],
                    "is_title": is_title,
                    "structure_type": section["structure_type"]
                })
                
        return structured_sections

    def rank_sections(self, sections: List[Dict[str, Any]], task_description: str) -> List[Dict[str, Any]]:
        """Rank sections based on relevance to the task."""
        if not sections:
            return []
            
        # Prepare texts for TF-IDF
        texts = [section["text"] for section in sections]
        texts.append(task_description)  # Add task description as the last document
        
        # Calculate TF-IDF and similarities
        tfidf_matrix = self.vectorizer.fit_transform(texts)
        similarities = cosine_similarity(tfidf_matrix[:-1], tfidf_matrix[-1:])
        
        # Add similarity scores to sections
        ranked_sections = []
        for section, similarity in zip(sections, similarities):
            section_copy = section.copy()
            section_copy["relevance_score"] = float(similarity[0])
            ranked_sections.append(section_copy)
            
        # Sort by relevance score
        ranked_sections.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        return ranked_sections

    def analyze_collection(self, input_config: Dict[str, Any], collection_path: Path) -> Dict[str, Any]:
        """Analyze a collection of PDFs based on the input configuration."""
        results = {
            "metadata": {
                "input_documents": [],
                "persona": input_config["persona"]["role"],
                "job_to_be_done": input_config["job_to_be_done"]["task"]
            },
            "extracted_sections": [],
            "subsection_analysis": []
        }
        
        # Process each document in the collection
        for doc_info in input_config["documents"]:
            pdf_path = collection_path / "PDFs" / doc_info["filename"]
            if not pdf_path.exists():
                print(f"Warning: {pdf_path} not found")
                continue
                
            results["metadata"]["input_documents"].append(doc_info["filename"])
            
            # Extract and analyze content
            sections = self.extract_text_from_pdf(str(pdf_path))
            structured_sections = self.identify_sections(sections)
            ranked_sections = self.rank_sections(
                structured_sections,
                input_config["job_to_be_done"]["task"]
            )
            
            # Add high-level sections
            for section in ranked_sections:
                if section["is_title"] and section["relevance_score"] > 0.1:
                    results["extracted_sections"].append({
                        "document": doc_info["filename"],
                        "section_title": section["text"],
                        "importance_rank": len(results["extracted_sections"]) + 1,
                        "page_number": section["page_number"]
                    })
            
            # Add detailed content analysis
            for section in ranked_sections[:5]:  # Top 5 most relevant sections
                results["subsection_analysis"].append({
                    "document": doc_info["filename"],
                    "refined_text": section["text"],
                    "page_number": section["page_number"]
                })
                
        return results

def process_collections(base_path: Path):
    """Process all collections in the challenge."""
    analyzer = PersonaBasedAnalyzer()
    
    # Process each collection
    for collection in ["Collection 1", "Collection 2", "Collection 3"]:
        collection_path = base_path / collection
        input_file = collection_path / "challenge1b_input.json"
        output_file = collection_path / "challenge1b_output.json"
        
        # Load input configuration
        if not input_file.exists():
            print(f"Warning: {input_file} not found")
            continue
            
        with open(input_file, 'r', encoding='utf-8') as f:
            input_config = json.load(f)
        
        # Analyze collection
        results = analyzer.analyze_collection(input_config, collection_path)
        
        # Save results
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"Processed {collection}: {len(results['extracted_sections'])} sections extracted")

if __name__ == "__main__":
    base_path = Path(__file__).parent.parent
    process_collections(base_path)
