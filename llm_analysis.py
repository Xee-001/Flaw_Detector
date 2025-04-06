import json
import subprocess
import requests


def analyze_website_with_mistral(website_data):
    """Send website analysis data to Mistral 7B for flaw detection and recommendations."""

    # Convert data to readable text
    input_text = f"""
    Analyze the following website data and suggest improvements:

    Title: {website_data.get("title", "N/A")}
    Meta Description: {website_data.get("meta_description", "N/A")}
    Broken Links: {len(website_data.get("broken_links", []))} found
    Performance Score: {website_data.get("performance_score", "N/A")}
    Accessibility Score: {website_data.get("accessibility_score", "N/A")}
    SEO Score: {website_data.get("seo_score", "N/A")}

    Provide clear recommendations.
    """

    # Run Mistral locally with Ollama
    try:
        response = subprocess.run(
            ["ollama", "run", "mistral", input_text],
            capture_output=True, text=True, timeout=200
        )
        return response.stdout.strip()

    except subprocess.TimeoutExpired:
        return "LLM processing timed out."


# Example usage
if __name__ == "__main__":
    # Simulated data (replace with real output from previous steps)
    website_data = {
        "title": "Test Website",
        "meta_description": "A sample website",
        "broken_links": ["https://broken-link.com"],
        "performance_score": 75,
        "accessibility_score": 60,
        "seo_score": 80
    }

    print(analyze_website_with_mistral(website_data))
