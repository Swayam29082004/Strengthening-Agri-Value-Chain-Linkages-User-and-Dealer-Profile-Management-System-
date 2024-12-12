// Function to handle login form submission
async function handleLoginFormSubmit(event) {
    event.preventDefault();
    
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const loginType = document.querySelector('input[name="login_type"]:checked').value;

    try {
        const response = await fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password,
                login_type: loginType
            })
        });

        if (response.redirected) {
            window.location.href = response.url;
        } else {
            const result = await response.text();
            document.getElementById("login-message").textContent = "Invalid username or password.";
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("login-message").textContent = "An error occurred. Please try again.";
    }
}

// Function to handle account creation form submission
async function handleCreateAccountFormSubmit(event) {
    event.preventDefault();
    
    const username = document.getElementById("new-username").value;
    const password = document.getElementById("new-password").value;
    const confirmPassword = document.getElementById("confirm-password").value;
    const accountType = document.getElementById("account-type").value;

    if (password !== confirmPassword) {
        document.getElementById("create-account-message").textContent = "Passwords do not match.";
        return;
    }

    try {
        const response = await fetch('/create_account', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                username: username,
                password: password,
                confirm_password: confirmPassword,
                profile_type: accountType
            })
        });

        if (response.ok) {
            document.getElementById("create-account-message").textContent = "Account created successfully! Please log in.";
            document.getElementById("create-account-form").reset();
        } else {
            const result = await response.text();
            document.getElementById("create-account-message").textContent = result;
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById("create-account-message").textContent = "An error occurred. Please try again.";
    }
}

// Function to open the popup and fetch user or dealer details
async function openPopup(id, type) {
    const popup = document.getElementById('popup');
    const popupContent = document.querySelector('.popup-content .user-details');
    
    popup.style.display = 'flex';

    try {
        const response = await fetch(`/${type}/${id}`);
        const data = await response.json();

        if (data.error) {
            popupContent.innerHTML = `<p>${data.error}</p>`;
        } else {
            if (type === 'dealer') {
                popupContent.innerHTML = `
                    <h2>${data.profile.full_name}</h2>
                    <p><strong>Email:</strong> ${data.profile.email}</p>
                    <p><strong>Phone:</strong> ${data.profile.phone}</p>
                    <p><strong>Organization:</strong> ${data.profile.organization_name}</p>
                    <p><strong>Address:</strong> ${data.profile.organization_address}</p>
                    <p><strong>Location:</strong> ${data.profile.location}</p>
                    <p><strong>Business Type:</strong> ${data.profile.business_type}</p>
                    <p><strong>Products Interested:</strong> ${data.profile.products_interested}</p>
                    <p><strong>GST No:</strong> ${data.profile.gst_no}</p>
                    <p><strong>Profile Picture:</strong><br><img src="${data.profile.profile_picture}" alt="Profile Picture" class="popup-pic"></p>
                    <p><strong>Certified Documents:</strong><br><img src="${data.profile.certified_documents}" alt="Certified Documents" class="popup-doc"></p>
                `;
            } else if (type === 'user') {
                popupContent.innerHTML = `
                    <img src="${data.profile_picture}" alt="User Picture" class="popup-pic">
                    <div class="details">
                        <p><strong>Email:</strong> ${data.email}</p>
                        <p><strong>Phone:</strong> ${data.phone}</p>
                        <p><strong>Address:</strong> ${data.address}</p>
                        <p><strong>Farm Size:</strong> ${data.farm_size}</p>
                        <p><strong>Products:</strong> ${data.products}</p>
                    </div>
                `;
            }
        }
    } catch (error) {
        console.error('Error fetching data:', error);
        popupContent.innerHTML = `<p>Unable to fetch details.</p>`;
    }
}

// Function to close the popup
function closePopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'none';
}

// Initialize event listeners
function initEventListeners() {
    document.querySelectorAll('.view-more').forEach(link => {
        link.addEventListener('click', (event) => {
            event.preventDefault();
            const id = link.getAttribute('data-user-id') || link.getAttribute('data-dealer-id');
            const type = link.getAttribute('data-user-id') ? 'user' : 'dealer';
            openPopup(id, type);
        });
    });

    document.querySelector('.popup-content .close')?.addEventListener('click', closePopup);

    document.getElementById('popup')?.addEventListener('click', (event) => {
        if (event.target === document.getElementById('popup')) {
            closePopup();
        }
    });

    document.querySelector('.popup-content .sell-button')?.addEventListener('click', () => {
        confirm("Your contract is done with this dealer.");
    });
    document.querySelector('.popup-content .buy-button')?.addEventListener('click', () => {
        confirm("Your contract is done with this user.");
    });
}

// Function to redirect to the home page
function redirectToHome() {
    window.location.href = '/';  // Redirects to the home page (root of the site)
}

// Initialize event listener for the image
function initImageClick() {
    const logoImg = document.getElementById('logo-img');
    if (logoImg) {
        logoImg.addEventListener('click', redirectToHome);
    }
}

// Wait for the DOM to fully load before initializing event listeners
document.addEventListener('DOMContentLoaded', initImageClick);

// Wait for the DOM to fully load before initializing event listeners
document.addEventListener('DOMContentLoaded', initEventListeners);
