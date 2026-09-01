# =========================
# Stage 1: Builder
# =========================
FROM python:3.12-slim AS builder

WORKDIR /app

# Create a virtual environment
RUN python -m venv /opt/venv

# Make the virtual environment the default
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


# =========================
# Stage 2: Production
# =========================
FROM python:3.12-slim

WORKDIR /app

# Copy only the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Copy application
COPY app.py .

EXPOSE 5000

CMD ["python", "app.py"]