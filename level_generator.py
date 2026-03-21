import json, random, os

TOPICS = {
    "general": [
        ("What is the capital of France?", ["Paris","Rome","Berlin"], "Paris"),
        ("Which planet is known as the Red Planet?", ["Mars","Venus","Jupiter"], "Mars"),
        ("Who wrote 'Hamlet'?", ["Shakespeare","Dickens","Homer"], "Shakespeare"),
        ("What is the largest ocean?", ["Pacific","Atlantic","Indian"], "Pacific"),
        ("What gas do plants breathe in?", ["Carbon Dioxide","Oxygen","Nitrogen"], "Carbon Dioxide"),
        ("Which continent is Egypt in?", ["Africa","Asia","Europe"], "Africa"),
        ("What is H2O?", ["Water","Salt","Oxygen"], "Water"),
        ("How many days are in a leap year?", ["366","365","364"], "366"),
        ("What is the tallest mountain?", ["Everest","K2","Kilimanjaro"], "Everest"),
        ("What is the fastest land animal?", ["Cheetah","Lion","Horse"], "Cheetah"),
        ("What is the largest desert?", ["Sahara","Gobi","Kalahari"], "Sahara"),
        ("What is the boiling point of water?", ["100°C","90°C","80°C"], "100°C"),
        ("Which animal is known as the King of the Jungle?", ["Lion","Tiger","Elephant"], "Lion"),
        ("What is the capital of Japan?", ["Tokyo","Osaka","Kyoto"], "Tokyo"),
        ("What is the currency of the USA?", ["Dollar","Euro","Pound"], "Dollar"),
        ("Which organ pumps blood?", ["Heart","Lungs","Kidneys"], "Heart"),
        ("What is the largest mammal?", ["Blue Whale","Elephant","Giraffe"], "Blue Whale"),
        ("Which metal is liquid at room temp?", ["Mercury","Iron","Gold"], "Mercury"),
        ("What is the square root of 81?", ["9","8","7"], "9"),
        ("Which planet has rings?", ["Saturn","Mars","Earth"], "Saturn"),
        ("What is the capital of Kenya?", ["Nairobi","Mombasa","Kisumu"], "Nairobi"),
        ("Which bird cannot fly?", ["Ostrich","Eagle","Parrot"], "Ostrich"),
        ("What is the largest country?", ["Russia","China","USA"], "Russia"),
        ("What is the smallest prime number?", ["2","1","3"], "2"),
        ("What is the freezing point of water?", ["0°C","10°C","-10°C"], "0°C"),
        ("Which animal gives us wool?", ["Sheep","Cow","Goat"], "Sheep"),
        ("What is the capital of UK?", ["London","Manchester","Liverpool"], "London"),
        ("What is the longest river?", ["Nile","Amazon","Yangtze"], "Nile"),
        ("Which gas do humans breathe?", ["Oxygen","Carbon Dioxide","Nitrogen"], "Oxygen"),
        ("What is the largest continent?", ["Asia","Africa","Europe"], "Asia")
    ]
}

def generate_level(level_number):
    topic = "general"
    questions = []

    for q in random.sample(TOPICS[topic], 30):
        questions.append({
            "question": q[0],
            "options": q[1],
            "answer": q[2]
        })

    data = {
        "title": f"Level {level_number} - {topic.title()}",
        "theme": random.randint(1, 5),
        "questions": questions
    }

    os.makedirs("surveys", exist_ok=True)
    filename = f"surveys/level{level_number}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return filename

