# Employee Leave Visualization System

## Project Overview

The Employee Leave Visualization System is a comprehensive application designed to manage and visualize employee leave data. It consists of a Flask backend to handle API requests, a PostgreSQL database for data storage, and a Streamlit frontend for data visualization.

## Features

- API endpoints to fetch employee and leave data
- Data ingestion from external sources (API and bulk file uploads)
- Visualization of leave data using Streamlit
- Dockerized setup for easy deployment

## Project Structure

leave-visualization-app/
├── alembic/
│ ├── versions/
│ └── env.py
├── app/
│ ├── init.py
│ ├── models.py
│ ├── api.py
│ └── views.py
├── migrations/
├── static/
├── templates/
├── tests/
├── .env
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── config.py
├── run.py
├── setup.py
└── README.md


## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Steps

1. **Clone the Repository:**

    ```sh
    git clone https://github.com/yourusername/leave-visualization-app.git
    cd leave-visualization-app
    ```

2. **Environment Configuration:**

    Create a `.env` file in the project root directory and add the following:

    ```env
    DATABASE_URL=postgresql://root:leave@visualization123@db/leave_visualization
    ```

3. **Build and Run Docker Containers:**

    ```sh
    docker-compose up --build
    ```

4. **Run Database Migrations:**

    ```sh
    docker-compose exec app flask db init
    docker-compose exec app flask db migrate -m "Initial migration."
    docker-compose exec app flask db upgrade
    ```

5. **Access the Flask API:**

    Open your browser and navigate to `http://localhost:8000/api/employees` and `http://localhost:8000/api/leaves` to verify the Flask API endpoints.

6. **Run the Streamlit App:**

    Open a new terminal and navigate to the project directory. Then run:

    ```sh
    streamlit run streamlit_app.py
    ```

    Open your browser and navigate to the Streamlit app URL provided in the terminal (typically `http://localhost:8501`).

## API Endpoints

- **GET /api/employees**: Retrieve all employees
- **GET /api/leaves**: Retrieve all leave requests

## Visualizations in Streamlit

- **Leave Types Distribution**: Bar chart showing the distribution of different types of leave.
- **Leaves by Department**: Bar chart showing the number of leaves taken in each department.
- **Leaves by Month**: Line chart showing the number of leaves taken each month.
- **Leave Status Distribution**: Pie chart showing the distribution of leave statuses.

## Contributing

Contributions are welcome! Please create a pull request or open an issue to discuss changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
