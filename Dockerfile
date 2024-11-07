FROM python:3.11-slim-bookworm

WORKDIR /trends-demo

COPY --from=ghcr.io/astral-sh/uv:0.4.27 /uv /uvx /bin/

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install system dependencies if needed (django maybe)
# RUN apt-get update && apt-get install -y <dependencies> && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN uv sync --frozen

# Copy the project into the image
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the project, binding Django to all interfaces
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]