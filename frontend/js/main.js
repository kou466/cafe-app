// API 기본 URL
const API_URL = 'http://localhost:8000/api/v1';

// 전역 변수
let categories = [];
let menus = [];
let currentCategory = null;

// 페이지 로드 시 실행
document.addEventListener('DOMContentLoaded', () => {
    loadCategories();
    loadMenus();
});

// 카테고리 로드
async function loadCategories() {
    try {
        const response = await fetch(`${API_URL}/categories`);
        categories = await response.json();
        renderCategoryTabs();
    } catch (error) {
        console.error('카테고리 로드 실패:', error);
    }
}

// 메뉴 로드
async function loadMenus(categoryId = null) {
    try {
        let url = `${API_URL}/menus`;
        if (categoryId) {
            url += `?category_id=${categoryId}`;
        }
        
        const response = await fetch(url);
        menus = await response.json();
        renderMenuGrid();
    } catch (error) {
        console.error('메뉴 로드 실패:', error);
    }
}

// 카테고리 탭 렌더링
function renderCategoryTabs() {
    const categoryTabsEl = document.getElementById('categoryTabs');
    
    // 전체 보기 탭 추가
    let tabsHTML = `
        <button class="category-tab ${!currentCategory ? 'active' : ''}" 
                onclick="filterByCategory(null)">
            전체
        </button>
    `;
    
    // 카테고리별 탭 추가
    categories.forEach(category => {
        tabsHTML += `
            <button class="category-tab ${currentCategory === category.id ? 'active' : ''}" 
                    onclick="filterByCategory(${category.id})">
                ${category.name}
            </button>
        `;
    });
    
    categoryTabsEl.innerHTML = tabsHTML;
}

// 카테고리별 필터링
function filterByCategory(categoryId) {
    currentCategory = categoryId;
    loadMenus(categoryId);
    renderCategoryTabs();
}

// 메뉴 그리드 렌더링
function renderMenuGrid() {
    const menuGridEl = document.getElementById('menuGrid');
    
    if (menus.length === 0) {
        menuGridEl.innerHTML = '<p>메뉴가 없습니다.</p>';
        return;
    }
    
    let menuHTML = '';
    menus.forEach(menu => {
        // 가격 포맷팅 (천단위 콤마)
        const formattedPrice = menu.price.toLocaleString('ko-KR');
        
        menuHTML += `
            <div class="menu-item">
                <img src="${menu.image_url || '/images/default-menu.jpg'}" 
                     alt="${menu.name}"
                     onerror="this.src='/images/default-menu.jpg'">
                <div class="menu-item-content">
                    <h3>${menu.name}</h3>
                    <p class="description">${menu.description || ''}</p>
                    <p class="price">₩${formattedPrice}</p>
                    ${!menu.is_available ? '<p class="sold-out">품절</p>' : ''}
                </div>
            </div>
        `;
    });
    
    menuGridEl.innerHTML = menuHTML;
}

// 메뉴 섹션으로 스크롤
function scrollToMenu() {
    document.getElementById('menu').scrollIntoView({ behavior: 'smooth' });
}

// 부드러운 스크롤 네비게이션
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        
        if (targetSection) {
            const navbarHeight = document.querySelector('.navbar').offsetHeight;
            const targetPosition = targetSection.offsetTop - navbarHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
}); 