document.querySelector('.button-loading-screen').addEventListener('click', async function(e) {
    e.preventDefault();

    const csrftoken = getCookie('csrftoken');
    const form = e.target.form; 
    const formData = new FormData(form);

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest', 
                'X-CSRFToken': csrftoken, 
            },
        });

        const data = await response.json();

        if (data.success) {
            console.log("Success");
            startAnimation();
        } else {
            displayServerErrors(data.errors);
        }
    } catch (error) {
        console.error('Fetch error:', error);
    }
});

function startAnimation() {
    document.getElementById('overlay').style.display = 'flex';
    document.querySelectorAll('.site-content, header, footer').forEach(function(element) {
        element.classList.add('blurred');
    });

    let progress = 0;
    const interval = 30;
    const totalTime = 1500; 
    const increment = 100 * interval / totalTime; 

    const intervalId = setInterval(function() {
        progress += increment;
        if (progress >= 100) {
            progress = 100;
            clearInterval(intervalId);

            let redirectUrl = '/home/'; 
            const params = new URLSearchParams(window.location.search);
            const next = params.get('next');
            if (next) {
                redirectUrl = next;
            }
            window.location.href = redirectUrl;
        }
        const progressBar = document.getElementById('progressBar');
        const progressPercentage = document.getElementById('progressPercentage');
        progressBar.style.width = progress + '%';
        progressPercentage.textContent = Math.round(progress) + '%';
    }, interval);
}

function displayServerErrors(errors) {
    console.log("To do: handle this: ", errors)
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}