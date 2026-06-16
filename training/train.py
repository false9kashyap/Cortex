import pandas as pd
import joblib
import os
import re

from sentence_transformers import SentenceTransformer

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report



# ======================
# Load Data
# ======================

df = pd.read_csv(
    "NewResumeDataset.csv"
)


df = df.dropna(
    subset=[
        "Resume",
        "Category"
    ]
)



# ======================
# Category cleanup
# ======================

category_map = {


    # ==================
    # SOFTWARE
    # ==================

    "Software Developer": "Software Engineer",
    "Python Developer": "Software Engineer",
    "Java Developer": "Software Engineer",
    "Web Developer": "Software Engineer",
    "DotNet Developer": "Software Engineer",
    "Database Administrator": "Software Engineer",
    "Database": "Software Engineer",
    "ETL Developer": "Software Engineer",
    "Testing": "Software Engineer",
    "Automation Testing": "Software Engineer",
    "SAP Developer": "Software Engineer",
    "Blockchain": "Software Engineer",
    "Web Designing": "Software Engineer",
    "Information Technology": "Software Engineer",


    # ==================
    # DATA
    # ==================

    "Data Science": "Data Scientist",
    "Hadoop": "Data Scientist",


    # ==================
    # SECURITY
    # ==================

    "Security Analyst": "Cyber Security Engineer",
    "Network Security Engineer": "Cyber Security Engineer",
    "Network Administrator": "Cyber Security Engineer",
    "Systems Administrator": "Cyber Security Engineer",


    # ==================
    # ENGINEERING
    # ==================

    "Electrical Engineering": "Electronics Engineer",
    "Engineering": "Electronics Engineer",

    "Automobile": "Mechanical Engineer",
    "Civil Engineer": "Mechanical Engineer",


    # ==================
    # BUSINESS
    # ==================

    "Business Development": "Business",
    "Business Analyst": "Business",
    "Operations Manager": "Business",
    "Project manager": "Business",
    "PMO": "Business",
    "Consultant": "Business",


    # ==================
    # CREATIVE
    # ==================

    "Designer": "Creative",
    "Arts": "Creative",
    "Digital Media": "Creative",
    "Apparel": "Creative",


    # ==================
    # HEALTH
    # ==================

    "Healthcare": "Healthcare",
    "Health and fitness": "Healthcare",
    "Fitness": "Healthcare",


    # ==================
    # OTHER
    # ==================

    "Teacher": "Education",
    "Advocate": "Legal",
    "Accountant": "Finance",
    "Banking": "Finance"
}


df["Category"] = (
    df["Category"]
    .replace(category_map)
)



# ======================
# Balance Dataset
# ======================

balanced = []


for category in df["Category"].unique():

    temp = df[
        df["Category"] == category
    ]

    temp = temp.sample(
        min(len(temp),500),
        random_state=42
    )


    balanced.append(temp)



df = pd.concat(
    balanced,
    ignore_index=True
)



print(
    df["Category"].value_counts()
)



# ======================
# Clean Text
# ======================

def clean(text):

    text = str(text).lower()

    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text



texts = (
    df["Resume"]
    .apply(clean)
    .tolist()
)


labels = df["Category"]



# ======================
# AI Embeddings
# ======================

print(
    "\nCreating AI embeddings..."
)


embedder = SentenceTransformer(
     "all-MiniLM-L6-v2"
)


X = embedder.encode(
    texts,
    show_progress_bar=True
)



# ======================
# Split
# ======================

X_train, X_test, y_train, y_test = train_test_split(

    X,

    labels,

    test_size=0.2,

    random_state=42,

    stratify=labels
)



# ======================
# Classifier
# ======================

model = LogisticRegression(

    max_iter=5000,

    class_weight="balanced"

)



model.fit(
    X_train,
    y_train
)



# ======================
# Evaluation
# ======================

pred = model.predict(
    X_test
)



acc = accuracy_score(
    y_test,
    pred
)



print(
    f"\n🔥 Accuracy: {acc*100:.2f}%"
)



print(
    classification_report(
        y_test,
        pred
    )
)



# ======================
# Save
# ======================

os.makedirs(
    "models",
    exist_ok=True
)


joblib.dump(
    model,
    "models/classifier.pkl"
)



print(
    "\nTransformer classifier saved 🧠🔥"
)