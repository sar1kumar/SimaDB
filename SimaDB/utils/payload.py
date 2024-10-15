import requests
import json
from faker import Faker
import random

# Initialize Faker
fake = Faker()

# API endpoint
API_URL = "http://4.234.178.24:5000/people/"

# List of possible job roles
job_roles = [
    "Full Stack Developer", "Data Scientist", "Machine Learning Engineer",
    "DevOps Engineer", "Cloud Architect", "UI/UX Designer", "Product Manager",
    "Cybersecurity Analyst", "Blockchain Developer", "IoT Specialist"
]

# List of possible skills
all_skills = [
    "Python", "JavaScript", "Java", "C++", "Ruby", "Go", "Rust", "Swift",
    "Kotlin", "PHP", "TypeScript", "React", "Angular", "Vue.js", "Node.js",
    "Django", "Flask", "Spring Boot", "Express.js", "TensorFlow", "PyTorch",
    "Scikit-learn", "Pandas", "NumPy", "Docker", "Kubernetes", "AWS", "Azure",
    "GCP", "Git", "CI/CD", "Jenkins", "Ansible", "Terraform", "MongoDB", "PostgreSQL",
    "MySQL", "Redis", "Elasticsearch", "GraphQL", "REST API", "Microservices",
    "Agile", "Scrum", "Kanban", "JIRA", "Confluence", "Figma", "Sketch", "Adobe XD"
]

# List of possible projects
all_projects = [
    "E-commerce platform", "Social media app", "Inventory management system",
    "Customer relationship management (CRM) software", "Content management system (CMS)",
    "Real-time chat application", "Task management tool", "Booking and reservation system",
    "Financial portfolio tracker", "Fitness and health monitoring app",
    "Machine learning-based recommendation engine", "Blockchain-based supply chain system",
    "IoT home automation platform", "Augmented reality (AR) mobile game",
    "Natural language processing chatbot", "Cybersecurity threat detection system",
    "Cloud-based data analytics platform", "Video streaming service",
    "Online learning management system (LMS)", "Peer-to-peer file sharing application"
]

def generate_person():
    first_name = fake.first_name()
    last_name = fake.last_name()
    company = fake.company()
    job_role = random.choice(job_roles)
    
    person = {
        "id": f"person_{fake.unique.random_number(digits=6)}",
        "first_name": first_name,
        "last_name": last_name,
        "company": company,
        "job_role": job_role,
        "phone_number": fake.phone_number(),
        "email": f"{first_name.lower()}.{last_name.lower()}@{fake.domain_name()}",
        "address": fake.address().replace('\n', ', '),
        "experience": f"{random.randint(1, 20)} years in {job_role.lower()}, specializing in {fake.bs()}",
        "projects": random.sample(all_projects, k=random.randint(2, 5)),
        "skills": random.sample(all_skills, k=random.randint(5, 10))
    }
    
    return person

def post_person(person):
    try:
        response = requests.post(API_URL, json=person)
        response.raise_for_status()
        print(f"Successfully added person: {person['id']}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to add person {person['id']}: {e}")

# Generate and post 1000 people
for _ in range(100):
    person = generate_person()
    post_person(person)

print("Finished adding 1000 people to the database.")