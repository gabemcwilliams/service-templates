# -----------------------------------------------------------------------------
# MinIO Functionality Testing Using `mc` (MinIO Client) on Windows & Linux
# -----------------------------------------------------------------------------
# This guide provides step-by-step instructions to test MinIO using `mc`
# on both Windows and Linux environments.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# ✅ Step 1: Install `mc` (MinIO Client)
# -----------------------------------------------------------------------------
# Windows:
# - Download MinIO Client: `https://dl.min.io/client/mc/release/windows-amd64/mc.exe`
# - Move `mc.exe` to a folder in your `PATH` (e.g., `C:\Windows\System32\` for easy access)
# - Verify installation:
mc --version

# Linux:
# - Download & install `mc`:
wget https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/local/bin/mc
chmod +x /usr/local/bin/mc
mc --version

# -----------------------------------------------------------------------------
# ✅ Step 2: Configure MinIO Client (`mc`)
# -----------------------------------------------------------------------------
# Set up MinIO connection in `mc`:
mc alias set myminio https://minio.example.internal ACCESS_KEY SECRET_KEY

# Verify alias:
mc alias list

# -----------------------------------------------------------------------------
# ✅ Step 3: Verify MinIO Buckets
# -----------------------------------------------------------------------------
# List available buckets:
mc ls myminio/

# Create a new test bucket:
mc mb myminio/testbucket

# Verify bucket creation:
mc ls myminio/

# -----------------------------------------------------------------------------
# ✅ Step 4: Upload and Download Files
# -----------------------------------------------------------------------------
# Windows - Upload a test file:
echo "This is a test file" > testfile.txt
mc cp testfile.txt myminio/testbucket/

# Linux - Upload a test file:
echo "This is a test file" > testfile.txt
mc cp testfile.txt myminio/testbucket/

# List files in the bucket:
mc ls myminio/testbucket/

# Download the file back to local machine:
mc cp myminio/testbucket/testfile.txt ./downloaded_testfile.txt

# Verify the file integrity:
cat downloaded_testfile.txt  # Should output: "This is a test file"

# -----------------------------------------------------------------------------
# ✅ Step 5: Delete Files & Buckets
# -----------------------------------------------------------------------------
# Remove a file from MinIO:
mc rm myminio/testbucket/testfile.txt

# Delete the test bucket:
mc rb myminio/testbucket --force

# Verify deletion:
mc ls myminio/

# -----------------------------------------------------------------------------
# ✅ Troubleshooting
# -----------------------------------------------------------------------------
# Check MinIO logs (Linux):
sudo journalctl -u minio --no-pager

# Check if MinIO is running:
sudo systemctl status minio

# Trace API calls to MinIO:
mc admin trace myminio

# If facing TLS issues, use `--insecure` (for testing only):
mc alias set myminio https://minio.example.internal ACCESS_KEY SECRET_KEY --insecure

# -----------------------------------------------------------------------------
# 🎉 MinIO is Now Fully Tested!
# -----------------------------------------------------------------------------
# You can now use MinIO for storage, API integrations, and more. 🚀

