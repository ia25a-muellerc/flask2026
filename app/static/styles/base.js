const logo = document.querySelector(".logo");
const logoText = document.querySelector(".logo-text");

logo.addEventListener("click", ()=>{
    window.location.href = "/";
});

logoText.addEventListener("click", ()=>{
    window.location.href = "/";
});

// Profile Hover Menu
document.addEventListener('DOMContentLoaded', function() {
    const profileContainer = document.querySelector('.nav-profile-container');
    const profileMenu = document.getElementById('profileMenu');
    let hideTimeout;

    if (profileContainer && profileMenu) {
        profileContainer.addEventListener('mouseenter', function() {
            clearTimeout(hideTimeout);

            // Fetch user data
            fetch('/api/user')
                .then(response => response.json())
                .then(data => {
                    const userInfo = document.getElementById('userInfo');
                    if (data.logged_in) {
                        const surname = data.surname ? ` ${data.surname}` : '';
                        userInfo.innerHTML = `
                            <div style="padding: 10px; background: #f5f5f5; border-radius: 4px; min-width: 200px;">
                                <p style="margin: 5px 0; font-weight: bold; color: #333;">${data.name}${surname}</p>
                                <p style="margin: 5px 0; font-size: 0.9em; color: #666;">${data.email}</p>
                                <hr style="margin: 10px 0; border: none; border-top: 1px solid #ddd;">
                                <a href="/profile" style="display: block; color: #333; text-decoration: none; padding: 5px 0; margin: 5px 0;">My Profile</a>
                                <a href="/logout" style="display: block; color: #d32f2f; text-decoration: none; padding: 5px 0; margin: 5px 0;">Logout</a>
                                <a href="/orders" style="display: block; color: #333; text-decoration: none; padding: 5px 0; margin: 5px 0;">My Orders</a>
                            </div>
                        `;
                    } else {
                        userInfo.innerHTML = '<a href="/signin" style="color: #fff; background: #f58800; text-decoration: none; padding: 8px 20px; border-radius: 6px; font-size: 0.9em; font-weight: 500; transition: all 0.2s ease; display: inline-block;">Sign In</a>';
                    }
                    profileMenu.style.display = 'block';
                })
                .catch(err => {
                    console.error('Error fetching user:', err);
                    profileMenu.style.display = 'block';
                });
        });

        // Menü auch sichtbar halten wenn Maus über Menü selbst fährt
        profileMenu.addEventListener('mouseenter', function() {
            clearTimeout(hideTimeout);
            profileMenu.style.display = 'block';
        });

        // Nur verstecken wenn Maus Container UND Menü verlässt
        profileContainer.addEventListener('mouseleave', function() {
            hideTimeout = setTimeout(function() {
                profileMenu.style.display = 'none';
            }, 100);
        });

        profileMenu.addEventListener('mouseleave', function() {
            hideTimeout = setTimeout(function() {
                profileMenu.style.display = 'none';
            }, 100);
        });
    }
});

// Password visibility toggle
// Uses event delegation so it works across pages without inline scripts.
document.addEventListener('click', function(event) {
    const button = event.target.closest('.toggle-password');
    if (!button) return;

    const name = button.getAttribute('data-target');
    const input = document.querySelector(`input[name="${name}"]`);
    if (!input) return;

    if (input.type === 'password') {
        input.type = 'text';
        button.textContent = '🙈';
        button.setAttribute('aria-label', 'Passwort verbergen');
    } else {
        input.type = 'password';
        button.textContent = '👁';
        button.setAttribute('aria-label', 'Passwort anzeigen');
    }
});
