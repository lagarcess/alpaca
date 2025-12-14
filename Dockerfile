# Stage 1: Builder
# We use a full Python image to make sure we have all build tools avail or easily installable
FROM python:3.11-slim as builder

# Install system dependencies required for building ta-lib and python packages
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    make \
    wget \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Download and compile TA-Lib C library
# We install to /usr so the libraries end up in /usr/lib and headers in /usr/include
WORKDIR /tmp
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install

# Install Poetry
RUN pip install poetry

# Setup project directory
WORKDIR /app

# Copy poetry files
COPY pyproject.toml poetry.lock ./

# Configure poetry to create venv in project so we can copy it easily
RUN poetry config virtualenvs.in-project true

# Install dependencies (this will compile the ta-lib python wrapper against the installed C lib)
RUN poetry install --without dev --no-root

# Stage 2: Final Runtime
FROM python:3.11-slim

# Copy compiled TA-Lib C libraries from builder
COPY --from=builder /usr/lib/libta_lib* /usr/lib/

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Update Environment variables
# Add venv bin to PATH so 'python' calls use the venv
ENV PATH="/app/.venv/bin:$PATH"
# Ensure the dynamic linker finds the ta-lib libraries (often not needed if in /usr/lib, but good safety)
ENV LD_LIBRARY_PATH="/usr/lib:$LD_LIBRARY_PATH"

# Ensure Python can import the package in `src/` when run the copied application
# without installing the project into site-packages. This makes `from market_data...` work.
ENV PYTHONPATH="/app/src:$PYTHONPATH"

WORKDIR /app

# Copy application code
COPY src ./src
COPY main.py .

# Entrypoint
ENTRYPOINT ["python", "main.py"]
