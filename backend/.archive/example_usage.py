"""
Example usage of ResumeCraft API - Quick Start Guide
"""

import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from app.graphs.workflow import (
    parse_resume_only,
    match_candidate_to_job,
    complete_workflow,
)

# Load environment variables
load_dotenv()


# ============================================================================
# SAMPLE DATA
# ============================================================================

SAMPLE_RESUME = """
John Doe
Software Engineer
Email: john.doe@email.com
Phone: (555) 123-4567
Location: San Francisco, CA
LinkedIn: linkedin.com/in/johndoe

PROFESSIONAL SUMMARY
Results-driven Software Engineer with 7+ years of experience building scalable
web applications. Expert in Python, React, and cloud technologies. Proven track
record of leading development teams and delivering high-impact projects.

WORK EXPERIENCE

Senior Software Engineer - TechCorp Inc.
San Francisco, CA | January 2020 - Present
• Led development of microservices architecture serving 10M+ users
• Reduced API response time by 40% through optimization
• Mentored team of 5 junior engineers
• Technologies: Python, Django, React, AWS, Docker, PostgreSQL

Software Engineer - StartupXYZ
Palo Alto, CA | June 2017 - December 2019
• Built RESTful APIs for mobile and web applications
• Implemented CI/CD pipeline reducing deployment time by 60%
• Collaborated with product team to define technical requirements
• Technologies: Python, Flask, JavaScript, MongoDB, Redis

EDUCATION

Bachelor of Science in Computer Science
University of California, Berkeley | Graduated 2017

SKILLS

Technical Skills:
- Languages: Python, JavaScript, TypeScript, Java
- Frameworks: Django, Flask, React, Node.js
- Cloud: AWS (EC2, S3, Lambda), Docker, Kubernetes
- Databases: PostgreSQL, MongoDB, Redis
- Tools: Git, Jenkins, Jira

Soft Skills:
- Team Leadership
- Problem Solving
- Communication
- Agile/Scrum
"""

SAMPLE_JOB_DESCRIPTION = """
Senior Backend Engineer - Python/AWS

We're looking for an experienced Backend Engineer to join our growing team.

Requirements:
• 5+ years of Python development experience
• Strong experience with AWS services (EC2, Lambda, S3)
• Expertise in microservices architecture
• Experience with PostgreSQL and NoSQL databases
• Docker and Kubernetes knowledge
• Strong API design skills
• Team leadership experience preferred

Responsibilities:
• Design and implement scalable backend services
• Optimize application performance
• Mentor junior engineers
• Collaborate with frontend and product teams
• Participate in code reviews and architectural decisions

Nice to have:
• React or frontend experience
• CI/CD pipeline experience
• Experience with Redis or caching strategies
"""


# ============================================================================
# EXAMPLE 1: PARSE RESUME ONLY
# ============================================================================


def example_parse_resume():
    """Example: Parse a resume without job matching"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Parse Resume Only")
    print("="*70 + "\n")

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.0)

    # Parse resume
    result = parse_resume_only(llm, SAMPLE_RESUME)

    # Display results
    if result.get("errors"):
        print("❌ Errors:", result["errors"])
    else:
        parsed = result["parsed_resume"]
        print("✅ Resume parsed successfully!\n")

        print(f"Name: {parsed['personal_info']['full_name']}")
        print(f"Email: {parsed['personal_info']['email']}")
        print(f"Experience: {parsed['summary']['years_experience']} years")
        print(f"Level: {parsed['summary']['experience_level']}")
        print(f"\nTechnical Skills: {', '.join(parsed['skills']['technical'][:5])}...")
        print(f"\nConfidence Score: {result['confidence_scores'].get('parser', 0)}%")


# ============================================================================
# EXAMPLE 2: MATCH CANDIDATE TO JOB
# ============================================================================


def example_match_candidate():
    """Example: Match candidate to job and get recommendation"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Match Candidate to Job")
    print("="*70 + "\n")

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.1)

    # Match candidate to job
    result = match_candidate_to_job(llm, SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION)

    # Display results
    if result.get("errors"):
        print("❌ Errors:", result["errors"])
    else:
        match = result["match_result"]["match_summary"]
        print("✅ Matching completed!\n")

        print(f"Match Score: {match['score']}/100")
        print(f"Match Level: {match['level']}")
        print(f"Recommendation: {match['recommendation']}")

        print("\n📊 Strengths:")
        for strength in result["match_result"]["strengths"][:3]:
            print(f"  ✓ {strength}")

        print("\n⚠️  Gaps:")
        for gap in result["match_result"]["gaps"][:3]:
            print(f"  • {gap['gap']} ({gap['severity']})")

        print(f"\n🎯 Final Recommendation:")
        print(f"  {result['final_recommendation']}")


# ============================================================================
# EXAMPLE 3: COMPLETE WORKFLOW (WITH ENHANCEMENT)
# ============================================================================


def example_complete_workflow():
    """Example: Run complete workflow including enhancement"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Complete Workflow (Parse + Match + Enhance + QA)")
    print("="*70 + "\n")

    # Initialize LLM
    llm = ChatOpenAI(model="gpt-4-turbo-preview", temperature=0.2)

    # Run complete workflow
    print("🔄 Running workflow...")
    result = complete_workflow(llm, SAMPLE_RESUME, SAMPLE_JOB_DESCRIPTION)

    # Display results
    if result.get("errors"):
        print("❌ Errors:", result["errors"])
    else:
        print(f"✅ Workflow completed with status: {result['status']}\n")

        # Parsing
        print("1️⃣  PARSING:")
        print(f"   Confidence: {result['confidence_scores'].get('parser', 0)}%")

        # Matching
        print("\n2️⃣  MATCHING:")
        match_score = result.get('match_score', 0)
        print(f"   Match Score: {match_score}/100")

        # Enhancement
        if result.get('enhanced_resume'):
            enhanced = result['enhanced_resume']
            print("\n3️⃣  ENHANCEMENT:")
            print(f"   ATS Score: {enhanced.get('ats_score', {}).get('before', 0)} → "
                  f"{enhanced.get('ats_score', {}).get('after', 0)}")
            print(f"   Changes: {len(enhanced.get('change_summary', []))}")
            print(f"   Keywords Added: {', '.join(enhanced.get('keywords_added', [])[:5])}...")

        # QA
        if result.get('qa_result'):
            qa = result['qa_result']
            print("\n4️⃣  QUALITY ASSURANCE:")
            print(f"   Status: {qa.get('approval', {}).get('status', 'N/A')}")
            if qa.get('issues'):
                print(f"   Issues Found: {len(qa['issues'])}")

        # Final Recommendation
        print("\n🎯 FINAL RECOMMENDATION:")
        print(f"   {result.get('final_recommendation', 'N/A')}")


# ============================================================================
# MAIN
# ============================================================================


def main():
    """Run all examples"""
    print("\n" + "🚀 " + "="*66 + " 🚀")
    print("  ResumeCraft - Example Usage & Quick Start Guide")
    print("🚀 " + "="*66 + " 🚀")

    # Check if API key is set
    if not os.getenv("OPENAI_API_KEY"):
        print("\n❌ Error: OPENAI_API_KEY not found in environment")
        print("   Please set your OpenAI API key in .env file")
        return

    try:
        # Run examples
        example_parse_resume()
        example_match_candidate()
        example_complete_workflow()

        print("\n" + "="*70)
        print("✅ All examples completed successfully!")
        print("="*70 + "\n")

    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
