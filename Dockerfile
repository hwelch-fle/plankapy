# Use the official Python image
FROM python:3.13-slim

# Move plankapy to the container
COPY ./src /plankapy/src
COPY ./pyproject.toml /plankapy

# Update pip
RUN pip install --upgrade pip

# Install latest plankapy
RUN pip install /plankapy

# Create a directory for scripts
RUN mkdir /scripts

# Set the working directory to the scripts directory
WORKDIR /scripts

# Expose the scripts directory
VOLUME /scripts

# Set the entrypoint to terminal
ENTRYPOINT ["bash"]

# Set the default command to print the Plankapy version
CMD ["plankapy", "--version"]

# End of Dockerfile