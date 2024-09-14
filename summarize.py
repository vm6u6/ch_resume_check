from faker import Faker
import json
fake = Faker()

def summarize_resume(resume_text):
    sections = {
        "Employment History": "",
        "Skills": "",
        "Education": "",
        "Certifications": ""
    }

    prompts = {
        "Employment History": "Summarize the employment history from the following resume: ",
        "Skills": "List the skills mentioned in the following resume: ",
        "Education": "Summarize the education details from the following resume: ",
        "Certifications": "List any certifications mentioned in the following resume: "
    }

    for section, prompt in prompts.items():
        input_text = prompt + resume_text
        summary = generate(input_text)
        sections[section] = summary

    sections["Name"] = fake.name()
    return sections

def process_resumes_from_json(json_file_path, summarized_json_file_path):
    with open(json_file_path, "r", encoding="utf-8") as json_file:
        resumes = json.load(json_file)

    summarized_resumes = {}

    for filename, resume_text in resumes.items():
        summarized_resumes[filename] = summarize_resume(resume_text)
        print(f"Summarized {filename}")

    with open(summarized_json_file_path, "w", encoding="utf-8") as output_json_file:
        json.dump(summarized_resumes, output_json_file, indent=4, ensure_ascii=False)
    print(f"All resumes summarized and saved to {summarized_json_file_path}")