# Virtual Pet API

This project is a FastAPI backend for a virtual pet mobile application written in kotlin. It provides a set of APIs to manage users and their virtual pets, including functionalities for creating users, logging in, and managing pets' attributes like hunger and happiness. The application uses a PostgreSQL database for data persistence and SQLAlchemy for ORM.

## Project Structure

The project is organized into the following directories:

- **Config**: Contains the database configuration, including the SQLAlchemy engine and session management.
- **Model**: Defines the SQLAlchemy ORM models for the `users` and `mascotas` (pets) tables.
- **Routers**: Contains the API endpoints for users and pets, defining the application's routes and business logic.
- **Schemas**: Defines the Pydantic models for data validation and serialization, ensuring that the API receives and returns data in the correct format.

## API Endpoints

The application exposes the following endpoints:

### User Endpoints

- `POST /users/`: Creates a new user.
- `GET /users/`: Retrieves a list of all users.
- `POST /users/login`: Authenticates a user and returns a token.

### Pet Endpoints

- `POST /mascotas/{user_id}`: Creates a new pet for a specific user.
- `GET /mascotas/{user_id}`: Retrieves all pets belonging to a specific user.
- `GET /mascotas/{user_id}/{mascota_id}`: Retrieves a specific pet by its ID.
- `PUT /mascotas/{user_id}/{mascota_id}`: Updates a pet's information.
- `DELETE /mascotas/{user_id}/{mascota_id}`: Deletes a pet.

## Getting Started

### Prerequisites

- Python 3.8+
- PostgreSQL

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/castro-bot/Virtual-Pet-Backend.git
   cd Virtual-Pet-Backend
   ```

2. **(Optional) Create and activate a virtual environment:**

   ```bash
   python -m venv env
   source env/bin/activate  # On Windows, use `env\Scripts\activate`
   ```

3. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   - Create a `.env` file in the root directory.
   - Add your PostgreSQL connection string to the `.env` file:

     ```
     DATABASE_URL="postgresql://user:password@host:port/database"
     ```

### Running the Application

To run the application, execute the following command:

```bash
uvicorn main:app --reload
```

For development, you can run the application with auto-reloading, which will automatically restart the server when code changes are detected.

If you need to make the application accessible over your local network, use the following command:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Using Ngrok for Public Access

If you need to expose your local server to the internet, you can use `ngrok`.

1. **Install ngrok:**

   Follow the instructions on the [ngrok website](https://ngrok.com/download) to download and install it.

2. **Run ngrok:**

   ```bash
   ngrok http http://localhost:8000
   ```

This will provide you with a public URL that forwards to your local server, which is useful for testing webhooks or sharing your development server with others.
