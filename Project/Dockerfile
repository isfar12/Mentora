# Step 1: Use a lightweight Python base image
# Why: Python 3.11 is required for your project, and the slim version reduces image size.
FROM python:3.11-slim

# Step 2: Set the working directory inside the container
# Why: Keeps the application files organized inside the container.
WORKDIR /app

# Step 3: Copy the app folder into the container
# Why: To install the necessary Python dependencies.
COPY . /app

# Step 4: Install the dependencies
# Why: Ensures all required libraries are available for the application.
RUN pip install -r requirements.txt

# Step 5: Copy the application code into the container
# Why: To make the application code accessible inside the container.
COPY . .

# Step 6: Expose the port Streamlit runs on (default is 8501)
# Why: Allows the application to be accessible from outside the container.
EXPOSE 8501

# Step 7: Define the command to run the Streamlit app
# Why: Specifies the entry point for the container to start the application.
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
