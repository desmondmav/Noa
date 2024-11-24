import spacy
import nltk
from typing import List, Dict
import logging
from transformers import pipeline

class TextAnalyzer:
    """
    Advanced text analysis module using NLP techniques
    """
    def __init__(self):
        # Load spaCy model
        try:
            self.nlp = spacy.load('en_core_web_sm')
            nltk.download('punkt', quiet=True)
            
            # Initialize sentiment analysis pipeline
            self.sentiment_analyzer = pipeline('sentiment-analysis')
        except Exception as e:
            logging.error(f"NLP model loading failed: {e}")
            raise

    def extract_keywords(self, text: str, top_n: int = 5) -> List[str]:
        """
        Extract top keywords from the given text
        
        :param text: Input text
        :param top_n: Number of top keywords to return
        :return: List of top keywords
        """
        try:
            doc = self.nlp(text)
            
            # Filter for nouns and proper nouns
            keywords = [
                token.text for token in doc 
                if token.pos_ in ['NOUN', 'PROPN'] and len(token.text) > 2
            ]
            
            # Remove duplicates while preserving order
            keywords = list(dict.fromkeys(keywords))
            
            return keywords[:top_n]
        except Exception as e:
            logging.error(f"Keyword extraction failed: {e}")
            return []

    def analyze_sentiment(self, text: str) -> Dict[str, float]:
        """
        Perform sentiment analysis on the given text
        
        :param text: Input text
        :return: Sentiment analysis results
        """
        try:
            result = self.sentiment_analyzer(text)[0]
            return {
                'sentiment': result['label'],
                'confidence': result['score']
            }
        except Exception as e:
            logging.error(f"Sentiment analysis failed: {e}")
            return {'sentiment': 'NEUTRAL', 'confidence': 0.5}

    def summarize_text(self, text: str, max_length: int = 150) -> str:
        """
        Generate a concise summary of the input text
        
        :param text: Input text
        :param max_length: Maximum length of summary
        :return: Summarized text
        """
        try:
            summarizer = pipeline('summarization')
            summary = summarizer(
                text, 
                max_length=max_length, 
                min_length=50, 
                do_sample=False
            )[0]['summary_text']
            
            return summary
        except Exception as e:
            logging.error(f"Text summarization failed: {e}")
            return text[:max_length]