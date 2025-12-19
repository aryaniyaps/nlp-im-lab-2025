"""
Mini-Project Title - Regex-Based Text Analyser and Information Extractor 

 

Problem Statement 

In real-world NLP applications, raw text often contains unstructured information such as emails, phone numbers, dates, URLs, extra spaces, and repeated words. Before applying advanced NLP models, this data must be cleaned and structured. The objective of this mini-project is to design and implement a Python-based text analyzer using Regular Expressions that can automatically clean text and extract key information from it. 

 

Functional Requirements 

The system should: 

    Accept a paragraph of text from the user 

    Remove extra spaces and unwanted symbols 

    Extract email IDs 

    Extract mobile numbers 

    Extract dates in DD/MM/YYYY format 

    Extract URLs 

    Detect repeated consecutive words 

    Mask email usernames for privacy 

 

Output Display Format: S

 

ANALYSIS REPORT 

Cleaned Text: 

Emails Found: 

Masked Emails: 

Mobile Numbers: 

Dates: 

URLs: 

Repeated Words: 
"""

import re

def analyze_text(text):
    print("ANALYSIS REPORT\n")
    cleaned_text = re.sub(r"\s+", " ", text.strip())
    print("Cleaned Text:", cleaned_text)

    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", cleaned_text)
    print("Emails Found:", emails)

    masked_emails = [re.sub(r"([a-zA-Z0-9._%+-]+)@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", r"****@****.com", email) for email in emails]
    print("Masked Emails:", masked_emails)

    mobile_numbers = re.findall(r"\b\d{10}\b", cleaned_text)
    print("Mobile Numbers:", mobile_numbers)

    dates = re.findall(r"\b\d{2}/\d{2}/\d{4}\b", cleaned_text)
    print("Dates:", dates)

    urls = re.findall(r"https?://[A-Za-z0-9./]+", cleaned_text)
    print("URLs:", urls)

    repeated_words = re.findall(r"\b(\w+)\s+\1\b", cleaned_text)
    print("Repeated Words:", repeated_words)


if __name__ == "__main__":
    input_text = input("Please enter text for RegEx analysis:")
    analyze_text(input_text)