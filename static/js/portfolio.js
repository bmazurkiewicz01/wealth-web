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
    const dateInput = document.getElementById('id_trade_date'); 

    symbolInput.addEventListener('blur', function () {
        const symbol = this.value.trim(); 
        if (symbol) {
            fetchExchangeRate(symbol, dateInput.value);
        }
    });

    dateInput.addEventListener('input', function () {
        const symbol = symbolInput.value.trim();
        const date = this.value.trim();
        if (symbol && date) {
            fetchExchangeRate(symbol, date);
        }
    });

    function fetchExchangeRate(symbol, date) {
        fetch(`/api/exchange-rate?symbol=${symbol}&date=${date}`)
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

