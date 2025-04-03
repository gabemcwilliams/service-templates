
# Configuring PostgreSQL as the Backend Store for MLflow

### Prerequisites:
- PostgreSQL is already installed and configured for production.
- MLflow is running in your environment.
- Sudo privileges on the host for creating users and databases.

---

### 1. Switch to PostgreSQL User
PostgreSQL creates a system user `postgres` during installation. Switch to this user to manage PostgreSQL:

```bash
sudo -i -u postgres
```

---

### 2. Create PostgreSQL User and Database for MLflow

- **Create a User for MLflow:**

  Run the following command to create a new PostgreSQL user for MLflow. You will be prompted for a password for the user.

  ```bash
  createuser --pwprompt mlflow
  ```

  Example output:
  ```
  Enter password for new role: [Enter password]
  Enter it again: [Re-enter password]
  ```

- **Create a Database for MLflow:**

  Create a database named `mlflow` with the user `mlflow` as the owner:

  ```bash
  createdb --owner=mlflow mlflow
  ```

- **Grant Permissions:**

  You need to grant all privileges to the `mlflow` on the `mlflow` database:

  ```bash
  psql
  GRANT ALL PRIVILEGES ON DATABASE mlflow TO mlflow;
  \q
  ```

---

### 3. Connect MLflow to PostgreSQL
Now that the PostgreSQL user and database are set up, you need to configure **MLflow** to connect to this database.

- **Set Database URI in MLflow:**

  MLflow connects to PostgreSQL using a database URI in the format:

  ```bash
  postgresql://<username>:<password>@<host>:<port>/<database>
  ```

  You can specify this in your `mlflow.env` file or directly in the `MLFLOW_TRACKING_URI` environment variable.

  Here is an example of the `mlflow.env` file:

  ```bash
  MLFLOW_TRACKING_URI=postgresql://mlflow:<password>@localhost:5432/mlflow
  ```

  Replace `<password>` with the actual password for the `mlflow` you created.

---

### 4. Verify PostgreSQL Connection
Ensure MLflow is connected to PostgreSQL by running the following command:

```bash
mlflow server --host 0.0.0.0 --port 5000
```

Check the MLflow UI by navigating to `http://localhost:5000` and verify that data is being tracked in PostgreSQL.

---

### 5. Optional: Configure SSL for PostgreSQL (If Using SSL)

If you are using SSL for your PostgreSQL connection, you can configure MLflow to use the same SSL certificates.

Here is an example of setting up SSL in your PostgreSQL connection string:

```bash
MLFLOW_TRACKING_URI=postgresql://mlflow:<password>@localhost:5432/mlflow?sslmode=require&sslrootcert=/path/to/ca.crt
```

Replace `/path/to/ca.crt` with the path to your SSL certificate.

---

### 6. Configuring Postgres with MinIO (Optional)

If you want to store artifacts in MinIO and use it with PostgreSQL as a backend for MLflow:

- **Set up the MinIO connection in MLflow:**

  In your `mlflow.env` file, specify the MinIO configuration for artifact storage:

  ```bash
  MLFLOW_ARTIFACT_LOCATION=s3://mlflow-artifacts
  MLFLOW_S3_ENDPOINT_URL=http://minio.example.internal:9000
  ```

  Ensure MinIO is running with the appropriate credentials.

---

### 7. Finalize and Restart
After configuring the environment variables and connecting MLflow to PostgreSQL, restart the MLflow service/container to apply the changes:

```bash
docker restart mlflow
```

---

### Conclusion:
MLflow is now set up to use PostgreSQL as its backend store and MinIO as an artifact store. You can start tracking machine learning experiments and managing metadata through PostgreSQL. Make sure the necessary environment variables are configured to point to your PostgreSQL and MinIO instances.