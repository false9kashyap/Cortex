import { useState } from "react"


import Header from "./components/Header"

import UploadBox from "./components/UploadBox"

import ResultCard from "./components/ResultCard"

import Loader from "./components/Loader"







function App(){



  const [results,setResults] = useState([])



  const [mode,setMode] = useState("analyze")



  const [loading,setLoading] = useState(false)







  const changeMode = (selectedMode) => {



    setMode(selectedMode)



    setResults([])



    setLoading(false)



  }









  return (



    <div className="
    min-h-screen

    flex

    flex-col

    items-center

    pb-10
    ">







        <Header/>









        {/* Mode Selector */}

        <div className="
        mt-10

        flex

        bg-[#0b0b0b]

        border

        border-white/10

        rounded-xl

        p-2
        ">







          <button


          onClick={()=>changeMode("analyze")}



          className={`

          px-8

          py-3

          rounded-lg

          font-bold


          transition-all

          duration-300


          hover:scale-105


          ${


            mode==="analyze"


            ?


            "bg-lime-400 text-black"


            :


            "text-gray-400"


          }


          `}


          >



            Analyze Candidate



          </button>









          <button


          onClick={()=>changeMode("rank")}



          className={`

          px-8

          py-3

          rounded-lg

          font-bold


          transition-all

          duration-300


          hover:scale-105


          ${


            mode==="rank"


            ?


            "bg-lime-400 text-black"


            :


            "text-gray-400"


          }


          `}


          >



            Rank Candidates



          </button>







        </div>











        <UploadBox


          mode={mode}


          setResults={setResults}


          setLoading={setLoading}


        />











        {

          loading &&

          <Loader/>

        }











        <div className="
        mt-6

        w-[620px]

        transition-all

        duration-300
        ">








          {


            results.map(


              (item,index)=>(



                <ResultCard


                  key={index}


                  data={item}


                />



              )


            )


          }








        </div>








    </div>



  )



}








export default App