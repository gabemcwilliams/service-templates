# Vault PKI Setup - Multi-SAN Certificate Approach

## Step 1: Enable & Configure Vault PKI

This setup enables Vault’s PKI, issues TLS certificates, and integrates them into Vault, MinIO, and Nginx for secure communications.

### Enable the PKI secrets engine:
```sh
vault secrets enable pki
```

### Set maximum certificate lease duration (10 years):
```sh
vault secrets tune -max-lease-ttl=87600h pki
```

## Step 2: Generate Root CA

### Create a self-signed Root CA valid for 10 years:
```sh
vault write pki/root/generate/internal \
    common_name="example.internal" \
    ttl="87600h"
```

### Configure Certificate Authority (CA) URLs:
```sh
vault write pki/config/urls \
    issuing_certificates="http://vault.example.internal:8200/v1/pki/ca" \
    crl_distribution_points="http://vault.example.internal:8200/v1/pki/crl"
```

## Step 3: Define Certificate Issuance Roles

### Multi-SAN Role (for Core Services):
```sh
vault write pki/roles/internal-services \
    allowed_domains="example.internal,vault.example.internal,minio.example.internal,db.example.internal,internal" \
    allow_subdomains=true \
    allow_wildcard_certificates=true \
    max_ttl="8760h"
```

### Wildcard Role (for Applications Supporting Wildcards):
```sh
vault write pki/roles/wildcard-internal \
    allowed_domains="example.internal" \
    allow_subdomains=true \
    allow_wildcard_certificates=true \
    max_ttl="8760h"
```

## Step 4: Issue Multi-SAN Certificates

### Issue a TLS certificate with multiple SANs:
```sh
vault write pki/issue/internal-services \
    common_name="example.internal" \
    alt_names="vault.example.internal,minio.example.internal,db.example.internal,*.example.internal" \
    ttl="8760h" 
```

---

**Next:** Proceed to [Vault SSL and Configuration](#) to extract and configure certificates.