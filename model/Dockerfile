FROM python:3.9-slim-bullseye

RUN mkdir -p /model

WORKDIR /model

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY patternmining.py .

RUN mkdir -p /pickle

# Run the rule generation script
CMD ["python", "patternmining.py"]
