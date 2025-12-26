document.addEventListener('DOMContentLoaded', function () {
    // Элементы страницы
    const spendsTableBody = document.getElementById('spendsTableBody');
    // const totalAmountElement = document.getElementById('totalAmount');
    const addSpendBtn = document.getElementById('addSpendBtn');
    const spendModal = document.getElementById('spendModal');
    const descriptionModal = document.getElementById('descriptionModal');
    const modalClose = document.getElementById('modalClose');
    const descriptionModalClose = document.getElementById('descriptionModalClose');
    const closeDescBtn = document.getElementById('closeDescBtn');
    const cancelBtn = document.getElementById('cancelBtn');
    const spendForm = document.getElementById('spendForm');
    const categoryFilter = document.getElementById('categoryFilter');
    const sortSelect = document.getElementById('sortSelect');
    const searchInput = document.getElementById('searchInput');
    const statsContainer = document.getElementById('statsContainer');
    const charCounter = document.getElementById('charCount');
    const descriptionTextarea = document.getElementById('description');

    // Счетчик символов для описания
    if (descriptionTextarea) {
        descriptionTextarea.addEventListener('input', function () {
            charCounter.textContent = this.value.length;
        });
    }

    // Обновление общей суммы
    function updateTotalAmount() {
        const amounts = document.querySelectorAll('.amount-cell, .card-amount');
        let total = 0;

        amounts.forEach(element => {
            const amountText = element.textContent.replace(' ₽', '').trim();
            total += parseFloat(amountText) || 0;
        });

        // totalAmountElement.textContent = total.toFixed(2);
    }

    // Генерация статистики
    function generateStats() {
        const categoryTotals = {};
        const tableRows = document.querySelectorAll('#spendsTableBody tr[data-id]');
        const cardItems = document.querySelectorAll('.expense-card[data-id]');

        // Обрабатываем строки таблицы
        tableRows.forEach(row => {
            const category = row.getAttribute('data-category');
            const amountText = row.querySelector('.amount-cell').textContent.replace(' ₽', '').trim();
            const amount = parseFloat(amountText) || 0;

            if (!categoryTotals[category]) {
                categoryTotals[category] = 0;
            }
            categoryTotals[category] += amount;
        });

        // Обрабатываем карточки
        cardItems.forEach(card => {
            const category = card.getAttribute('data-category');
            const amountText = card.querySelector('.card-amount').textContent.replace(' ₽', '').trim();
            const amount = parseFloat(amountText) || 0;

            if (!categoryTotals[category]) {
                categoryTotals[category] = 0;
            }
            categoryTotals[category] += amount;
        });

        // Очистка контейнера
        statsContainer.innerHTML = '';

        // Добавление карточек статистики
        Object.entries(categoryTotals).forEach(([category, total]) => {
            const statCard = document.createElement('div');
            statCard.className = 'stat-card';

            // Цвет в зависимости от категории
            const colors = {
                'Продукты': '#ffebee',
                'Транспорт': '#e3f2fd',
                'Развлечения': '#f3e5f5',
                'Коммуналка': '#e8f5e9',
                'Другое': '#fff3e0'
            };

            statCard.style.borderTopColor = colors[category] || '#f0f0f0';

            statCard.innerHTML = `
                <h4>${category}</h4>
                <div class="stat-value">${total.toFixed(2)} ₽</div>
            `;

            statsContainer.appendChild(statCard);
        });
    }

    // Фильтрация таблицы
    function filterTable() {
        const selectedCategory = categoryFilter.value;
        const searchQuery = searchInput.value.toLowerCase();

        // Фильтрация таблицы
        const tableRows = document.querySelectorAll('#spendsTableBody tr[data-id]');
        let visibleTableCount = 0;

        tableRows.forEach(row => {
            const category = row.getAttribute('data-category');
            const categoryCell = row.querySelector('.category-cell').textContent.toLowerCase();
            const amountCell = row.querySelector('.amount-cell').textContent.toLowerCase();
            const dateCell = row.querySelector('.date-cell').textContent.toLowerCase();
            const description = row.getAttribute('data-description').toLowerCase();

            const matchesCategory = selectedCategory === 'all' || category === selectedCategory;
            const matchesSearch = searchQuery === '' ||
                categoryCell.includes(searchQuery) ||
                amountCell.includes(searchQuery) ||
                dateCell.includes(searchQuery) ||
                description.includes(searchQuery);

            if (matchesCategory && matchesSearch) {
                row.style.display = '';
                visibleTableCount++;
            } else {
                row.style.display = 'none';
            }
        });

        // Фильтрация карточек
        const cards = document.querySelectorAll('.expense-card');
        let visibleCardCount = 0;

        cards.forEach(card => {
            const category = card.getAttribute('data-category');
            const categoryText = card.querySelector('.category-badge').textContent.toLowerCase();
            const amountText = card.querySelector('.card-amount').textContent.toLowerCase();
            const dateText = card.querySelector('.card-date').textContent.toLowerCase();
            const description = card.querySelector('.card-description').textContent.toLowerCase();

            const matchesCategory = selectedCategory === 'all' || category === selectedCategory;
            const matchesSearch = searchQuery === '' ||
                categoryText.includes(searchQuery) ||
                amountText.includes(searchQuery) ||
                dateText.includes(searchQuery) ||
                description.includes(searchQuery);

            if (matchesCategory && matchesSearch) {
                card.style.display = '';
                visibleCardCount++;
            } else {
                card.style.display = 'none';
            }
        });

        // Показать/скрыть сообщение о пустой таблице
        const emptyRow = document.querySelector('.empty-row');
        if (emptyRow && visibleTableCount === 0 && visibleCardCount === 0) {
            emptyRow.style.display = '';
        } else if (emptyRow) {
            emptyRow.style.display = 'none';
        }
    }

    // Сортировка таблицы
    function sortTable(sortType) {
        const tbody = document.getElementById('spendsTableBody');
        const cardsContainer = document.getElementById('cardsContainer');
        const tableRows = Array.from(tbody.querySelectorAll('tr[data-id]'));
        const cards = Array.from(cardsContainer.querySelectorAll('.expense-card'));

        // Сортировка строк таблицы
        tableRows.sort((a, b) => {
            switch (sortType) {
                case 'newest':
                    const dateA = new Date(a.querySelector('.date-cell').textContent);
                    const dateB = new Date(b.querySelector('.date-cell').textContent);
                    return dateB - dateA;

                case 'oldest':
                    const dateA2 = new Date(a.querySelector('.date-cell').textContent);
                    const dateB2 = new Date(b.querySelector('.date-cell').textContent);
                    return dateA2 - dateB2;

                case 'amount_high':
                    const amountA = parseFloat(a.querySelector('.amount-cell').textContent.replace(' ₽', ''));
                    const amountB = parseFloat(b.querySelector('.amount-cell').textContent.replace(' ₽', ''));
                    return amountB - amountA;

                case 'amount_low':
                    const amountA2 = parseFloat(a.querySelector('.amount-cell').textContent.replace(' ₽', ''));
                    const amountB2 = parseFloat(b.querySelector('.amount-cell').textContent.replace(' ₽', ''));
                    return amountA2 - amountB2;

                default:
                    return 0;
            }
        });

        // Сортировка карточек
        cards.sort((a, b) => {
            switch (sortType) {
                case 'newest':
                    const dateA = new Date(a.querySelector('.card-date').textContent);
                    const dateB = new Date(b.querySelector('.card-date').textContent);
                    return dateB - dateA;

                case 'oldest':
                    const dateA2 = new Date(a.querySelector('.card-date').textContent);
                    const dateB2 = new Date(b.querySelector('.card-date').textContent);
                    return dateA2 - dateB2;

                case 'amount_high':
                    const amountA = parseFloat(a.querySelector('.card-amount').textContent.replace(' ₽', ''));
                    const amountB = parseFloat(b.querySelector('.card-amount').textContent.replace(' ₽', ''));
                    return amountB - amountA;

                case 'amount_low':
                    const amountA2 = parseFloat(a.querySelector('.card-amount').textContent.replace(' ₽', ''));
                    const amountB2 = parseFloat(b.querySelector('.card-amount').textContent.replace(' ₽', ''));
                    return amountA2 - amountB2;

                default:
                    return 0;
            }
        });

        // Удаляем старые строки таблицы
        tableRows.forEach(row => tbody.removeChild(row));
        // Добавляем отсортированные строки таблицы
        tableRows.forEach(row => tbody.appendChild(row));

        // Удаляем старые карточки
        cards.forEach(card => cardsContainer.removeChild(card));
        // Добавляем отсортированные карточки
        cards.forEach(card => cardsContainer.appendChild(card));
    }

    // Открытие модального окна с полным описанием
    function showFullDescription(element) {
        const row = element.closest('tr, .expense-card');
        const category = row.querySelector('.category-badge').textContent;
        const date = row.querySelector('.date-cell, .card-date').textContent;
        const amount = row.querySelector('.amount-cell, .card-amount').textContent;
        const description = row.getAttribute('data-description');

        document.getElementById('descCategory').textContent = category;
        document.getElementById('descDate').textContent = date;
        document.getElementById('descAmount').textContent = amount;
        document.getElementById('descContent').textContent = description || 'Описание отсутствует';

        descriptionModal.style.display = 'flex';
    }

    // Управление модальными окнами
    // addSpendBtn.addEventListener('click', () => {
    //     document.getElementById('modalTitle').textContent = 'Добавить расход';
    //     spendForm.reset();
    //     document.getElementById('spendId').value = '';
    //     charCounter.textContent = '0';
    //     spendModal.style.display = 'flex';
    // });

    modalClose.addEventListener('click', () => {
        spendModal.style.display = 'none';
    });

    descriptionModalClose.addEventListener('click', () => {
        descriptionModal.style.display = 'none';
    });

    closeDescBtn.addEventListener('click', () => {
        descriptionModal.style.display = 'none';
    });

    cancelBtn.addEventListener('click', () => {
        spendModal.style.display = 'none';
    });

    // Закрытие модальных окон при клике вне их
    window.addEventListener('click', (event) => {
        if (event.target === spendModal) {
            spendModal.style.display = 'none';
        }
        if (event.target === descriptionModal) {
            descriptionModal.style.display = 'none';
        }
    });

    // Обработка формы
    spendForm.addEventListener('submit', function (e) {
        e.preventDefault();

        const id = document.getElementById('spendId').value;
        const category = document.getElementById('category').value;
        const amount = document.getElementById('amount').value;
        const description = document.getElementById('description').value;

        // В реальном приложении здесь будет AJAX-запрос к серверу
        console.log('Сохранение данных:', {
            id,
            category,
            amount,
            description
        });

        // Имитация успешного сохранения
        alert(`Расход сохранен!\nКатегория: ${category}\nСумма: ${amount} ₽\nОписание: ${description || 'не указано'}`);

        spendModal.style.display = 'none';
        // В реальном приложении здесь будет обновление таблицы
    });

    // Обработчики кликов по описанию
    document.addEventListener('click', function (e) {
        // Клик по описанию для показа полного текста
        if (e.target.closest('.description-preview')) {
            e.preventDefault();
            e.stopPropagation();
            showFullDescription(e.target);
        }

        // Клик по кнопке "читать далее"
        if (e.target.closest('.read-more')) {
            e.preventDefault();
            e.stopPropagation();
            showFullDescription(e.target);
        }

        // Редактирование записи
        if (e.target.closest('.btn-edit')) {
            const row = e.target.closest('tr, .expense-card');
            const id = row.getAttribute('data-id');
            const category = row.getAttribute('data-category');
            const amountElement = row.querySelector('.amount-cell, .card-amount');
            const amount = amountElement.textContent.replace(' ₽', '').trim();
            const description = row.getAttribute('data-description');

            document.getElementById('modalTitle').textContent = 'Редактировать расход';
            document.getElementById('spendId').value = id;
            document.getElementById('category').value = category;
            document.getElementById('amount').value = amount;
            document.getElementById('description').value = description || '';
            charCounter.textContent = (description || '').length;

            spendModal.style.display = 'flex';
        }

        // Удаление записи
        if (e.target.closest('.btn-delete')) {
            if (confirm('Вы уверены, что хотите удалить эту запись?')) {
                const row = e.target.closest('tr, .expense-card');
                const id = row.getAttribute('data-id');

                // В реальном приложении здесь будет AJAX-запрос на удаление
                console.log('Удаление записи с ID:', id);

                row.remove();
                updateTotalAmount();
                generateStats();
                filterTable();
            }
        }
    });

    // Обработчики фильтров
    categoryFilter.addEventListener('change', filterTable);
    sortSelect.addEventListener('change', function () {
        sortTable(this.value);
    });
    searchInput.addEventListener('input', filterTable);

    // Инициализация
    updateTotalAmount();
    generateStats();

    // Адаптивное переключение между таблицей и карточками
    function checkViewMode() {
        const tableContainer = document.querySelector('.table-container');
        const cardsContainer = document.getElementById('cardsContainer');

        if (window.innerWidth <= 768) {
            tableContainer.style.display = 'none';
            cardsContainer.style.display = 'grid';
        } else {
            tableContainer.style.display = 'block';
            cardsContainer.style.display = 'none';
        }
    }

    window.addEventListener('resize', checkViewMode);
    checkViewMode(); // Инициализация при загрузке

    // Пример добавления тестовых данных (для демонстрации)
    if (spendsTableBody.querySelectorAll('tr[data-id]').length === 0) {
        const testData = [{
                id: 1,
                category: 'Продукты',
                amount: 1250.50,
                created_at: '2024-01-15 14:30',
                description: 'Покупка продуктов на неделю: молоко, хлеб, сыр, овощи, фрукты, мясо, крупы и сладости к чаю.'
            },
            {
                id: 2,
                category: 'Транспорт',
                amount: 450,
                created_at: '2024-01-14 09:15',
                description: 'Оплата проезда в общественном транспорте на месяц, включая метро и автобусы.'
            },
            {
                id: 3,
                category: 'Развлечения',
                amount: 3200,
                created_at: '2024-01-13 20:45',
                description: 'Посещение кинотеатра с друзьями, ужин в ресторане и различные активности на выходных.'
            },
            {
                id: 4,
                category: 'Коммуналка',
                amount: 5400.75,
                created_at: '2024-01-12 11:00',
                description: 'Оплата коммунальных услуг за январь: электричество, вода, газ, отопление и вывоз мусора.'
            },
            {
                id: 5,
                category: 'Продукты',
                amount: 890.20,
                created_at: '2024-01-11 18:30',
                description: 'Вечерняя покупка продуктов для ужина и завтрака: рыба, гарнир, салат и десерт.'
            }
        ];

        testData.forEach(spend => {
            // Добавление в таблицу
            const row = document.createElement('tr');
            row.setAttribute('data-id', spend.id);
            row.setAttribute('data-category', spend.category);
            row.setAttribute('data-description', spend.description || '');

            const truncatedDesc = spend.description ?
                (spend.description.length > 50 ?
                    spend.description.substring(0, 50) + '...' :
                    spend.description) :
                '';

            row.innerHTML = `
                <td class="id-cell">${spend.id}</td>
                <td class="category-cell">
                    <span class="category-badge category-${spend.category.toLowerCase()}">
                        ${spend.category}
                    </span>
                </td>
                <td class="amount-cell">${spend.amount} ₽</td>
                <td class="date-cell">${spend.created_at}</td>
                <td class="description-cell">
                    <div class="description-wrapper">
                        <div class="description-preview">
                            ${spend.description ? 
                                `${truncatedDesc}` + 
                                (spend.description.length > 50 ? 
                                    '<span class="read-more">... <i class="fas fa-chevron-down"></i></span>' : 
                                    '') : 
                                '<span class="no-description">—</span>'}
                        </div>
                        ${spend.description ? 
                            `<div class="description-full" title="${spend.description}">
                                ${spend.description}
                            </div>` : 
                            ''}
                    </div>
                </td>
                <td class="actions-cell">
                    <button class="btn-action btn-edit" title="Редактировать">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn-action btn-delete" title="Удалить">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            `;

            spendsTableBody.appendChild(row);

            // Добавление в карточки
            const cardsContainer = document.getElementById('cardsContainer');
            if (cardsContainer) {
                const card = document.createElement('div');
                card.className = 'expense-card';
                card.setAttribute('data-id', spend.id);
                card.setAttribute('data-category', spend.category);
                card.setAttribute('data-description', spend.description || '');

                const cardTruncatedDesc = spend.description ?
                    (spend.description.length > 100 ?
                        spend.description.substring(0, 100) + '...' :
                        spend.description) :
                    '';

                card.innerHTML = `
                    <div class="card-header">
                        <span class="category-badge category-${spend.category.toLowerCase()}">
                            ${spend.category}
                        </span>
                        <span class="card-date">${spend.created_at}</span>
                    </div>
                    <div class="card-body">
                        <div class="card-amount">${spend.amount} ₽</div>
                        <div class="card-description">
                            ${spend.description ? 
                                `<div class="description-preview">
                                    ${cardTruncatedDesc}
                                    ${spend.description.length > 100 ? 
                                        '<span class="read-more">... <i class="fas fa-chevron-down"></i></span>' : 
                                        ''}
                                </div>
                                <div class="description-full">
                                    ${spend.description}
                                </div>` : 
                                '<span class="no-description">Нет описания</span>'}
                        </div>
                    </div>
                    <div class="card-footer">
                        <button class="btn-action btn-edit" title="Редактировать">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="btn-action btn-delete" title="Удалить">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                `;

                cardsContainer.appendChild(card);
            }
        });

        updateTotalAmount();
        generateStats();
    }
});