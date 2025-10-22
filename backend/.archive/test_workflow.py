"""
Quick test script to verify workflow is working
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.graphs.workflow import match_candidate_to_job

load_dotenv()

# Sample data
RESUME = """
John Doe
Software Engineer
john@email.com

Experience:
- Senior Engineer at TechCorp (2020-Present)
- Python, AWS, Docker
"""

JOB = """
Senior Backend Engineer

Requirements:
- 3+ years Python
- AWS experience
- Docker/Kubernetes
"""

print("Testing workflow...")
print("=" * 50)

try:
    import logging
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.1)

    print(f"\n📝 Resume length: {len(RESUME)} chars")
    print(f"📝 Job length: {len(JOB)} chars")

    result = match_candidate_to_job(llm, RESUME, JOB)

    print(f"\n✅ Result keys: {list(result.keys())}")
    print(f"✅ Has errors: {bool(result.get('errors'))}")
    print(f"✅ Errors: {result.get('errors', [])}")
    print(f"✅ Has match_result: {bool(result.get('match_result'))}")
    print(f"✅ Has parsed_resume: {bool(result.get('parsed_resume'))}")
    print(f"✅ Has analyzed_job: {bool(result.get('analyzed_job'))}")

    if result.get('match_result'):
        print(f"\n🎯 Match Score: {result['match_result'].get('match_summary', {}).get('score', 'N/A')}")

    print("\n" + "=" * 50)
    print("✅ Test completed successfully!")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()
