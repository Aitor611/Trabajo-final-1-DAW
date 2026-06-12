document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const clearBtn = document.getElementById('clearBtn');
    const searchInfo = document.getElementById('searchInfo');
    const productGrid = document.getElementById('productGrid');
    const prevBtn = document.getElementById('prevPage');
    const nextBtn = document.getElementById('nextPage');
    const pageInfo = document.getElementById('pageInfo');
    
    let allCards = [];
    let filteredCards = [];
    let currentPage = 1;
    let itemsPerPage = 9;
    let totalPages = 1;

    function initCards() {
        allCards = Array.from(document.querySelectorAll('.product-card'));
        filteredCards = [...allCards];
        totalPages = Math.ceil(filteredCards.length / itemsPerPage);
        currentPage = 1;
        updatePaginationButtons();
        showPage(currentPage);
        updateSearchInfo();
    }

    function showPage(page) {
        allCards.forEach(card => card.style.display = 'none');
        if (filteredCards.length === 0) return;
        const start = (page - 1) * itemsPerPage;
        const end = start + itemsPerPage;
        const cardsToShow = filteredCards.slice(start, end);
        cardsToShow.forEach(card => card.style.display = '');
        pageInfo.textContent = `Page ${page} of ${totalPages}`;
    }

    function updatePaginationButtons() {
        if (prevBtn) prevBtn.disabled = (currentPage === 1);
        if (nextBtn) nextBtn.disabled = (currentPage === totalPages || totalPages === 0);
    }

    function updateSearchInfo() {
        if (searchInfo) {
            const query = searchInput.value.trim().toLowerCase();
            if (query === '') {
                searchInfo.textContent = `${filteredCards.length} games available`;
            } else {
                searchInfo.textContent = `${filteredCards.length} result(s) for "${query}"`;
            }
        }
        let noResultsDiv = document.getElementById('noResultsMsg');
        if (filteredCards.length === 0 && searchInput.value.trim() !== '') {
            if (!noResultsDiv) {
                noResultsDiv = document.createElement('div');
                noResultsDiv.id = 'noResultsMsg';
                noResultsDiv.className = 'no-results';
                noResultsDiv.textContent = 'No games found.';
                productGrid.appendChild(noResultsDiv);
            }
        } else {
            if (noResultsDiv) noResultsDiv.remove();
        }
    }

    function applyFilter() {
        const query = searchInput.value.trim().toLowerCase();
        if (query === '') {
            filteredCards = [...allCards];
        } else {
            filteredCards = allCards.filter(card => {
                const name = card.getAttribute('data-name');
                return name && name.includes(query);
            });
        }
        totalPages = Math.ceil(filteredCards.length / itemsPerPage);
        currentPage = 1;
        updatePaginationButtons();
        showPage(currentPage);
        updateSearchInfo();
    }

    if (searchInput) searchInput.addEventListener('input', applyFilter);
    if (clearBtn) {
        clearBtn.addEventListener('click', function() {
            searchInput.value = '';
            applyFilter();
            searchInput.focus();
        });
    }
    if (nextBtn) {
        nextBtn.addEventListener('click', function() {
            if (currentPage < totalPages) {
                currentPage++;
                showPage(currentPage);
                updatePaginationButtons();
            }
        });
    }
    if (prevBtn) {
        prevBtn.addEventListener('click', function() {
            if (currentPage > 1) {
                currentPage--;
                showPage(currentPage);
                updatePaginationButtons();
            }
        });
    }
    initCards();
});