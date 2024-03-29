"use client"
import { useState  , useRef , useEffect} from "react"
  
export default function Home() {
  const [file , setFile] = useState<any>(null)
  const [id , setId] = useState<string>("")
  const [video , setVideo] = useState<any>(null)
  const DragandDropRef = useRef<HTMLDivElement>(null)
  const data:FormData = new FormData()
  const handleChange = function(event:any) {
    setFile(Array.from(event.target.files))
    // console.log(file)
    for(const files in file)
    {
      data.append('file', files)
    }
    // console.log(data)
  }
  const handleSubmit = async function(event:any) {
    event.preventDefault()
    console.log("Submitted")
    const data_: FormData = new FormData()
    // data_.append('file', file[0])
    for (const files in file) {
      console.log(files)
      data_.append('file', file[files])
    }
    console.log(data_)
    const res = await fetch('http://localhost:8000/uploadfiles/', {
      headers: {
        'uId': id,
      },
      method: 'POST',
      body: data_,
    })
    console.log(res)
  }
  const getVideo = async function() {
    const res = await fetch('http://localhost:8000/get-video/' , {headers: {'uId': id,}})
    var value = URL.createObjectURL(await res.blob());
    setVideo(value)

    console.log("respose is this " ,value)
  }
  const handleDragOver = function(event:any) {
    event.preventDefault()
    event.dataTransfer.dropEffect = 'copy'
    DragandDropRef.current? DragandDropRef.current.style.backgroundColor = "red" :
    console.log("Dragging")
  }
  const handleDrop = function(e:any)
  {
    console.log("Dropeed")
    e.preventDefault()
    setFile(Array.from(e.dataTransfer.files))
    for(const files in file)
    {
      data.append('file', file[files])
    }
  }

  useEffect(() => {
    const cookieValue = document.cookie
    .split('; ')
    .find((row) => row.startsWith('myCookie='))
    ?.split('=')[1];

    
    if (!cookieValue) {
      
      const genId = makeid(10)
      document.cookie = 'myCookie='+genId;
      console.log('Cookie has been set ' + genId)
      setId(genId)
    }
    else{
      console.log('Cookie is already set ' + cookieValue)
      setId(cookieValue)
    }
    // console.log(cookieStore)
  }
  , [])


  return <div>
    <form onSubmit={handleSubmit}>
    <input type="file" onChange={handleChange} name="input_file" multiple />
    <button type="submit">Submit</button>
    </form>
    <div className="w-1/2 h-[20vh] mx-auto my-[30vh] bg-slate-300 "
        ref={DragandDropRef}
        onDragOver={handleDragOver}
        onDrop={handleDrop} 
        onDropCapture={handleDrop}
        >
      Drag and Drop Here
    </div>
    <div>
      <button onClick={getVideo}>Render</button>
    </div>
    {video && <video src={video} controls />}
  </div>
}


function makeid(length:number) {
  let result = '';
  const characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
  const charactersLength = characters.length;
  let counter = 0;
  while (counter < length) {
    result += characters.charAt(Math.floor(Math.random() * charactersLength));
    counter += 1;
  }
  return result;
}