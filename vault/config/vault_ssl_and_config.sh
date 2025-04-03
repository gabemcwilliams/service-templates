
# -----------------------------------------------------------------------------
# Store and Secure Certificates
# -----------------------------------------------------------------------------
# - Manually copy each certificate part from `multi_san_cert.txt` into separate files.
# - Ensure correct permissions for security.
# -----------------------------------------------------------------------------

# Create the Vault certificate directory if it doesn't exist
mkdir -p /mnt/data/swarm/certs/vault
cd /mnt/data/swarm/certs/vault

# Open the cert file for manual extraction
nano multi_san_cert.txt

# Extract and copy the relevant sections:
nano ca_chain.crt    # Copy the CA chain
nano ca.crt          # Copy only the Root CA
nano private.key     # Copy the Private Key
nano public.crt      # Copy the Server Certificate

# -----------------------------------------------------------------------------
# Secure Certificate Permissions
# -----------------------------------------------------------------------------
# - Private key: Only readable by the owner
# - Public certs: Readable by all services
# -----------------------------------------------------------------------------
sudo chmod 600 private.key
sudo chmod 644 public.crt ca.crt ca_chain.crt

# -----------------------------------------------------------------------------
# Step 4: Configure Vault, MinIO, and Nginx to Use TLS
# -----------------------------------------------------------------------------
# This step configures each service to use the issued TLS certificates.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Configure Vault for TLS
# -----------------------------------------------------------------------------
# Updates Vault's configuration file to use the issued certificates.
# -----------------------------------------------------------------------------

#listener "tcp" {
#  address       = "0.0.0.0:8200"
#  tls_cert_file = "/etc/vault.d/public.crt"
#  tls_key_file  = "/etc/vault.d/private.key"
#  tls_disable   = 0  #  0 = Allows HTTP (INSECURE, only for local testing), 1 = HTTPS
#}

# Restart Vault to apply the changes
sudo systemctl restart vault
