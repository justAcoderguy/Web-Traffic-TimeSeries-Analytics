# Set the python version as a build-time argument
# with Python 3.12 as the default
FROM python:3.13.9-slim-trixie

# Create a virtual environment
RUN python -m venv /opt/venv

# Set the virtual environment as the current location
ENV PATH=/opt/venv/bin:$PATH

# Upgrade pip
RUN pip install --upgrade pip

# Install Poetry
RUN pip install poetry

# Configure Poetry to not create a virtual environment (we're using the venv we created)
ENV POETRY_VENV_IN_PROJECT=false
ENV POETRY_NO_INTERACTION=1
ENV POETRY_CACHE_DIR=/tmp/poetry_cache

# Explicitly tell Poetry to use the existing venv and not create new ones
RUN poetry config virtualenvs.create false

# Set Python-related environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install os dependencies for our mini vm
RUN apt-get update && apt-get install -y \
    # for postgres
    libpq-dev \
    # for Pillow
    libjpeg-dev \
    # for CairoSVG
    libcairo2 \
    # other
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Create the mini vm's code directory
RUN mkdir -p /code

# Set the working directory to that same code directory
WORKDIR /code

# Copy Poetry configuration files
COPY pyproject.toml poetry.lock ./

# Install the Python project dependencies using Poetry
# Poetry will automatically detect and use the venv at /opt/venv because PATH is set
RUN poetry install --no-interaction --no-root && rm -rf $POETRY_CACHE_DIR

# copy the project code into the container's working directory
COPY ./src /code

# make the bash script executable
COPY ./boot/docker-run.sh /opt/run.sh
RUN chmod +x /opt/run.sh

# Clean up apt cache to reduce image size
RUN apt-get remove --purge -y \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Run the FastAPI project via the runtime script
# when the container starts
CMD ["/opt/run.sh"]