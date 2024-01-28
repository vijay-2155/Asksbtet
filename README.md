 SBTET Community Page

Welcome to the SBTET Community Page GitHub repository! This Django project aims to create an open and collaborative space for individuals associated with the State Board of Technical Education and Training.

## Getting Started

Follow these steps to set up the project locally:

### Prerequisites

1. Make sure you have Python installed on your machine. If not, download and install it from [python.org](https://www.python.org/).

### Setting Up Virtual Environment

1. Clone the repository:
   git clone 
Navigate to the project directory:

cd sbtet-community
Create and activate a virtual environment:


python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Installing Dependencies
Install the project dependencies:

pip install -r requirements.txt
Database Configuration
Open vsem/settings.py.

Locate the DATABASES section and update the database credentials according to your local setup.

Applying Migrations
Run the following Django commands to apply migrations and create the database:


python manage.py migrate
Running the Project
Start the development server:


python manage.py runserver
Open your web browser and go to http://127.0.0.1:8000/ to view the SBTET Community Page.
