import { useState } from 'react';
import { searchImages, uploadImage } from './api'
import { Carousel } from "./Components/Carousel"
import axios from 'axios';

const App = () => {
  const [query, setQuery] = useState<string>("");
  const [searchResults, setSearchResults] = useState([]);
  const [imageUrls, setImageUrls] = useState<string[]>([]);
  const [isFile, setIsFile] = useState<boolean>(false);
  const [err, setErr] = useState<string>("");

  const handleFileCheck = (e: React.ChangeEvent<HTMLInputElement>) => {
      setIsFile(e.target.checked);
  }

  const handleSearch = async () => {
    try {
      if (!query) {
        setErr("Please enter a search query");
        return;
      }
      const data = await searchImages(query, isFile);
      console.log(data)
      setSearchResults(data.results);
      setImageUrls(data.images)
    } catch (err) {
      err instanceof Error? setErr(err.message):
        setErr(`An unexpected error has occured please refresh the page: ${err}`);
    }
  }

  const handleUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    try {
      await uploadImage(e.target.files?.[0]);
    } catch (err) {
      err instanceof Error? setErr(err.message):
        setErr(`An unexpected error has occured please refresh the page: ${err}`);
    }
  }
  return (
  <>
    {err && <p>{err}</p>}
    <h1 style={{display:'flex', justifyContent: 'center'}}>Image Matching Engine</h1>
    <div className="image-upload-div">
      <input type="file" accept="image/*" onChange={(e)=>handleUpload(e)} />
    </div>
    <div className="userInputSection">
        <input
          style={{
            display: 'flex',
            width:'800px',
            height: '100px',
            fontSize: '20px',
            justifyContent: 'center',
            
          }}
          type="text" 
          onChange={(e)=>setQuery(e.target.value)}
          placeholder='What do you want to search? e.g. filename, treehouse'
        />
        <input
          type='checkbox'
          id="isFile"
          name="isFile"
          checked={isFile}
          onChange={(e)=>handleFileCheck(e)}
        />
        <label htmlFor="isFile">Are you searching for a file?</label>
        <button onClick={handleSearch}>Search</button>
    </div>
    <div className='imageDisplay'>
      <Carousel images={imageUrls}/>
    </div>
  </>
  )
}

export default App
