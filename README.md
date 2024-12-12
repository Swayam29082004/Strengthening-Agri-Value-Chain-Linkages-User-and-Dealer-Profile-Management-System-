# User and Dealer Profile Management System 🌐

Welcome to the **User and Dealer Profile Management System**! A modern web application built with Flask that seamlessly connects users and dealers. Users can create accounts, manage profiles, upload documents, and much more. Dealers can engage with users, creating a dynamic interaction platform. Whether you’re on a desktop or mobile, this responsive app ensures a smooth experience everywhere.

## ⚙️ Features

- **Account Creation & Authentication**: Quick and easy account sign-ups for both users and dealers.
- **Profile Management**: Upload your profile picture, documents, and manage personal details effortlessly.
- **Dashboards**: Unique dashboards for both users and dealers to interact with the platform and update their profiles.
- **Responsive Design**: Designed for a sleek experience on all devices, from desktops to smartphones.

## 🚀 Technologies Used

- **Flask**: The lightweight web framework that powers the backend.
- **JSON**: Storing user and dealer data in a simple and efficient format.
- **Werkzeug**: Ensures secure handling of file uploads (profile pics, documents, etc.).
- **HTML/CSS**: Crafting beautiful and responsive web pages.

## 💻 Installation

To run this project locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/project-name.git
    cd project-name
    ```

2. **Install the Requirements**:
    Make sure you have Python installed and then install the dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. **Run the Application**:
    Start the Flask server and see your app in action:
    ```bash
    python app.py
    ```

4. **Access the Application**:
    Open your browser and navigate to [http://localhost:5000](http://localhost:5000).

## 📁 Project Structure

Here's the breakdown of the project directory:

```bash
project-name/
  ├── app.py                   # Main application file
  ├── static/                  # Static files (CSS, JS, Images)
  │   └── uploads/             # Uploaded profile pictures and documents
  ├── templates/               # HTML templates for rendering
  │   ├── index.html           # Landing page
  │   ├── login.html           # Login page
  │   ├── create_account.html  # Account creation form
  │   ├── complete_profile_user.html  # User profile completion
  │   ├── complete_profile_dealer.html # Dealer profile completion
  │   ├── user_dashboard.html  # User's dashboard
  │   └── dealer_dashboard.html # Dealer's dashboard
  └── data/                    # JSON files for user and dealer data
      ├── users.json           # Store for user data
      └── dealers.json         # Store for dealer data
```

## 🔐 Authentication

- **User Login/Signup**: Users can sign up, log in, and manage their profile from their personalized dashboard.
- **Dealer Login/Signup**: Dealers can also create accounts, upload their profiles, and interact with users.

## 🖼️ Profile Management

Users and dealers can upload profile pictures and documents, with secure file handling in place to ensure safety and integrity. The profiles are stored in the `static/uploads/` directory.

## 🌱 Contributions

We welcome contributions to improve and enhance this platform. If you have suggestions or improvements, feel free to fork the repo and submit a pull request!

## 👨‍💻 License

This project is open-source and licensed under the MIT License. See [LICENSE](LICENSE) for details.

Enjoy managing your profiles like a pro with this sleek, user-friendly system! 😎
