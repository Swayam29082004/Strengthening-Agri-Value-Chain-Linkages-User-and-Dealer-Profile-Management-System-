# User and Dealer Profile Management System

## Overview
This project is a web application built with Flask that allows users and dealers to create accounts, log in, and manage their profiles. It serves as a platform to connect users with dealers, facilitating communication and interaction.

## Features
- User and dealer account creation and authentication
- Profile management with the ability to upload profile pictures and documents
- Dashboards tailored for user and dealer profiles
- Responsive design for accessibility on various devices

## Technologies Used
- **Flask**: Web framework for building the application
- **JSON**: Data storage format for user and dealer information
- **Werkzeug**: Library for secure filename handling during uploads
- **HTML/CSS**: Frontend technologies for rendering templates

## Installation
To set up the project locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/project-name.git
   cd project-name


project-name/
│
├── app.py                    # Main application file
├── static/                   # Static files (CSS, JS, Images)
│   └── uploads/              # Uploaded profile pictures and documents
├── templates/                # HTML templates for rendering
│   ├── index.html
│   ├── login.html
│   ├── create_account.html
│   ├── complete_profile_user.html
│   ├── complete_profile_dealer.html
│   ├── user_dashboard.html
│   └── dealer_dashboard.html
└── data/                     # JSON files for user and dealer data
    ├── users.json
    └── dealers.json
