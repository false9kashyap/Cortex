from fastapi import FastAPI, UploadFile, File, Form, HTTPException

from fastapi.middleware.cors import CORSMiddleware


from app.parser import extract_text_from_pdf

from app.predictor import predict_category

from app.matcher import calculate_match







app = FastAPI(

    title="Cortex AI Resume Screening API",

    openapi_version="3.0.2"

)








# =====================================
# CORS Middleware
# =====================================

app.add_middleware(

    CORSMiddleware,


    allow_origins=[

        "http://localhost:5173"

    ],


    allow_credentials=True,


    allow_methods=[

        "*"

    ],


    allow_headers=[

        "*"

    ]

)









# =====================================
# Home Route
# =====================================

@app.get("/")
def home():


    return {

        "message":

            "Cortex AI Resume Screening API"

    }










# =====================================
# Health Check
# =====================================

@app.get("/health")
def health():


    return {

        "status":

            "running",


        "model":

            "loaded"

    }












# =====================================
# Match Score Engine
# =====================================

def generate_match_score(

        resume_text,

        job_description,

        prediction

):



    # Resume ↔ JD similarity

    match_result = calculate_match(

        resume_text,

        job_description

    )




    semantic_score = float(

        match_result["match_percentage"]

        .replace(

            "%",

            ""

        )

    )





    semantic_score = min(

        semantic_score * 1.8,

        100

    )









    # Role ↔ JD similarity

    role_text = " ".join(

        prediction["suggested_roles"]

    )





    role_match = calculate_match(

        role_text,

        job_description

    )





    role_score = float(

        role_match["match_percentage"]

        .replace(

            "%",

            ""

        )

    )






    role_score = min(

        role_score * 2,

        100

    )










    # Hybrid Score

    match_score = (

        0.7 * semantic_score

        +

        0.3 * role_score

    )





    match_score = round(

        match_score,

        2

    )










    # Decision

    if match_score >= 75:


        decision = "Strong Match"



    elif match_score >= 50:


        decision = "Moderate Match"



    else:


        decision = "Weak Match"








    return {


        "match_score":

            f"{match_score}%",



        "decision":

            decision,



        "numeric_score":

            match_score

    }












# =====================================
# Single Resume Prediction
# =====================================

@app.post("/predict")
async def predict_resume(


    file: UploadFile = File(...),


    job_description: str = Form(...)

):




    try:


        resume_text = extract_text_from_pdf(

            file.file

        )




    except Exception:


        raise HTTPException(

            status_code=400,

            detail="Unable to process resume"

        )








    prediction = predict_category(

        resume_text

    )







    score = generate_match_score(

        resume_text,

        job_description,

        prediction

    )








    return {


        "filename":

            file.filename,



        "suggested_roles":

            prediction["suggested_roles"],



        "match_score":

            score["match_score"],



        "decision":

            score["decision"]

    }















# =====================================
# Multiple Resume Ranking
# =====================================

@app.post("/rank")
async def rank_resumes(


    files: list[UploadFile] = File(...),


    job_description: str = Form(...)

):





    results = []








    for file in files:





        try:


            resume_text = extract_text_from_pdf(

                file.file

            )





        except Exception:


            continue









        prediction = predict_category(

            resume_text

        )








        score = generate_match_score(

            resume_text,

            job_description,

            prediction

        )









        results.append(

            {


                "filename":

                    file.filename,



                "suggested_roles":

                    prediction["suggested_roles"],



                "match_score":

                    score["match_score"],



                "decision":

                    score["decision"],



                "score":

                    score["numeric_score"]

            }

        )









    if len(results) == 0:


        raise HTTPException(

            status_code=400,

            detail="No valid resumes processed"

        )











    # Ranking Candidates

    ranked = sorted(

        results,


        key=lambda x:

            x["score"],


        reverse=True

    )










    for index, resume in enumerate(

        ranked

    ):



        resume["rank"] = index + 1



        del resume["score"]










    return {


        "total_resumes":

            len(ranked),



        "ranking":

            ranked

    }