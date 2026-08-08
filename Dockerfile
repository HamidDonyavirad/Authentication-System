FROM python:3.14-slim AS builder

WORKDIR /app

RUN python -m venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


FROM python:3.14-slim AS runtime

WORKDIR /app

RUN addgroup --system appgroup && \
    adduser --system --ingroup appgroup appuser

COPY --from=builder /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"

COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]