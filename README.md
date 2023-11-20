[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/2sZOX9xt)
# Log Search Application

This is a Flask-based web application for logging and searching logs in MongoDB and MySQL databases.

## Features Implemented

1. **Log Ingestion:**
   - Ingest logs from JSON data received in the POST request.
   - Determine data size using `get_data_size` function.
   - Conditionally store logs in either MongoDB or MySQL based on data size.

2. **MongoDB Error Handling:**
   - Log MongoDB-specific errors.
   - If MongoDB insertion fails, attempt to add the data to MySQL.

3. **MySQL Log Ingestion:**
   - If MongoDB insertion fails or if the data size is small, add logs to MySQL.
   - Log MySQL-specific errors.

4. **Search Logs:**
   - Retrieve all logs for the GET request.
   - Build a query based on the form data for the POST request.
   - Search logs in MongoDB and handle MongoDB-specific errors.
   - If MongoDB search fails, attempt to fetch data from MySQL and handle MySQL-specific errors.

5. **Query Building:**
   - Build a query based on the form data for timestamp, message, and other search criteria.

6. **Error Handling:**
   - Log general errors during log ingestion and log search.

7. **Timestamp for Error Logging:**
   - Include a timestamp in error logs for better identification of when errors occur.

8. **Redirect to Ingest:**
   - Redirect to the log ingestion page when accessing the root URL.


## System Design

The system uses Flask as the web framework, MongoDB for storing large logs, and MySQL for smaller logs. The application follows a microservices architecture to handle different database backends efficiently.

## How to Run

### Prerequisites

1. Python (3.7 or higher)
2. MongoDB
3. MySQL

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/dyte-submissions/november-2023-hiring-Devbijwe.git
    cd november-2023-hiring-Devbijwe
    ```

2. Create a virtual environment:

    ```bash
    python -m venv venv
    ```

3. Activate the virtual environment:

    - On Windows:

        ```bash
        venv\Scripts\activate
        ```

    - On macOS/Linux:

        ```bash
        source venv/bin/activate
        ```

4. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Configuration

1. Set up MySQL:

    - Create a MySQL database.
    - Update the `SQLALCHEMY_DATABASE_URI` in `app.py` with your MySQL database connection details.

2. Set up MongoDB:

    - Create a MongoDB cluster.
    - Update the `mongo_uri` in `app.py` with your MongoDB connection string.
3. Set up MONGODB_THRESHOLD:

    - MONGODB_THRESHOLD is initially set to 0.
    - Update the `MONGODB_THRESHOLD` after creating MySql DB.
### Run the Application

```bash
python app.py

- The app will be accessible at http://localhost:3000 in your web browser.
 
## Usage

  - Navigate to http://localhost:3000/ingest to submit log entries.
  - Visit http://localhost:3000/search to search and filter logs.


# Identified Issues

1. **Error Handling Consistency:**
   - Error handling is present, but there is room for consistency improvement. Ensure that errors are consistently logged and handled across different components.

2. **Database Connection Configuration:**
   - Database connection details are hardcoded in the `app.py` file. Consider using environment variables or a configuration file for a more secure and flexible setup.

3. **Data Size Calculation:**
   - The `get_data_size` function currently calculates the size based on the string length of the data. For more accurate results, consider implementing a more robust size calculation method.

4. **Handling Large Data in MySQL:**
   - When dealing with large data in MySQL, consider optimizing the schema, indexing, and pagination to enhance performance.

5. **Web Interface Styling:**
   - The web interface could benefit from improved styling for better user experience.

6. **Security Considerations:**
   - Ensure that the application follows security best practices, especially when dealing with user input and database connections.

7. **Documentation Completeness:**
   - The README provides basic instructions, but consider expanding it to include more detailed information on dependencies, environment setup, and troubleshooting.

8. **Consistent Logging:**
   - Log messages across the application could be standardized for better readability and debugging.

9. **Testing:**
   - Consider implementing unit tests and integration tests to ensure the robustness of the application.

10. **Pagination for Search Results:**
    - Implement pagination for search results to improve performance when dealing with a large number of logs.

11. **Handling Concurrent Requests:**
    - Evaluate and optimize the application's ability to handle concurrent requests, especially during log ingestion and search operations.

12. **Database Existence Check:**
    - Currently, the application assumes the existence of both MongoDB and MySQL databases. Implement checks to handle cases where one or both databases may not exist.

13. **Graceful Shutdown:**
    - Implement a mechanism for graceful shutdown of the application to ensure data integrity.

14. **Input Validation:**
    - Implement input validation to prevent potential security vulnerabilities.
