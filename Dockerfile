FROM python:3.11-slim-bookworm

WORKDIR /trends-demo

# Install UV via pip
RUN pip install uv

# Copy dependency files first
COPY pyproject.toml uv.lock ./

# Install Python dependencies
RUN uv sync --frozen

# Copy the rest of the project
COPY . .

# Expose port
EXPOSE 8000

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the Django version
RUN echo "Django version:" && uv run python -m django --version

# Run the project, binding Django to all interfaces
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]