import requests

BASE_URL = "https://summarizer-agent-vpmw.onrender.com"

def test_health():
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check:", response.json())

def test_summarize(text):
    response = requests.post(
        f"{BASE_URL}/summarize",
        json={"text": text}
    )
    result = response.json()
    print("\n📝 Original text word count:", len(text.split()))
    print("✅ Summary:", result["summary"])
    print("📊 Status:", result["status"])

# Run tests
test_health()

test_summarize("""
Artificial intelligence is transforming industries worldwide. 
Machine learning algorithms can now process vast amounts of data 
in seconds, enabling breakthroughs in medicine, climate science, 
and transportation. However, ethical considerations around bias, 
privacy, and job displacement remain critical challenges that 
society must address as AI adoption accelerates.
""")

test_summarize("""
Climate change is one of the most pressing issues of our time.
Rising global temperatures are causing more frequent extreme weather
events, melting polar ice caps, and threatening biodiversity.
Scientists warn that without significant reductions in greenhouse
gas emissions, the consequences could be catastrophic and irreversible.
""")