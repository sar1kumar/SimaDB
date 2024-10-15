import json

# Example JSON input
json_data = {
    "data": None,
    "documents": [
        "15 AGI Common Sense",
        "15 AGI Common Sense",
        "MD with commonsense AGI Common Sense",
        "7 years in data science, focus on predictive modeling and data visualization Customer churn prediction model Real-time data dashboard Python R SQL Tableau Scikit-learn",
        "12 years in cloud computing and distributed systems Serverless microservices architecture Multi-cloud deployment strategy AWS Azure Kubernetes Docker Terraform",
        "10 years in software development, specializing in AI and machine learning AI-powered recommendation system Natural language processing chatbot Python Machine Learning NLP TensorFlow PyTorch",
        "6 years in machine learning and computer vision Facial recognition system Autonomous driving object detection Python TensorFlow OpenCV CUDA Deep Learning",
        "8 years in network security and threat detection Intrusion detection system Security information and event management (SIEM) implementation Network Security Penetration Testing Python Wireshark Splunk",
        "5 years in IoT development and embedded systems Smart home energy management system Industrial IoT monitoring platform C++ Python MQTT Raspberry Pi Arduino",
        "4 years in blockchain development and smart contracts Decentralized finance (DeFi) platform Non-fungible token (NFT) marketplace Solidity Ethereum Web3.js Smart Contracts JavaScript",
        "7 years in data visualization and business intelligence Interactive COVID-19 dashboard Real-time sales performance visualizations D3.js Tableau Power BI SQL R",
        "6 years in full stack development, focusing on educational technology Adaptive learning platform Online collaborative coding environment JavaScript React Node.js MongoDB GraphQL"
    ],
    "metadatas": [
        {
            "address": "Manhattan",
            "company": "One Corp",
            "email": "sharva@onecorp.com",
            "first_name": "Saravan",
            "job_role": "MD",
            "last_name": "Kumar",
            "phone_number": "0070070079"
        },
        {
            "address": "Manhattan",
            "company": "One Corp",
            "email": "sharva@onecorp.com",
            "first_name": "Saravan",
            "job_role": "MD",
            "last_name": "Kumar",
            "phone_number": "0070070079"
        },
        {
            "address": "Manhattan",
            "company": "One Corp",
            "email": "sharva@onecorp.com",
            "first_name": "Saravan",
            "job_role": "MD",
            "last_name": "Kumar",
            "phone_number": "0070070079"
        },
        {
            "address": "456 Oak Ave, New York, NY",
            "company": "Data Wizards",
            "email": "jane.smith@datawizards.com",
            "first_name": "Jane",
            "job_role": "Data Scientist",
            "last_name": "Smith",
            "phone_number": "9876543210"
        },
        {
            "address": "789 Pine St, Seattle, WA",
            "company": "Cloud Solutions Inc.",
            "email": "mike.johnson@cloudsolutions.com",
            "first_name": "Mike",
            "job_role": "Cloud Architect",
            "last_name": "Johnson",
            "phone_number": "5551234567"
        },
        {
            "address": "123 Main St, San Francisco, CA",
            "company": "Tech Innovators",
            "email": "john.doe@techinnovators.com",
            "first_name": "John",
            "job_role": "Senior Software Engineer",
            "last_name": "Doe",
            "phone_number": "1234567890"
        },
        {
            "address": "101 Tech Blvd, Boston, MA",
            "company": "AI Innovations Ltd.",
            "email": "emily.chen@aiinnovations.com",
            "first_name": "Emily",
            "job_role": "Machine Learning Engineer",
            "last_name": "Chen",
            "phone_number": "3331234567"
        },
        {
            "address": "202 Firewall St, Austin, TX",
            "company": "SecureNet Systems",
            "email": "alex.rodriguez@securenet.com",
            "first_name": "Alex",
            "job_role": "Cybersecurity Analyst",
            "last_name": "Rodriguez",
            "phone_number": "7778889999"
        },
        {
            "address": "303 Solar Lane, Portland, OR",
            "company": "Green Energy Solutions",
            "email": "sarah.thompson@greenenergy.com",
            "first_name": "Sarah",
            "job_role": "IoT Developer",
            "last_name": "Thompson",
            "phone_number": "4445556666"
        },
        {
            "address": "404 Crypto Ave, Miami, FL",
            "company": "FinTech Innovations",
            "email": "david.kim@fintechinno.com",
            "first_name": "David",
            "job_role": "Blockchain Developer",
            "last_name": "Kim",
            "phone_number": "9990001111"
        },
        {
            "address": "505 Chart St, Chicago, IL",
            "company": "DataViz Pro",
            "email": "olivia.brown@datavizpro.com",
            "first_name": "Olivia",
            "job_role": "Data Visualization Specialist",
            "last_name": "Brown",
            "phone_number": "2223334444"
        },
        {
            "address": "707 Learning Lane, Toronto, ON",
            "company": "EduTech Solutions",
            "email": "lisa.wong@edutech.com",
            "first_name": "Lisa",
            "job_role": "Full Stack Developer",
            "last_name": "Wong",
            "phone_number": "1112223333"
        }
    ]
}

# Creating the transformed structure
transformed_data = []

for i in range(len(json_data['documents'])):
    person_data = {
        "person_id": f"person_{str(i+1).zfill(3)}",
        "Description": json_data['documents'][i],
        "address": json_data['metadatas'][i]["address"],
        "company": json_data['metadatas'][i]["company"],
        "email": json_data['metadatas'][i]["email"],
        "first_name": json_data['metadatas'][i]["first_name"],
        "job_role": json_data['metadatas'][i]["job_role"],
        "last_name": json_data['metadatas'][i]["last_name"],
        "phone_number": json_data['metadatas'][i]["phone_number"]
    }
    transformed_data.append(person_data)

# Output the transformed data
print(json.dumps(transformed_data, indent=4))

# Transform the data