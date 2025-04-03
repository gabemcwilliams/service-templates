import docker
import subprocess
import datetime

# Initialize Docker client
client = docker.from_env()

# Generate image tags
repo_name = "docker-registry.example.internal:5000/vault_ubuntu_22.04"
timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M")
commit_hash = subprocess.getoutput("git rev-parse --short HEAD").strip()

# Image tags
latest_tag = f"{repo_name}:latest"
version_tag = f"{repo_name}:{timestamp}-{commit_hash}"

print(f"📦 Building Docker image: {version_tag}...")
image, _ = client.images.build(path="/mnt/data/build/", tag=version_tag)

# Tag 'latest'
image.tag(repo_name, tag="latest")

# Push both tags
for tag in [version_tag, "latest"]:
    print(f"🚀 Pushing {repo_name}:{tag} to registry...")
    client.images.push(repo_name, tag=tag)

print("✅ Build & Push Complete!")
