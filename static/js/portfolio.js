document.querySelectorAll(".portfolio-nav-item").forEach((link) => {
    if (link.href.replaceAll("/", "") === window.location.href.replaceAll("/", "")) {
        link.classList.add("active");
        link.setAttribute("aria-current", "page");
    }
});

const modal = document.getElementById("myModal");

const btn = document.getElementById("openModal");

const span = document.getElementsByClassName("close")[0];

btn.onclick = function() {
    modal.style.display = "block";
}

span.onclick = function() {
    modal.style.display = "none";
}

window.onclick = function(event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}

document.addEventListener('DOMContentLoaded', function () {
    const symbolInput = document.getElementById('{{ form.prefix }}-symbol');
    const exchangeRateInput = document.getElementById('{{ form.prefix }}-exchange_rate');

    symbolInput.addEventListener('blur', function () {
        const symbol = this.value.trim(); 
        if (symbol) {
            fetchExchangeRate(symbol);
        }
    });

    function fetchExchangeRate(symbol) {
        fetch(`/api/exchange-rate?symbol=${symbol}`)
            .then(response => response.json())
            .then(data => {
                if (data.exchangeRate) {
                    exchangeRateInput.value = parseFloat(data.exchangeRate).toFixed(14);
                } else {
                    console.error('Exchange rate not found');
                }
            })
            .catch(error => {
                console.error('Error fetching exchange rate:', error);
            });
    }
});
