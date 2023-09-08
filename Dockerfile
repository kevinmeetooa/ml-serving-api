FROM python:3.10-slim-bullseye

# Copy code
COPY src /src

# Install requirements
RUN pip install -r src/requirements.txt

# Expose the port the application will run on
EXPOSE 5000

# Run the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "--timeout", "120", "src.api.api:app"]
