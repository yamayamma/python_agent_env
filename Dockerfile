# 1. Base stage for Python and uv setup
FROM python:3.12-slim as base

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    UV_LINK_MODE=copy

# Install uv
RUN pip install uv

WORKDIR /app

# 2. Builder stage for installing dependencies
FROM base as builder

COPY pyproject.toml uv.lock ./

# Install all dependencies (including dev)
RUN uv sync --system --extra dev

# 3. Development stage
FROM builder as development

COPY . .

CMD ["sleep", "infinity"]

# 4. Production stage
FROM builder as production

# Install only production dependencies
RUN uv sync --system

COPY src/ /app/src/

# Set the entrypoint to the application
ENTRYPOINT ["python-agent-env"]

