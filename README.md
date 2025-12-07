# Flask App with Google OAuth and Calendar API

This repository contains a Flask-based application that integrates Google OAuth for authentication and uses the Google Calendar API to fetch and display events. The app is hosted on an AWS EC2 instance using Docker and can be accessed over the internet.

---

## Features
- User authentication via Google OAuth 2.0.
- Fetch and display events from the user's Google Calendar.
- Deployed on AWS using Docker.
- Accessible over the internet via an Ngrok domain.

---

## Getting Started

### Prerequisites
Ensure the following are installed on your system:
- Python 3.x
- Docker & Docker Compose
- Ngrok (optional for local testing)

---

### Environment Variables
Create a .env file in the project directory with the following variables:

env
GOOGLE_CLIENT_ID=<your-google-client-id>
GOOGLE_CLIENT_SECRET=<your-google-client-secret>
GOOGLE_DISCOVERY_URL=https://accounts.google.com/.well-known/openid-configuration
REDIRECT_URI=http://localhost:5000/callback


---

### Local Development

1. Clone the repository:
    
    bash
    git clone <repository-url>
    cd <repository-directory>
    
    
2. Start the application using Docker Compose:
    
    bash
    docker-compose up --build
    
    
3. Open your browser and visit:
    
    - http://localhost:5000 for local access.
    - Ngrok URL for internet access if configured.

---

### Hosted on AWS

The app is deployed on an AWS EC2 instance with the following details:

- *Public IP*: 15.207.54.193
- *Port*: 5000

Access the hosted app via:

plaintext
http://15.207.54.193:5000


---

## Usage

1. Visit the app's URL (local or hosted).
2. Click the "Login" button to authenticate via Google.
3. View your Google Calendar events on the /events page.
4. Optionally, specify date ranges to filter events.


Note: Only Gmail accounts added as testers in the Google Cloud Console project can successfully authenticate. This is required to comply with Google's OAuth 2.0 policies during the testing phase.

---

## Technologies Used

- *Flask*: Web framework.
- *Google OAuth 2.0*: For authentication.
- *Google Calendar API*: For fetching user calendar events.
- *Docker*: For containerization.
- *AWS EC2*: Hosting environment.
- *Ngrok*: Publicly expose the app during development.

---



---

## Acknowledgements

- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Docker Documentation](https://docs.docker.com/)

