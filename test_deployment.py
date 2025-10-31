#!/usr/bin/env python3
"""
Test script for deployed ResumeCraft LangGraph workflow on LangSmith Cloud
"""

import requests
import json
import os
import sys

# Your deployment details
DEPLOYMENT_ID = "028c1a44-1085-4888-b504-b5e0dbd1a949"
DEPLOYMENT_URL = f"https://api.smith.langchain.com/deployments/{DEPLOYMENT_ID}"

# Get API key from environment or prompt
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")

if not LANGSMITH_API_KEY:
    print("❌ Error: LANGSMITH_API_KEY not found in environment")
    print("\nPlease set your API key:")
    print("  export LANGSMITH_API_KEY='lsv2_pt_your_key_here'")
    print("\nGet your API key from: https://smith.langchain.com/settings")
    sys.exit(1)


def test_workflow(resume_text, job_description):
    """Test the deployed ResumeCraft workflow"""

    print("🚀 Testing deployed ResumeCraft workflow...")
    print(f"📍 Deployment URL: {DEPLOYMENT_URL}")
    print()

    headers = {
        "Authorization": f"Bearer {LANGSMITH_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "input": {
            "resume_text": resume_text,
            "job_description": job_description
        }
    }

    try:
        print("⏳ Sending request...")
        response = requests.post(
            f"{DEPLOYMENT_URL}/invoke",
            headers=headers,
            json=payload,
            timeout=120  # 2 minutes timeout
        )

        print(f"📡 Response status: {response.status_code}")
        print()

        if response.status_code == 200:
            result = response.json()
            print("✅ Success! Workflow executed successfully")
            print()
            print("=" * 80)
            print("RESULTS")
            print("=" * 80)
            print()

            # Parse and display results
            output = result.get("output", {})

            # Status
            status = output.get("status", "unknown")
            print(f"Status: {status}")
            print()

            # Match Score
            match_score = output.get("match_score")
            if match_score is not None:
                print(f"🎯 Match Score: {match_score}/100")
                print()

            # Parsed Resume
            parsed_resume = output.get("parsed_resume")
            if parsed_resume:
                print("📄 Parsed Resume:")
                print(f"  Name: {parsed_resume.get('name', 'N/A')}")
                print(f"  Email: {parsed_resume.get('email', 'N/A')}")
                print(f"  Skills: {', '.join(parsed_resume.get('skills', []))}")
                print()

            # Analyzed Job
            analyzed_job = output.get("analyzed_job")
            if analyzed_job:
                print("💼 Job Analysis:")
                print(f"  Title: {analyzed_job.get('title', 'N/A')}")
                required_skills = analyzed_job.get('required_skills', [])
                if required_skills:
                    print(f"  Required Skills: {', '.join(required_skills)}")
                print()

            # Match Result
            match_result = output.get("match_result")
            if match_result:
                print("🔍 Match Details:")
                matching = match_result.get('matching_skills', [])
                missing = match_result.get('missing_skills', [])
                if matching:
                    print(f"  ✅ Matching Skills: {', '.join(matching)}")
                if missing:
                    print(f"  ❌ Missing Skills: {', '.join(missing)}")
                print()

            # Final Recommendation
            recommendation = output.get("final_recommendation")
            if recommendation:
                print("📋 Final Recommendation:")
                print(f"  {recommendation}")
                print()

            # Full JSON (optional)
            print()
            print("=" * 80)
            print("FULL RESPONSE (JSON)")
            print("=" * 80)
            print(json.dumps(result, indent=2))

            return result

        else:
            print(f"❌ Error: {response.status_code}")
            print()
            print("Response:")
            print(response.text)
            return None

    except requests.exceptions.Timeout:
        print("❌ Error: Request timed out after 120 seconds")
        print("The workflow might be taking longer than expected.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Error: Request failed")
        print(f"   {str(e)}")
        return None
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        return None


def main():
    """Run test cases"""

    print()
    print("=" * 80)
    print("ResumeCraft Deployment Test")
    print("=" * 80)
    print()

    # Test Case 1: Good match
    print("TEST CASE 1: Strong Match")
    print("-" * 80)

    resume1 = """
John Doe
Software Engineer
john.doe@email.com

EXPERIENCE:
Senior Python Developer at Tech Corp (2020-2024)
- Built scalable web applications using Django and Flask
- Managed PostgreSQL databases with complex queries
- Deployed applications on AWS using Docker and Kubernetes
- Led team of 3 developers

Python Developer at StartupXYZ (2018-2020)
- Developed REST APIs using FastAPI
- Implemented CI/CD pipelines
- Redis caching and optimization

SKILLS:
Python, Django, Flask, FastAPI, PostgreSQL, Redis, Docker, Kubernetes, AWS, Git

EDUCATION:
BS Computer Science, State University (2018)
"""

    job1 = """
Senior Python Developer

We are looking for an experienced Python developer to join our backend team.

REQUIREMENTS:
- 5+ years of Python development experience
- Strong experience with Django or Flask
- Database design and optimization (PostgreSQL preferred)
- Cloud deployment experience (AWS, GCP, or Azure)
- Docker and containerization
- Team leadership experience

NICE TO HAVE:
- Kubernetes experience
- Redis caching
- FastAPI knowledge
"""

    result1 = test_workflow(resume1, job1)

    if result1:
        print()
        print("✅ Test Case 1 completed successfully!")
    else:
        print()
        print("❌ Test Case 1 failed")

    print()
    print("=" * 80)
    print()

    # Uncomment for more test cases
    """
    # Test Case 2: Weak match
    print("TEST CASE 2: Weak Match")
    print("-" * 80)

    resume2 = "Jane Smith\nFrontend Developer\n3 years React experience"
    job2 = "Looking for Senior Backend Python Developer with 10 years experience"

    result2 = test_workflow(resume2, job2)

    if result2:
        print()
        print("✅ Test Case 2 completed successfully!")
    else:
        print()
        print("❌ Test Case 2 failed")
    """


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print()
        print()
        print("⚠️  Test interrupted by user")
        sys.exit(0)
