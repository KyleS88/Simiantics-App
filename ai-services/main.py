from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import torch
from contextlib import asynccontextmanager
import uuid
from redis_utils import save_item, create_index, vector_search, search_by_filename
from transformer_utils import embed, load_model
from fastapi.staticfiles import StaticFiles
import os

@asynccontextmanager
async def startup_event(app: FastAPI):
    try:
        load_model()
        await create_index()
    except Exception as e:
        print(f"Error in loading the CLIP model and/or creating the index. Is Redis Stack running? {e}")
    yield

app = FastAPI(lifespan=startup_event)

UPLOAD_DIR = 'uploads'
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
if (not os.path.exists("uploads")):
    os.makedirs("uploads")
app.mount("/images", StaticFiles(directory="uploads"), name="images")
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    try:
        original_name = os.path.basename(file.filename)
        ext = os.path.splitext(original_name)[1].lower()    
        stored_name = f"{uuid.uuid4()}{ext}"
        file_data = await file.read()
        item_id = str(uuid.uuid4())
        embedding = (await embed(file_data, None ))["embedding"]
        await save_item(item_id, original_name, embedding, stored_name)

        path = os.path.join(UPLOAD_DIR, stored_name)
        with open(path, "wb") as buffer:
            buffer.write(file_data)
        
        return {"message": "success", "id": item_id, "filename": original_name}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/search")
async def search(q: str, isFileName: bool):
    try:
        print("returning results")
        result = None
        if (isFileName is True):
            result = await search_by_filename(q)
        else:
            query_vector = (await embed(None, q))["embedding"]
            result = await vector_search(query_vector)   
        if (result is None):
            raise HTTPException(status_code=404, detail="No matching files")
        output = []
        for doc in result.docs:
            if (1-float(doc.score) < .22):
                continue
            output.append({
                "id": doc.id,
                "filename": doc.filename,
                "stored_name": doc.stored_name,
                "score": 1 - float(doc.score),
                "url": f"http://localhost:8000/images/{doc.stored_name}"
            })
        images_url = [item["url"] for item in output]
        return {"results": output, "images": images_url}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)