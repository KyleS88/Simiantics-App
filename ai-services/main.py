from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sentence_transformers import SentenceTransformer
import torch
from PIL import Image
import io

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Loading CLIP model...")
model = SentenceTransformer('clip-ViT-B-32')
print("Model finished loading!")

@app.post("/embed")
async def embed (
    text: str = Form(None),
    file: UploadFile = File(None),
):
    if text is None and file is None:
        raise HTTPException(status_code=400, detail="No text or file provided")
    
    try:
        if text:
            print("Embedding text...")
            embedding = model.encode(text)
        elif file:
            print("Embedding image...")
            file_contents = await file.read()
            image = Image.open(io.BytesIO(file_contents))
            embedding = model.encode(image)
        return {"embedding": embedding.tolist()}
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

