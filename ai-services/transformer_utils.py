from fastapi import Form, HTTPException
from sentence_transformers import SentenceTransformer
from PIL import Image
import io
model = None

def load_model():
    global model
    if (model is None):
        model = SentenceTransformer('clip-ViT-B-32', device='cpu')
    return model

async def embed (
    image_data=None,
    text: str = Form(None),
):
    if text is None and image_data is None:
        raise HTTPException(status_code=400, detail="No text or file provided")
    
    try:
        if text:
            print("Embedding textd...")
            embedding = model.encode(text)
        elif image_data:
            print("Embedding image...")
            image = Image.open(io.BytesIO(image_data)).convert("RGB")
            embedding = model.encode(image)
        print("Image embedded successfully")
        return {"embedding": embedding.tolist()}
    except Exception as e:
        print(f"Error {e}")
        raise HTTPException(status_code=500, detail=str(e))


