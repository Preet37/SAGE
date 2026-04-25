import os
import requests

def generate_design():
    api_key = os.getenv("STITCH_API_KEY")
    if not api_key:
        print("Please set STITCH_API_KEY in your environment.")
        return

    # Note: Replace this with the actual Stitch API endpoint
    endpoint = "https://api.stitch.dev/v1/generate"
    
    prompt = """
    Create a highly professional dashboard for a platform called SAGE (Socratic Agent for Guided Education).
    The UI needs a 3-column layout:
    1. Left Column: A live streaming 'Tutor Chat' (chat interface with message bubbles).
    2. Middle Column: A dynamic 'Concept Map' area (placeholder for an Obsidian-style network graph).
    3. Right Column: A 'Notes / PDF' area where user PDFs are displayed alongside AI-generated summaries.
    
    Aesthetics:
    - Glassmorphism effects
    - Soft, academic color palette (deep blues, off-whites, subtle gold accents)
    - Dark mode by default
    """
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompt": prompt,
        "framework": "nextjs",
        "styling": "tailwind"
    }
    
    try:
        response = requests.post(endpoint, json=data, headers=headers)
        if response.status_code == 200:
            print("Design generated successfully!")
            print("Response:", response.json())
        else:
            print(f"Failed to generate design: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"Error calling Stitch API: {e}")

if __name__ == "__main__":
    generate_design()
