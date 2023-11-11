FROM python:3.11.5

# Update pip and Install pipenv
RUN pip install --upgrade pip && pip install pipenv

# Copy Pipfile and Pipfile.lock to container
COPY Pipfile* /tmp/

# Install from lock file
RUN cd /tmp && pipenv install --system --deploy --ignore-pipfile

# Copy project files to container, except those in .dockerignore
COPY ./ticker_trace /app


# Set working directory
WORKDIR /app

# Run the application using uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--reload"]
