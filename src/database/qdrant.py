from qdrant_client.models import Distance, VectorParams
from qdrant_client import QdrantClient
from typing import Dict

class QdrantSetup:
    def __init__(self, collection_name: str, vector_size: int, url: str = "http://localhost:6333",distance_metric: Distance = Distance.COSINE):
        self.collection_name = collection_name
        self.vector_size = vector_size
        self.distance_metric = distance_metric
        self.client = QdrantClient(url=url)

    def create_collection(self) -> Dict[str, str]:
        """
        Create new collection in Qdrant if it doesn't exist
        """
        if not self.client.collection_exists(self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=self.vector_size, distance=self.distance_metric)
            )
            return {"result":"success", "message": f"Collection '{self.collection_name}' created successfully."}
        else:
            return {"result":"exists", "message": f"Collection '{self.collection_name}' already exists."}
    
    def upsert_points(self, points: list) -> Dict[str, str]:
        """
        Upsert points into the collection
        """
        try:
            self.client.upsert(
                collection_name=self.collection_name,
                points=points
            )
            return {"result":"success", "message": f"Points upserted successfully into collection '{self.collection_name}'."}
        except Exception as e:
            return {"result":"error", "message": f"An error occurred while upserting points: {str(e)}"}

if __name__ == "__main__":
    qdrant_setup = QdrantSetup(collection_name="pdf_embeddings_text", vector_size=4)
    print(qdrant_setup.create_collection())
    output = qdrant_setup.upsert_points(points=[
        {
            "id": 1,
            "vector": [0.1, 0.2, 0.3, 0.4],
            "payload": {"text": "This is a sample text for point 1."}
        },
        {
            "id": 2,
            "vector": [0.5, 0.6, 0.7, 0.8],
            "payload": {"text": "This is a sample text for point 2."}
        }
    ])
    print(output)
