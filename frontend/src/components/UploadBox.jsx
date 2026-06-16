import { useState, useEffect } from "react"

import axios from "axios"

import { Upload } from "lucide-react"





function UploadBox({ mode, setResults, setLoading }) {



    const [jobDescription, setJobDescription] = useState("")


    const [files, setFiles] = useState([])









    // Reset everything when switching Analyze / Rank

    useEffect(

        () => {


            setFiles([])


            setJobDescription("")


            setResults([])



        },


        [mode]

    )











    const submit = async () => {




        if (!jobDescription || files.length === 0) {



            alert("Enter JD and upload resume")


            return



        }










        const formData = new FormData()







        formData.append(

            "job_description",

            jobDescription

        )









        if (mode === "rank") {




            files.forEach(

                (file) => {



                    formData.append(

                        "files",

                        file

                    )



                }

            )



        }





        else {




            formData.append(

                "file",

                files[0]

            )



        }











        try {




            setLoading(true)









            const url =

                mode === "rank"


                    ?


                    "http://127.0.0.1:8000/rank"


                    :


                    "http://127.0.0.1:8000/predict"










            const response = await axios.post(

                url,

                formData

            )










            if (mode === "rank") {




                setResults(

                    response.data.ranking

                )



            }





            else {




                setResults(

                    [

                        response.data

                    ]

                )



            }





        }






        catch (error) {




            console.log(error)


            alert("Analysis failed")



        }







        finally {




            setLoading(false)



        }



    }












    return (



        <div className="
        mt-10

        w-[620px]

        bg-[#0b0b0b]

        border
        border-white/10

        rounded-3xl

        p-6
        ">











            <textarea


                placeholder="Paste Job Description..."


                value={jobDescription}



                onChange={(e) =>


                    setJobDescription(

                        e.target.value

                    )


                }





                className="
                w-full

                h-32

                bg-black

                border
                border-white/10

                rounded-xl

                p-4

                resize-none

                outline-none

                focus:border-lime-400
                "


            />












            <label className="
            mt-5

            h-24

            flex

            flex-col

            items-center

            justify-center

            border

            border-dashed

            border-lime-400/50

            rounded-xl

            cursor-pointer

            hover:scale-[1.02]

            transition

            duration-300
            ">








                <Upload

                    className="text-lime-400"

                />










                <p className="mt-3">





                    {


                        files.length > 0


                            ?


                            (


                                mode === "rank"


                                    ?


                                    `${files.length} resumes selected`


                                    :


                                    files[0].name



                            )



                            :



                            (


                                mode === "rank"


                                    ?


                                    "Upload Multiple Resume PDFs"


                                    :


                                    "Upload Resume PDF"



                            )



                    }






                </p>












                <input


                    type="file"



                    accept=".pdf"



                    multiple={

                        mode === "rank"

                    }





                    hidden







                    onChange={(e) =>



                        setFiles(



                            Array.from(

                                e.target.files

                            )



                        )



                    }


                />










            </label>













            <button


                onClick={submit}



                className="
                mt-5

                w-full

                bg-lime-400

                text-black

                py-3

                rounded-xl

                font-bold

                hover:scale-[1.03]

                active:scale-95

                transition

                duration-300
                ">








                {

                    mode === "rank"


                        ?


                        "Rank Candidates"


                        :


                        "Analyze Candidate"


                }









            </button>










        </div>



    )



}






export default UploadBox