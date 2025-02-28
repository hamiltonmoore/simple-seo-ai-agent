import requests
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import re

# Fake keyword database (replace with real SEO tools later)
SAMPLE_KEYWORDS = {
    "best running shoes": {"volume": 5000, "difficulty": 80},
    "affordable trail shoes": {"volume": 1200, "difficulty": 40},
    "running gear reviews": {"volume": 800, "difficulty": 50}
}

class SEOAgent:
    def __init__(self, url):
        self.url = url
        self.report = {"issues": [], "suggestions": [], "stats": {}}
    
    # THINK PHASE: Gather and analyze data
    def crawl_site(self):
        """Fetch and parse the webpage content."""
        try:
            response = requests.get(self.url, timeout=5)
            response.raise_for_status()  # Raise error if request fails
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract key elements
            self.title = soup.title.string if soup.title else "No title"
            self.meta_desc = soup.find('meta', attrs={'name': 'description'})
            self.meta_desc = self.meta_desc['content'] if self.meta_desc else "No meta description"
            self.content = soup.get_text(separator=' ')
            self.headings = [h.text for h in soup.find_all(['h1', 'h2', 'h3'])]
            self.word_count = len(self.content.split())
            
            self.report["stats"]["word_count"] = self.word_count
            self.report["stats"]["title"] = self.title
            self.report["stats"]["meta_desc"] = self.meta_desc
        except Exception as e:
            self.report["issues"].append(f"Failed to crawl site: {str(e)}")
    
    def analyze_content(self):
        """Analyze text for keywords and readability."""
        # Tokenize and clean content
        tokens = word_tokenize(self.content.lower())
        stop_words = set(stopwords.words('english'))
        clean_tokens = [w for w in tokens if w.isalpha() and w not in stop_words]
        
        # Count frequent words (potential keywords)
        word_freq = Counter(clean_tokens).most_common(5)
        self.report["stats"]["top_words"] = word_freq
        
        # Check title and meta description length
        if len(self.title) > 60:
            self.report["issues"].append("Title too long (over 60 chars)")
        if len(self.meta_desc) > 160:
            self.report["issues"].append("Meta description too long (over 160 chars)")
        if self.word_count < 300:
            self.report["issues"].append("Content too short (under 300 words)")
    
    # DO PHASE: Make suggestions
    def suggest_improvements(self):
        """Suggest SEO optimizations based on analysis."""
        # Keyword suggestions from sample database
        for keyword, data in SAMPLE_KEYWORDS.items():
            if keyword.lower() not in self.content.lower():
                self.report["suggestions"].append(
                    f"Add keyword '{keyword}' (Volume: {data['volume']}, Difficulty: {data['difficulty']})"
                )
        
        # Heading suggestions
        if not self.headings:
            self.report["suggestions"].append("Add at least one H1 heading")
        
        # Content length suggestion
        if self.word_count < 500:
            self.report["suggestions"].append(f"Expand content to 500+ words (currently {self.word_count})")
    
    # REPORT PHASE: Present findings
    def generate_report(self):
        """Compile and display the SEO report."""
        print(f"SEO Report for {self.url}")
        print("\nStats:")
        for key, value in self.report["stats"].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print("\nIssues:")
        for issue in self.report["issues"] or ["None found"]:
            print(f"  - {issue}")
        print("\nSuggestions:")
        for suggestion in self.report["suggestions"] or ["None found"]:
            print(f"  - {suggestion}")
    
    # Main execution flow
    def run(self):
        """Run the full agent process."""
        print("Starting SEO analysis...")
        self.crawl_site()       # Think
        self.analyze_content()  # Think
        self.suggest_improvements()  # Do
        self.generate_report()  # Report
        print("Analysis complete!")

# Example usage
if __name__ == "__main__":
    # Replace with any public URL you want to test
    site_url = "https://www.python.org"  # A simple placeholder site
    agent = SEOAgent(site_url)
    agent.run()