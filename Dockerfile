FROM python:3.11-slim as stage0

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update ; \
    apt-get install -y --no-install-recommends \
        gcc \
        g++ \
        vim

COPY requirements.txt /python_requirements/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /python_requirements/requirements.txt

COPY app/ /app/

# ------------ final -----------------------

FROM stage0 as final

CMD ["python3", "-m", "app.main"]
