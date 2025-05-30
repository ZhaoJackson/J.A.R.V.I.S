# J.A.R.V.I.S - Your Personal Life Assistant

JARVIS (Just A Rather Very Intelligent System) is a personal assistant that combines computer vision and workflow automation to help you manage your daily activities.

## Features

- **Computer Vision + LLM Integration**: Real-time activity detection and intelligent responses
- **N8N Workflow Integration**: Automated data collection and processing from various web sources

## Tech Stack

- Frontend: Next.js with TypeScript
- Backend: FastAPI (Python)
- Vision: OpenCV + ResNet-50
- AI: Azure OpenAI GPT-4
- Workflow Automation: N8N
- Styling: Tailwind CSS

## Getting Started

1. Clone the repository
2. Install dependencies:
   ```bash
   # Backend
   pip install -r requirements.txt
   
   # Frontend
   npm install
   ```
3. Set up environment variables:
   ```bash
   cp .env.example .env.local
   ```
4. Run the development servers:
   ```bash
   # Backend
   uvicorn backend.main:app --reload
   
   # Frontend
   npm run dev
   ```

## Environment Variables

Create a `.env.local` file with the following variables:

```
# Azure OpenAI
AZURE_OPENAI_API_KEY=your_gpt4_api_key
AZURE_OPENAI_ENDPOINT=your_azure_endpoint
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_DEPLOYMENT=gpt-4o

# N8N Integration
N8N_WEBHOOK_URL=http://localhost:5678
N8N_API_KEY=your_n8n_api_key

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Project Structure

```
├── backend/
│   ├── routers/          # API endpoints
│   │   ├── vision.py     # Vision and LLM integration
│   │   └── n8n.py        # N8N workflow integration
│   └── services/         # Business logic
│       ├── vision_service.py
│       └── n8n_service.py
├── src/
│   ├── components/       # React components
│   │   ├── VisionChat.tsx
│   │   └── N8NWorkflow.tsx
│   └── app/             # Next.js app directory
└── public/             # Static assets
```

## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

MIT