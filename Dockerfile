FROM python:3.10-slim

# Copy files to image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY tg_biblebot/. ./
COPY requirements.txt ./

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run gunicorn to serve the bot - timeout set to 0 so Google Cloud Run can handle scaling
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app