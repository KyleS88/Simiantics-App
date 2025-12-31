from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import torch
from contextlib import asynccontextmanager
import uuid
from redis_utils import save_item, create_index, vector_search, search_by_filename
from transformer_utils import embed, load_model
from fastapi.staticfiles import StaticFiles
import os

@asynccontextmanager
async def startup_event(app: FastAPI):
    load_model()
    await create_index()
    yield

app = FastAPI(lifespan=startup_event)

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
        embedding = await embed(None, file)["embedding"]
        item_id = str(uuid.uuid4())
        await save_item(item_id, file.filename, embedding)
        return {"message": "success", "id": item_id, "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/search")
async def search(q: str, isFileName: bool):
    try:
        result = None
        if (isFileName is True):
            result = search_by_filename(q)
        else:
            query_vector = await embed(q, None)
            result = await vector_search(query_vector)   
        if (result is None):
            return { "results": "No matching file"}
        output = []
        for doc in result:
            output.append({
                "id": doc.id,
                "filename": doc.filename,
                "score": 1 - float(doc.score),
                "url": f"http://localhost:8000/images/{doc.filename}"
            })
        return {"results": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)