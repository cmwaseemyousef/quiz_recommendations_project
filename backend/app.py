from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import os

import pandas as pd  # Ensure this is included for handling CSV files

# Generate the sample CSV file
def create_sample_csv():
    data = {
        "Topic": ["Algebra", "Biology", "Physics", "Geometry", "Algebra", "Physics", "Biology", "Geometry"],
        "Correct": [1, 0, 1, 0, 1, 1, 0, 1],
    }
    df = pd.DataFrame(data)
    df.to_csv("quiz_data.csv", index=False)

# Call the function to create the file
create_sample_csv()


import pandas as pd

# Generate the sample CSV file
def create_sample_csv():
    data = {
        "Topic": ["Algebra", "Biology", "Physics", "Geometry", "Algebra", "Physics", "Biology", "Geometry"],
        "Correct": [1, 0, 1, 0, 1, 1, 0, 1],
    }
    df = pd.DataFrame(data)
    df.to_csv("quiz_data.csv", index=False)

# Call the function to create the file
create_sample_csv()

app = Flask(__name__, template_folder="../frontend", static_folder="../frontend/static")


@app.route("/", methods=["GET", "POST"])
def home():
    recommendations = []
    chart = None
    insights = None  # Initialize insights to avoid UnboundLocalError


    if request.method == "POST":
        # Save the uploaded file
        file = request.files["file"]
        if file:
            file_path = os.path.join("uploads", file.filename)
            os.makedirs("uploads", exist_ok=True)
            file.save(file_path)

            # Process the uploaded file
            quiz_data = pd.read_csv(file_path)
            recommendations, chart = process_quiz_data(quiz_data)
            insights = generate_detailed_insights(quiz_data)


    return render_template("index.html", recommendations=recommendations, chart=chart, insights=insights)


def process_quiz_data(quiz_data):
    # Example processing: Calculate accuracy by topic
    topic_accuracy = quiz_data.groupby("Topic")["Correct"].mean() * 100

    # Generate the chart
    chart_path = generate_chart(topic_accuracy)

    # Generate recommendations
    recommendations = [
        {"topic": topic, "tip": f"Focus more on {topic} to improve accuracy."}
        for topic, accuracy in topic_accuracy.items() if accuracy < 70
    ]

    return recommendations, chart_path

def generate_detailed_insights(quiz_data):
    # Calculate accuracy by topic
    topic_accuracy = quiz_data.groupby("Topic")["Correct"].mean() * 100

    # Classify topics into strong and weak areas
    insights = {
        "strong_topics": [topic for topic, accuracy in topic_accuracy.items() if accuracy >= 70],
        "weak_topics": [topic for topic, accuracy in topic_accuracy.items() if accuracy < 70],
    }

    return insights


def generate_chart(data):
    topics = data.index
    accuracy = data.values

    # Create the bar chart
    plt.figure(figsize=(8, 5))
    plt.bar(topics, accuracy, color="skyblue")
    plt.title("Quiz Performance by Topic")
    plt.xlabel("Topics")
    plt.ylabel("Accuracy (%)")
    plt.ylim(0, 100)

    # Save the chart
    chart_path = "../frontend/static/chart.png"
    os.makedirs(os.path.dirname(chart_path), exist_ok=True)
    plt.savefig(chart_path)
    plt.close()

    return "static/chart.png"

if __name__ == "__main__":
    app.run(debug=True)
