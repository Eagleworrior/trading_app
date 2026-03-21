import random

TOPICS = [
    "blockchain", "AI", "machine learning", "cloud computing", "cybersecurity",
    "data science", "cryptocurrency", "mobile apps", "APIs", "databases",
    "networking", "web development", "smart contracts", "trading algorithms",
    "market analysis", "deep learning", "neural networks", "IoT devices",
    "quantum computing", "virtual reality", "augmented reality", "5G networks",
    "encryption", "firewalls", "ethical hacking", "penetration testing",
    "data mining", "big data", "robotics", "automation", "edge computing"
]

QUESTION_TEMPLATES = [
    "What is {}?",
    "How does {} work?",
    "Why is {} important?",
    "Which option best explains {}?",
    "What is an example of {}?",
    "What happens when {} is used?",
    "Which statement about {} is true?",
    "What is the purpose of {}?",
    "What is the main benefit of {}?",
    "Which choice correctly describes {}?"
]

def get_questions_for_level(level):
    questions = []

    for i in range(30):
        topic = random.choice(TOPICS)
        template = random.choice(QUESTION_TEMPLATES)
        question_text = template.format(topic)

        options = [
            f"A correct explanation of {topic}",
            f"A wrong explanation of {topic}",
            f"Another wrong explanation of {topic}"
        ]

        questions.append((question_text, options))

    random.shuffle(questions)
    return questions

