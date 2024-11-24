from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTextEdit, QLabel, QFileDialog
)
from PyQt6.QtCore import Qt
import pytesseract
from PIL import Image
import PyPDF2
import docx

from src.ai_modules.text_analyzer import TextAnalyzer

class DocumentAnalyzerWidget(QWidget):
    """
    Advanced document analysis widget
    """
    def __init__(self):
        super().__init__()
        
        # Initialize text analyzer
        self.text_analyzer = TextAnalyzer()
        
        # Setup main layout
        layout = QVBoxLayout()
        
        # File selection button
        self.file_btn = QPushButton('Select Document')
        self.file_btn.clicked.connect(self._select_document)
        layout.addWidget(self.file_btn)
        
        # Document content display
        self.content_display = QTextEdit()
        self.content_display.setReadOnly(True)
        layout.addWidget(self.content_display)
        
        # Analysis results
        self.keywords_label = QLabel('Keywords:')
        self.sentiment_label = QLabel('Sentiment:')
        self.summary_label = QLabel('Summary:')
        
        layout.addWidget(self.keywords_label)
        layout.addWidget(self.sentiment_label)
        layout.addWidget(self.summary_label)
        
        # Analyze button
        self.analyze_btn = QPushButton('Analyze Document')
        self.analyze_btn.clicked.connect(self._analyze_document)
        layout.addWidget(self.analyze_btn)
        
        self.setLayout(layout)

    def _select_document(self):
        """
        Open file dialog to select document
        """
        file_path, _ = QFileDialog.getOpenFileName(
            self, 
            'Select Document', 
            '', 
            'All Files (*);;PDF Files (*.pdf);;Word Files (*.docx);;Image Files (*.png *.jpg *.jpeg)'
        )
        
        if file_path:
            try:
                extracted_text = self._extract_text(file_path)
                self.content_display.setText(extracted_text)
            except Exception as e:
                self.content_display.setText(f"Error extracting text: {str(e)}")

    def _extract_text(self, file_path):
        """
        Extract text from different document types
        """
        file_extension = file_path.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return self._extract_pdf_text(file_path)
        elif file_extension == 'docx':
            return self._extract_docx_text(file_path)
        elif file_extension in ['png', 'jpg', 'jpeg']:
            return self._extract_image_text(file_path)
        else:
            raise ValueError("Unsupported file type")

    def _extract_pdf_text(self, file_path):
        """
        Extract text from PDF
        """
        with open(file_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            text = ''
            for page in reader.pages:
                text += page.extract_text()
        return text

    def _extract_docx_text(self, file_path):
        """
        Extract text from Word document
        """
        doc = docx.Document(file_path)
        return '\n'.join([para.text for para in doc.paragraphs])

    def _extract_image_text(self, file_path):
        """
        Extract text from image using OCR
        """
        image = Image.open(file_path)
        return pytesseract.image_to_string(image)

    def _analyze_document(self):
        """
        Perform comprehensive document analysis
        """
        text = self.content_display.toPlainText()
        
        if not text:
            return
        
        # Extract keywords
        keywords = self.text_analyzer.extract_keywords(text)
        self.keywords_label.setText(f"Keywords: {', '.join(keywords)}")
        
        # Sentiment analysis
        sentiment = self.text_analyzer.analyze_sentiment(text)
        self.sentiment_label.setText(
            f"Sentiment: {sentiment['sentiment']} (Confidence: {sentiment['confidence']:.2f})"
        )
        
        # Text summarization
        summary = self.text_analyzer.summarize_text(text)
        self.summary_label.setText(f"Summary: {summary}")