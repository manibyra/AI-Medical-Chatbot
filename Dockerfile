FROM python:3.9

# Create user
RUN useradd -m -u 1000 user
USER user
ENV PATH="/home/user/.local/bin:$PATH"

# Set working directory
WORKDIR /app

# Install requirements
COPY --chown=user ./requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy source
COPY --chown=user . /app

# Expose required port
EXPOSE 7860

# Run your Flask app
CMD ["python", "app.py"]
