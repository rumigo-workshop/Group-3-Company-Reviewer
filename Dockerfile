FROM node:22-alpine

# Install Python and pip
RUN apk add --no-cache python3 py3-pip

WORKDIR /app

# Install backend dependencies
COPY packages/api/requirements.txt ./api/requirements.txt

RUN python3 -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r ./api/requirements.txt

# Install frontend dependencies
COPY packages/web/React_Project/package*.json ./frontend/

WORKDIR /app/frontend

RUN npm ci

# Copy application source code
WORKDIR /app

COPY packages/api/ ./api/
COPY packages/web/React_Project/ ./frontend/

# Expose frontend and backend ports
EXPOSE 5173 8000

# Start both applications
CMD ["sh", "-c", "cd /app/api && python -m uvicorn main:app --host 0.0.0.0 --port 8000 & cd /app/frontend && npm run dev -- --host 0.0.0.0"]
