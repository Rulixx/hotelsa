document.addEventListener('DOMContentLoaded', function() {

    // --- Логика для мобильного меню (улучшенная) ---
    const menuToggle = document.querySelector('.mobile-menu-toggle');
    const headerControls = document.querySelector('.header-controls');

    if (menuToggle && headerControls) {
        menuToggle.addEventListener('click', function() {
            // Переключаем класс, который отвечает за показ/скрытие и стили
            headerControls.classList.toggle('is-mobile-active');

            // Можно добавить класс на body для блокировки скролла фона, если нужно
            // document.body.classList.toggle('mobile-menu-open');
        });

        // Закрытие меню при клике вне его (опционально)
        document.addEventListener('click', function(event) {
            const isClickInsideMenu = headerControls.contains(event.target);
            const isClickOnToggler = menuToggle.contains(event.target);

            if (!isClickInsideMenu && !isClickOnToggler && headerControls.classList.contains('is-mobile-active')) {
                headerControls.classList.remove('is-mobile-active');
                // document.body.classList.remove('mobile-menu-open');
            }
        });
    }

    // --- Остальной ваш JS (если был) ---

    console.log("Premium Travel JS Initialized (v2)");
});