import requests
import json

REGISTRY_URL = "http://docker-registry.example.internal:5000/v2"
REPO_NAME = "vault_ubuntu_22.04"
KEEP_LATEST_N = 5  # Keep only the last 5 images

# Get all tags
resp = requests.get(f"{REGISTRY_URL}/{REPO_NAME}/tags/list")
tags = sorted(json.loads(resp.text)["tags"], reverse=True)  # Sort latest first

# Delete old images
for tag in tags[KEEP_LATEST_N:]:
    print(f"🗑️ Deleting old image: {REPO_NAME}:{tag}...")
    digest_resp = requests.get(f"{REGISTRY_URL}/{REPO_NAME}/manifests/{tag}", headers={
        "Accept": "application/vnd.docker.distribution.manifest.v2+json"
    })
    digest = digest_resp.json()["config"]["digest"]
    delete_resp = requests.delete(f"{REGISTRY_URL}/{REPO_NAME}/manifests/{digest}")
    if delete_resp.status_code == 202:
        print(f"✅ Deleted {tag}")
    else:
        print(f"❌ Failed to delete {tag}: {delete_resp.text}")
