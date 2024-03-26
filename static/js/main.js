const logoutButton = document.querySelector('.button-logout-loading-screen');
if (logoutButton != null)
{
    document.querySelector('.button-logout-loading-screen').addEventListener('click', function(e) {
        e.preventDefault();
    
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
                e.target.form.submit(); 
            }
            const progressBar = document.getElementById('progressBar');
            const progressPercentage = document.getElementById('progressPercentage');
            progressBar.style.width = progress + '%';
            progressPercentage.textContent = Math.round(progress) + '%';
        }, interval);
    
    });
}
