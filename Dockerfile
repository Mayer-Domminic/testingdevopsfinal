FROM python:3.11.9-slim

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

CMD ["coverage", "run", "-m", "unittest", "discover", "-s", "tests"]