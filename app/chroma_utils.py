import json
import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

client = chromadb.PersistentClient(path="/app/chroma_data")
collection = client.get_or_create_collection("products")

def product_exists(product_id: str) -> bool:
    results = collection.get(limit=10000)
    ids = results.get("ids", [])
    return product_id in ids

def index_products_if_empty(json_path="products.json"):
    if len(collection.get(limit=1)["ids"]) > 0:
        print("ℹ️ Collection already contains data. Indexing is not needed.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    for product in products:
        product_id = str(product['id'])
        if product_exists(product_id):
            print(f"⚠️ Product with ID {product_id} already exists. Skipping.")
            continue

        text = (
            f"Name: {product['name']}. "
            f"Description: {product['description']}. "
            f"Category: {product['category']}. "
            f"Size: {product['size']}. "
            f"Color: {product['color']}. "
            f"Price: {product['price']}."
        )
        embedding = embedding_model.encode(text).tolist()
        collection.add(
            ids=[product_id],
            documents=[text],
            embeddings=[embedding],
            metadatas=[{
                "name": product["name"],
                "description": product["description"],
                "category": product["category"],
                "size": product["size"],
                "color": product["color"],
                "price": product["price"],
                "stock": product["stock"],
                "image_url": product["image_url"],
            }]
        )
    print("✅ Products indexed in Chroma.")

def search_products(query, n_results=3):
    query_embedding = embedding_model.encode(query).tolist()
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )
    return results
