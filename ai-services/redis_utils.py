import redis.asyncio as redis
import numpy as np
from redis.commands.search.field import VectorField, TextField
from redis.commands.search.query import Query
from redis.commands.search.index_definition import IndexDefinition, IndexType

client = redis.from_url("redis://localhost:6379", decode_responses=True)

async def create_index():
    index_name = "idx:items"
    try: 
        await client.ft(index_name).info()
    except:
        schema = (
            TextField("filename"),
            VectorField("embedding", "HNSW", {
                "TYPE": "FLOAT32",
                "DIM": 512,
                "DISTANCE_METRIC": "COSINE" 
            })
        )
        definition = IndexDefinition(prefix=["item:"], index_type= IndexType.HASH)
        await client.ft("idx:items").create_index(fields=schema, definition=definition)
        print("Index created")

async def search_by_filename(filename: str):
    query = Query(f"@filename: {filename}")
    results = await client.ft("idx:items").search(query)
    return results

async def vector_search(query_vector):
    vector_bytes_query = np.array(query_vector, dtype=np.float32).tobytes()
    query = Query("*=>[KNN 5 @embedding $vec AS score]").sort_by("score").dialect(2)

    results = await client.ft("idx:items").search(query, {"vec": vector_bytes_query})
    return results

async def save_item(item_id, filename, vector):
    vector_bytes = np.array(vector, dtype=np.float32).tobytes()
    await client.hset(
        f"item:{item_id}",
        mapping={
            "filename": filename,
            "type": "image",
            "embedding": vector_bytes
        }
    )
    print(f"Saved {filename} to Redis as item:{item_id}")
