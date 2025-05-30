import os

def create_env_file():
    env_content = f"""# Azure OpenAI
AZURE_OPENAI_API_KEY=4gM2HRtaDIsFbDjfQQl1DAO1RzN4l2TfAcmkIuC0KgcEjmsEOS9yJQQJ99BBACHYHv6XJ3w3AAAAACOGpcKh
AZURE_OPENAI_ENDPOINT=https://ppbai6350320563.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# Database (using SQLite for development)
DATABASE_URL=sqlite:///./jarvis.db

# Security
SECRET_KEY=your-secret-key-here  # Change this in production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=["http://localhost:3000"]
"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    
    print("Created .env file with Azure OpenAI credentials")

if __name__ == "__main__":
    create_env_file() 