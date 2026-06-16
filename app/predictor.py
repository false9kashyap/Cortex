import joblib
import numpy as np

from app.embedder import embedder



# ============================
# Load classifier once
# ============================

classifier = joblib.load(
    "models/classifier.pkl"
)



# ============================
# Predict Top Roles
# ============================

def predict_category(
        resume_text
):


    # Create resume embedding

    embedding = embedder.encode(
        [
            resume_text
        ]
    )



    # Calculate probabilities internally

    probabilities = (
        classifier
        .predict_proba(
            embedding
        )[0]
    )



    classes = (
        classifier
        .classes_
    )



    # Get top 3 roles

    top_indices = np.argsort(
        probabilities
    )[::-1][:3]



    suggested_roles = []



    for index in top_indices:

        suggested_roles.append(
            classes[index]
        )



    # Best predicted role

    top_role = classes[
        top_indices[0]
    ]



    role_confidence = (

        probabilities[
            top_indices[0]
        ]

        *

        100

    )




    return {

        # shown to user

        "suggested_roles":
            suggested_roles,


        # hidden ranking features

        "top_role":
            top_role,


        "role_confidence":
            round(
                float(role_confidence),
                2
            )

    }