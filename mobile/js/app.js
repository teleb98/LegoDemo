document.addEventListener('DOMContentLoaded', () => {
    const API_BASE = '/api'; // Relative path, assuming served by same backend
    const productList = document.getElementById('product-list');
    const cameraInput = document.getElementById('camera-input');
    const scanBtn = document.getElementById('scan-btn');
    const loadingOverlay = document.getElementById('loading-overlay');

    // Load initial data
    fetchProducts();

    // Event Listeners
    scanBtn.addEventListener('click', () => {
        cameraInput.click();
    });

    cameraInput.addEventListener('change', async (e) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0];
            await uploadImage(file);
        }
    });

    async function fetchProducts() {
        try {
            const response = await fetch(`${API_BASE}/products`);
            if (!response.ok) throw new Error('Failed to fetch products');
            const products = await response.json();
            renderProducts(products);
        } catch (error) {
            console.error('Error fetching products:', error);
            // alert('Failed to load your collection.');
        }
    }

    function renderProducts(products) {
        productList.innerHTML = '';
        products.reverse().forEach(product => { // Show newest first
            const card = document.createElement('div');
            card.className = 'product-card';

            // Use server path for image, fallback to placeholder if needed
            const imgSrc = product.image ? product.image : 'https://via.placeholder.com/150?text=Lego';

            card.innerHTML = `
                <button class="delete-btn" onclick="deleteProduct(${product.id})">&times;</button>
                <img src="${imgSrc}" alt="${product.name}" class="product-image">
                <div class="product-info">
                    <div class="product-name">${product.name}</div>
                    <div class="product-set-num">Set #${product.setNumber || '???'}</div>
                </div>
            `;
            productList.appendChild(card);
        });
    }

    // Expose delete function globally
    window.deleteProduct = async (id) => {
        if (!confirm('Are you sure you want to remove this set?')) return;

        try {
            const response = await fetch(`${API_BASE}/products/${id}`, {
                method: 'DELETE'
            });

            if (response.ok) {
                fetchProducts();
            } else {
                alert('Failed to delete product');
            }
        } catch (error) {
            console.error('Error deleting product:', error);
        }
    };

    async function uploadImage(file) {
        showLoading(true);
        const formData = new FormData();
        formData.append('image', file);

        try {
            const response = await fetch(`${API_BASE}/scan`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) throw new Error('Upload failed');

            const newProduct = await response.json();

            // Refresh list to show new item
            await fetchProducts();

        } catch (error) {
            console.error('Error uploading image:', error);
            alert('Failed to identify Lego set. Please try again.');
        } finally {
            showLoading(false);
            // Reset input
            cameraInput.value = '';
        }
    }

    function showLoading(show) {
        if (show) {
            loadingOverlay.classList.remove('hidden');
        } else {
            loadingOverlay.classList.add('hidden');
        }
    }
});
