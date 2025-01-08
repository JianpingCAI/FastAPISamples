import requests
from typing import List
import base64
import json
from backend.schemas import NodeDataORM, NodeDataCreate, FileMetadata

API_URL = "http://localhost:8000/api"


def fetch_root_nodes() -> List[NodeDataORM]:
    """Fetch the root nodes from the backend."""
    response = requests.get(f"{API_URL}/reference_data/root")
    response.raise_for_status()
    return [NodeDataORM(**node) for node in response.json()]


def fetch_child_nodes(parent_id: str) -> List[NodeDataORM]:
    """Fetch child nodes for a specific parent ID."""
    response = requests.get(f"{API_URL}/reference_data/parent/{parent_id}")
    response.raise_for_status()
    return [NodeDataORM(**node) for node in response.json()]


def fetch_child_folder_nodes(parent_id: str) -> List[NodeDataORM]:
    """Fetch child nodes for a specific parent ID."""
    response = requests.get(f"{API_URL}/folders/parent/{parent_id}")
    response.raise_for_status()
    return [NodeDataORM(**node) for node in response.json()]


def fetch_child_file_nodes(parent_id: str) -> List[NodeDataORM]:
    """Fetch child nodes for a specific parent ID."""
    response = requests.get(f"{API_URL}/files/parent/{parent_id}")
    response.raise_for_status()
    return [NodeDataORM(**node) for node in response.json()]


def delete_node(node_id: str) -> bool:
    """Delete a node by its ID."""
    try:
        response = requests.delete(f"{API_URL}/reference_data/{node_id}")
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        print(f"Failed to delete node: {e}")
        return False


def create_node(data: NodeDataCreate) -> NodeDataORM:
    """Create a new reference data entry."""
    response = requests.post(f"{API_URL}/reference_data/", json=data.dict())
    response.raise_for_status()
    return NodeDataORM(**response.json())


def upload_file(file_contents: str, metadata: FileMetadata) -> NodeDataORM:
    """
    Upload a file with metadata to the backend.
    Args:
        file_content: Base64 encoded file content
        metadata: FileMetadata object containing file metadata
    """
    try:
        # Decode the file content from base64
        content = base64.b64decode(file_contents.split(",")[1])

        # Create multipart form data
        files = {"file": (metadata.name, content)}
        data = {"metadata": metadata.model_dump_json()}

        response = requests.post(f"{API_URL}/upload", files=files, data=data, timeout=30)
        response.raise_for_status()
        return NodeDataORM(**response.json())
    except requests.exceptions.RequestException as e:
        raise Exception(f"Upload failed: {str(e)}")


def download_file(file_id: str) -> bytes:
    """
    Download a file by its ID.
    Args:
        file_id: ID of the file to download
    """
    response = requests.get(f"{API_URL}/download/{file_id}")
    response.raise_for_status()
    return response.content
