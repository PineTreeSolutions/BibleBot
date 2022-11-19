FROM python:3.11

# Copy files to image
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run gunicorn to serve the bot
CMD exec gunicorn --bind 127.0.0.1:$PORT --workers 1 --threads 8 main:app