document.addEventListener('DOMContentLoaded', function() {
    // Переменные для хранения текущего состояния
    let currentUserBalance = 0;
    let currentContainerId = null;
    let tonPriceUSD = 2.5;
    // Функция для загрузки баланса пользователя
    function loadUserBalance() {
        fetch('/api/user_balance')
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error('Error loading balance:', data.error);
                    return;
                }
                
                currentUserBalance = data.balance;
                updateBalanceDisplay();
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }


    function loadTonPrice() {
    fetch('/api/ton_price')
        .then(response => response.json())
        .then(data => {
            tonPriceUSD = data.ton_price_usd;
            updateBalanceDisplay();
        })
        .catch(error => {
            console.error('Error loading TON price:', error);
        });
}
    function updateBalanceDisplay() {
    const balanceElement = document.querySelector('.ton-value');
    const usdValueElement = document.querySelector('.usd-value');
    
    if (balanceElement) {
        balanceElement.textContent = currentUserBalance.toFixed(2) + ' TON';
    }
    
    if (usdValueElement) {
        const usdValue = currentUserBalance * tonPriceUSD;
        usdValueElement.textContent = '~ $' + usdValue.toFixed(2);
    }
}
    document.querySelectorAll('.btn-open-chest').forEach(btn => {
    btn.addEventListener('click', function(e) {
        e.stopPropagation();
        
        const containerId = this.getAttribute('data-container-id');
        if (!containerId) return;
        
        // Запрос к API для открытия контейнера
        fetch('/api/open_container', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                container_id: parseInt(containerId)
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert(data.error);
                return;
            }
            
            // Обновляем баланс
            currentUserBalance = data.new_balance;
            updateBalanceDisplay();
            
            // Заполняем и показываем модальное окно с результатом
            document.getElementById('rewardAmount').textContent = data.reward.toFixed(2) + ' TON';
            document.getElementById('rewardProbability').textContent = (data.probability * 100).toFixed(2) + '%';
            document.getElementById('newBalance').textContent = data.new_balance.toFixed(2) + ' TON';
            
            const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
            resultModal.show();
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Ошибка при открытии сундука');
        });
    });
});

// Добавим отдельный обработчик для просмотра содержимого кейса
document.querySelectorAll('.container-card').forEach(card => {
    card.addEventListener('click', function(e) {
        // Проверяем, не было ли клика по кнопке открытия
        if (e.target.closest('.btn-open-chest')) {
            return;
        }
        
        const containerId = this.getAttribute('data-container-id');
        
        // Запрос к API для получения информации о контейнере
        fetch(`/api/container/${containerId}`)
            .then(response => response.json())
            .then(data => {
                // Заполняем таблицу лута
                const tableBody = document.getElementById('lootTableBody');
                tableBody.innerHTML = '';
                
                data.cells.forEach(cell => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${cell.reward_amount.toFixed(2)}</td>
                        <td>${(cell.probability * 100).toFixed(2)}%</td>
                    `;
                    tableBody.appendChild(row);
                });
                
                // Показываем модальное окно
                const lootModal = new bootstrap.Modal(document.getElementById('lootModal'));
                lootModal.show();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ошибка при загрузке информации о сундуке');
            });
    });
});

    // Обработчик клика по кнопке "Открыть"
    document.querySelectorAll('.btn-open-chest').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.stopPropagation(); // Предотвращаем всплытие события к карточке
            const containerId = this.getAttribute('data-container-id');
            if (!containerId) return;
            const containerCard = this.closest('.container-card');
            if (containerCard.classList.contains('container-inactive')) {
            alert('Этот сундук временно недоступен');
            return;
        }
            if (!currentContainerId) return;
            
            // Запрос к API для открытия контейнера
            fetch('/api/open_container', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    container_id: parseInt(currentContainerId)
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    alert(data.error);
                    return;
                }
                
                // Обновляем баланс
                currentUserBalance = data.new_balance;
                updateBalanceDisplay();
                
                // Заполняем и показываем модальное окно с результатом
                document.getElementById('rewardAmount').textContent = data.reward.toFixed(2) + ' TON';
                document.getElementById('rewardProbability').textContent = (data.probability * 100).toFixed(2) + '%';
                document.getElementById('newBalance').textContent = data.new_balance.toFixed(2) + ' TON';
                
                const resultModal = new bootstrap.Modal(document.getElementById('resultModal'));
                resultModal.show();
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Ошибка при открытии сундука');
            });
        });
    });

    // Инициализация
    loadUserBalance();
    loadTonPrice();
    // Добавляем data-атрибуты к карточкам контейнеров
    document.querySelectorAll('.container-card').forEach((card, index) => {
        card.setAttribute('data-container-id', index + 1);
    });
});
