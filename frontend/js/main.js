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
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        categories = await response.json();
        renderCategoryTabs();
        console.log('카테고리 로드 완료:', categories.length);
    } catch (error) {
        console.error('카테고리 로드 실패:', error);
        showErrorMessage('카테고리를 불러오는데 실패했습니다.');
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
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        menus = await response.json();
        renderMenuGrid();
        console.log('메뉴 로드 완료:', menus.length);
    } catch (error) {
        console.error('메뉴 로드 실패:', error);
        showErrorMessage('메뉴를 불러오는데 실패했습니다.');
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

// 이미지 에러 처리 함수
function handleImageError(img) {
    img.style.display = 'none'; // 이미지 숨기기
    img.parentElement.classList.add('no-image'); // CSS 클래스 추가
}

// 메뉴 그리드 렌더링
function renderMenuGrid() {
    const menuGridEl = document.getElementById('menuGrid');
    
    if (menus.length === 0) {
        menuGridEl.innerHTML = `
            <div class="no-menu-message">
                <p>🍽️ 현재 표시할 메뉴가 없습니다.</p>
            </div>
        `;
        return;
    }
    
    let menuHTML = '';
    menus.forEach(menu => {
        // 가격 포맷팅 (천단위 콤마)
        const formattedPrice = menu.price.toLocaleString('ko-KR');
        
        // 이미지가 있을 때만 img 태그 생성, 없으면 플레이스홀더
        const imageHTML = menu.image_url ? 
            `<img src="${menu.image_url}" 
                  alt="${menu.name}"
                  onerror="handleImageError(this)">` : 
            `<div class="menu-placeholder">🍽️</div>`;
        
        // 메뉴 상태에 따른 CSS 클래스
        const menuItemClass = menu.is_available ? 'menu-item' : 'menu-item unavailable';
        
        menuHTML += `
            <div class="${menuItemClass}">
                ${imageHTML}
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

// 에러 메시지 표시
function showErrorMessage(message) {
    const menuGridEl = document.getElementById('menuGrid');
    if (menuGridEl) {
        menuGridEl.innerHTML = `
            <div class="error-message">
                <p>⚠️ ${message}</p>
                <button onclick="location.reload()" class="retry-btn">다시 시도</button>
            </div>
        `;
    }
}

// 메뉴 섹션으로 스크롤
function scrollToMenu() {
    const menuSection = document.getElementById('menu');
    if (menuSection) {
        menuSection.scrollIntoView({ behavior: 'smooth' });
    }
}

// 로딩 상태 표시
function showLoading() {
    const menuGridEl = document.getElementById('menuGrid');
    if (menuGridEl) {
        menuGridEl.innerHTML = `
            <div class="loading-message">
                <p>🔄 메뉴를 불러오는 중...</p>
            </div>
        `;
    }
}

// 부드러운 스크롤 네비게이션
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href').substring(1);
        const targetSection = document.getElementById(targetId);
        
        if (targetSection) {
            const navbarHeight = document.querySelector('.navbar')?.offsetHeight || 0;
            const targetPosition = targetSection.offsetTop - navbarHeight;
            
            window.scrollTo({
                top: targetPosition,
                behavior: 'smooth'
            });
        }
    });
});

// 키보드 네비게이션 지원
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        // ESC 키로 현재 카테고리 필터 해제
        if (currentCategory) {
            filterByCategory(null);
        }
    }
}); 