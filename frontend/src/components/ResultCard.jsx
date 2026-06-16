function ResultCard({ data }) {



    return (



        <div className="
        mb-5

        bg-[#0b0b0b]

        border
        border-white/10

        rounded-2xl

        p-6


        hover:border-lime-400/50

        hover:scale-[1.01]

        transition

        duration-300
        ">







            <div className="
            flex

            justify-between

            items-start

            gap-6
            ">







                <div className="
                max-w-[420px]
                ">



                    <h2 className="
                    text-lg

                    font-bold

                    text-white
                    ">



                        {

                            data.rank

                            &&

                            `#${data.rank} `

                        }


                        {data.filename}



                    </h2>









                    <p className="
                    mt-4

                    text-gray-400

                    text-sm
                    ">




                        {

                            data.suggested_roles
                            .join("  •  ")

                        }



                    </p>








                </div>












                <div className="
                text-right

                min-w-[120px]
                ">






                    <h1 className="
                    text-3xl

                    font-black

                    text-lime-400
                    ">



                        {data.match_score}




                    </h1>







                    <p className="
                    text-xs

                    text-gray-500

                    mt-1
                    ">


                        Match Score



                    </p>








                </div>





            </div>












            <div className="
            mt-6
            ">



                <span className="
                px-5

                py-2

                rounded-full


                bg-lime-400/10

                text-lime-400

                text-sm

                font-semibold
                ">



                    {data.decision}



                </span>





            </div>








        </div>




    )



}





export default ResultCard