from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

class NoteGenerator:
    @staticmethod
    def generate_summary(text: str, sentences_count: int = 3) -> str:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count)
        
        return " ".join(str(sentence) for sentence in summary)