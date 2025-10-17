from google.cloud import secretmanager

# CONFIGURE PROJECT AND SECRETS 
PROJECT_ID = "ai-agent-boilerplate0"  
SECRET_MAPPING = {
    "GROQ_API_KEY": "GROQ_API_KEY",           
    "POSTGRES_PASSWORD": "POSTGRES_PASSWORD"
}
ENV_FILE_PATH = ".env"

def access_secret(secret_id: str, project_id: str, version_id: str = "latest") -> str:
    client = secretmanager.SecretManagerServiceClient()
    secret_path = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": secret_path})
    return response.payload.data.decode("UTF-8")

def generate_env_file(secrets: dict, env_path: str = ".env"):
    # Template for the entire .env file
    env_content = f"""DEBUG=True
GROQ_API_KEY={secrets['GROQ_API_KEY']}
GROQ_MODEL_NAME=meta-llama/llama-4-scout-17b-16e-instruct

# PostgreSQL Database Configuration
DATABASE_URL=postgresql://postgres:{secrets['POSTGRES_PASSWORD']}@localhost:5432/
"""

    with open(env_path, "w") as f:
        f.write(env_content)
    print(f"✅ Generated {env_path} with all secrets.")

if __name__ == "__main__":
    secrets = {}
    for env_var, gcp_secret_name in SECRET_MAPPING.items():
        value = access_secret(gcp_secret_name, PROJECT_ID)
        secrets[env_var] = value

    generate_env_file(secrets, ENV_FILE_PATH)
