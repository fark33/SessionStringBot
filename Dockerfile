# ====================== Stage 1: Builder ======================
FROM python:3.10.4-slim AS builder

WORKDIR /app

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# کپی فایل‌های وابستگی
COPY requirements.txt .

# نصب پکیج‌ها
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# ====================== Stage 2: Production ======================
FROM python:3.10.4-slim

WORKDIR /app

# نصب runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# کپی پکیج‌های نصب شده از builder
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# کپی کد پروژه
COPY . .

# ایجاد دایرکتوری لاگ
RUN mkdir -p logs && chmod 777 logs

# متغیرهای محیط
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

# پورت (در صورت نیاز)
EXPOSE 8080

# دستور اجرا
CMD ["python3", "-m", "ssnbot"]
