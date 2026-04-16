from chains.extraction_chain import extraction_chain
from chains.matching_chain import matching_chain
from chains.scoring_chain import scoring_chain
from chains.explanation_chain import explanation_chain
import json
import os


# Better file reader (robust)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def read_file(filename):
    path = os.path.join(BASE_DIR, "files", filename)
    with open(path, "r", encoding="utf-8") as file:
        return file.read()


job_description = read_file("job_description.txt")
strong_resume = read_file("strong_resume.txt")
average_resume = read_file("average_resume.txt")
weak_resume = read_file("weak_resume.txt")


# Helper to clean LLM output
def parse_json(response):
    content = response.content  # extract text from AIMessage

    # Remove markdown if present
    content = content.strip().replace("```json", "").replace("```", "")

    return json.loads(content)


def run_pipeline(resume):
    # Step 1: Extraction
    extracted = extraction_chain.invoke({"resume": resume})
    extracted_dict = parse_json(extracted)

    # Step 2: Matching
    matching = matching_chain.invoke({
        "extracted_resume": extracted_dict,
        "job_description": job_description
    })
    matching_dict = parse_json(matching)

    # Step 3: Scoring
    score = scoring_chain.invoke({
        "matching_data": matching_dict
    })
    score_dict = parse_json(score)

    # Step 4: Explanation
    explanation = explanation_chain.invoke({
        "matching_data": matching_dict,
        "match_score": score_dict["match_score"]
    })
    explanation_dict = parse_json(explanation)

    return {
        "extracted": extracted_dict,
        "matching": matching_dict,
        "score": score_dict,
        "explanation": explanation_dict
    }

# function to clean json output and represent the final output clearly

def print_result(label, result):
    print(f"\n{'='*50}")
    print(f"{label} Candidate")
    print(f"{'='*50}")

    # Score
    print(f"\nScore: {round(result['score']['match_score'], 2)}")

    # Skills
    print("\nSkills:")
    print(f"  Matched: {', '.join(result['matching']['matched_skills']) or 'None'}")
    print(f"  Missing: {', '.join(result['matching']['missing_skills']) or 'None'}")

    # Tools
    print("\nTools:")
    print(f"  Matched: {', '.join(result['matching']['matched_tools']) or 'None'}")
    print(f"  Missing: {', '.join(result['matching']['missing_tools']) or 'None'}")

    # Experience
    print(f"\nExperience Match: {result['matching']['experience_match']}")

    # Explanation
    print("\nExplanation:")
    print(result['explanation']['explanation'])

    print("\n" + "="*50)

if __name__ == "__main__":
    print("Program testing starts!\n")

    resumes = {
        "Strong": strong_resume,
        "Average": average_resume,
        "Weak": weak_resume
    }

    for label, resume in resumes.items():
        result = run_pipeline(resume)
        print_result(label,result)