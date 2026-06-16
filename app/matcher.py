from sklearn.metrics.pairwise import cosine_similarity

from app.embedder import embedder



def calculate_match(
        resume_text,
        job_description
):


    # Generate embeddings

    embeddings = embedder.encode(
        [
            resume_text,
            job_description
        ]
    )



    resume_embedding = embeddings[0]

    jd_embedding = embeddings[1]



    # Cosine similarity

    similarity = cosine_similarity(

        [resume_embedding],

        [jd_embedding]

    )[0][0]



    # Real transformer score

    percentage = similarity * 100



    percentage = max(
        percentage,
        0
    )



    percentage = round(
        float(percentage),
        2
    )



    # ATS decision

    if percentage >= 55:

        decision = "Strong Match"


    elif percentage >= 35:

        decision = "Moderate Match"


    else:

        decision = "Weak Match"




    return {

        "match_percentage":
            f"{percentage}%",


        "decision":
            decision

    }