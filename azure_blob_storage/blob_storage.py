from msrest.authentication import ApiKeyCredentials
import os
from azure.identity.aio import DefaultAzureCredential
from azure.storage.blob.aio import BlobServiceClient, BlobClient, ContainerClient
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, PublicAccess, BlobBlock, StandardBlobTier
from config import(
    image_name_stored_in_blob_storage,
)

async def upload_blob_file(blob_service_client: BlobServiceClient, container_name: str, directory: str, filename: str):

    try:
        async with BlobServiceClient(account_url, credential=credential) as blob_service_client:
        container_client = blob_service_client.get_container_client(container=container_name)
        with open(file=os.path.join(directory, filename), mode="rb") as data:
            await container_client.upload_blob(name=image_name_stored_in_blob_storage, data=data, overwrite=True)

    except Exception as e:
        print(f"Error uploading file: {e}")