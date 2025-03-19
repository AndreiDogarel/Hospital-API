# Hospital API

## Description
Hospital API is a RESTful application for managing doctors, patients, assistants, and treatments in a hospital. The API allows user management with different roles and includes advanced functionalities such as detailed reports and JWT authentication.

## Features
- Authentication and authorization using JWT
- User management: General Manager, Doctors, Assistants, Patients
- CRUD operations for Doctors, Patients, Assistants, and Treatments
- Assigning patients to assistants
- Applying treatments only by assistants
- Detailed reports:
  - List of doctors and their patients
  - List of treatments applied to a patient
- API documentation generated with OpenAPI
- Deployment with Docker and PostgreSQL

## Installation and Setup

### Clone the repository
```sh
git clone https://github.com/username/hospital-api.git
cd hospital-api
```

### Local setup (without Docker)

#### Install dependencies
```sh
pip install -r requirements.txt
```

#### Apply migrations and create a superuser
```sh
python manage.py migrate
python manage.py createsuperuser
```

#### Start the server
```sh
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`

### Running with Docker

#### Build and run containers
```sh
docker-compose up --build -d
```

#### Apply migrations inside the container
```sh
docker-compose exec django python manage.py migrate
```

The API will be available at `http://127.0.0.1:8000/`

To stop the containers:
```sh
docker stop $(docker ps -q)
```

## API Documentation

All API calls have been tested using Postman to ensure correct functionality and proper authentication handling.
Swagger UI is available at:
```
http://127.0.0.1:8000/api/docs/
```

### Main Endpoints
| Method  | Endpoint | Description |
|---------|---------|-------------|
| `POST`  | `/api/token/` | Obtain JWT token |
| `POST`  | `/api/token/refresh/` | Refresh JWT token |
| `GET`   | `/api/doctors/` | List all doctors |
| `POST`  | `/api/doctors/` | Create a doctor (GM only) |
| `GET`   | `/api/patients/` | List all patients (Doctor, GM) |
| `POST`  | `/api/treatments/` | Create a treatment (Doctor, GM) |
| `PATCH` | `/api/treatments/{id}/apply-treatment/` | Apply treatment (Assistant) |
| `GET`   | `/api/reports/doctors/` | Doctor-Patient report (GM) |
| `GET`   | `/api/reports/patient/{patient_id}/treatments/` | Patient treatment report (Doctor, GM) |

## Project Structure
```plaintext
hospital_api/
│── core/                    # Main application
│   ├── models.py            # Database models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # ViewSets and API logic
│   ├── permissions.py       # Custom permissions
│── hospital_api/
│   ├── settings.py          # Django configuration
│── docker-compose.yml       # Docker configuration
│── Dockerfile               # Docker build configuration
│── requirements.txt         # Python dependencies
│── manage.py                # Django management commands
```

## Authentication and Permissions
- **General Manager (GM)**: Full access to all users and reports
- **Doctor**: Can manage patients and prescribe treatments
- **Assistant**: Can apply prescribed treatments

For authentication, use the JWT token in the request header:
```http
Authorization: Bearer YOUR_ACCESS_TOKEN
```