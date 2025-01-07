# TrailService Microservice

The **TrailService** microservice is a component of a well-being trail application that promotes outdoor exploration and physical activity. It provides CRUD operations for trails, enforces role-based access control, and integrates with an external Authenticator API for secure user authentication.

## Features
- **CRUD Operations**: Create, read, update, and delete trails.
- **Role-Based Access Control (RBAC)**:
  - Admins have full access to all trails.
  - Standard users can access only their own trails.
- **Secure Authentication**: Utilizes the Authenticator API for validating users.
- **Relational Data Model**:
  - Trails have geospatial data points and associated features.
  - Users own trails and have roles (e.g., "admin" or "user").
- **RESTful API**: JSON-based responses and Swagger documentation.

---

## Installation

### Prerequisites
- Python 3.9+
- Microsoft SQL Server
- Docker (optional, for containerized deployment)

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/finlayandersonplym/COMP2001-TrailService.git
   cd TrailService
   ```

2. **Setup enviroment variable in .env**
    ```
    DB_SERVER=your_db_server
    DB_NAME=your_db_name
    DB_USER=your_db_user
    DB_PASSWORD=your_db_password
    AUTH_API_URL=https://authenticator-api-url
    ```

3. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Initalise and seed database**
    ```bash
    python setup_database.py
    python seed_data.py
    ```

5. **Run application**
    ```bash
    python -m app
    ```

## Docker Installation

1. **Build docker image**
    ```bash
    docker build -t trailservice .
    ```

2. **Run docker container**
    ```bash
    docker run -p 5000:5000 --env-file .env trailservice
    ```
    


