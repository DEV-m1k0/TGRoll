// document.addEventListener('DOMContentLoaded', function() {
//     // Имитация загрузки данных пользователя
//     setTimeout(function() {
//         document.querySelector('.ton-value').textContent = '42.50 TON';
//         document.querySelector('.text-muted').textContent = '~ $102.00';
//     }, 1000);

//     // Обработка кликов по контейнерам
//     const containerButtons = document.querySelectorAll('.container-card .btn');
//     containerButtons.forEach(button => {
//         button.addEventListener('click', function(e) {
//             e.stopPropagation();
//             const container = this.closest('.container-card');
//             const title = container.querySelector('.container-title').textContent;
//             const price = container.querySelector('.container-price').textContent;
            
//             alert(`Открытие контейнера: ${title} за ${price}`);
//             // Здесь будет логика открытия контейнера
//         });
//     });

//     // Обработка кликов по карточкам контейнеров
//     const containerCards = document.querySelectorAll('.container-card');
//     containerCards.forEach(card => {
//         card.addEventListener('click', function() {
//             const title = this.querySelector('.container-title').textContent;
//             // Здесь будет логика просмотра информации о контейнере
//             console.log(`Просмотр контейнера: ${title}`);
//         });
//     });
// });