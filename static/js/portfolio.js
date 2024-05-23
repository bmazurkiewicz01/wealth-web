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
    const searchDiv = document.querySelector('.search-bar-container');
    searchDiv.style.display = 'block';

    const addInvestmentForm = document.getElementById('add-investment-form');
    const symbolInput = document.getElementById('{{ form.prefix }}-symbol');
    const exchangeRateInput = document.getElementById('{{ form.prefix }}-exchange_rate');
    const dateInput = document.getElementById('id_trade_date'); 
    const currencyInput = document.getElementById('id_currency');
    const loader = document.querySelector('.loader');
    loader.classList.add('loader-hidden');

    const submitBtn = document.querySelector('#submit-investment-btn');
    submitBtn.addEventListener('click', function() {
        if (addInvestmentForm.checkValidity()) {
            submitBtn.style.display = 'none';
            loader.classList.remove('loader-hidden');
        }
    });

    const refreshBtn = document.querySelector('#refresh');
    refreshBtn.addEventListener('click', async function() {
        await fetch('/portfolio/?refresh_prices=True');
        window.location.reload();
    });

    symbolInput.addEventListener('blur', function () {
        const symbol = this.value.trim(); 
        const currency = currencyInput.value.trim();
        if (symbol) {
            fetchExchangeRate(symbol, dateInput.value, currency);
        }
    });

    dateInput.addEventListener('input', function () {
        const symbol = symbolInput.value.trim();
        const date = this.value.trim();
        const currency = currencyInput.value.trim();
        if (symbol && date) {
            fetchExchangeRate(symbol, date, currency);
        }
    });

    function fetchExchangeRate(symbol, date, currency) {
        fetch(`/api/exchange-rate?symbol=${symbol}&date=${date}&currency=${currency}`)
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


document.addEventListener('DOMContentLoaded', function () {
    const symbolInput = document.getElementById('{{ form.prefix }}-symbol');
    const symbolsDatalist = document.getElementById('symbols');

    symbolInput.addEventListener('input', function () {
        const symbol = this.value.trim(); 
        if (symbol) {
            fetchSymbols(symbol);
        }
    });

    function fetchSymbols(symbol) {
        fetch(`/api/stock-symbols/?symbol=${symbol}`)
            .then(response => response.json())
            .then(data => {
                symbolsDatalist.innerHTML = ''; 
                data.symbols.forEach(symbol => {
                    const option = document.createElement('option');
                    option.value = symbol;
                    symbolsDatalist.appendChild(option);
                });
            })
            .catch(error => {
                console.error('Error fetching symbols:', error);
            });
    }
});

