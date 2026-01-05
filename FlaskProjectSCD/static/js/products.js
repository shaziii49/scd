// Products Page JavaScript

let currentPage = 1;
const perPage = 10;
let searchTerm = '';

// Load categories for dropdown
async function loadCategoriesDropdown() {
    try {
        const data = await apiRequest('/categories?per_page=100');
        if (data.success) {
            // Populate category dropdowns in forms (name="category_id")
            const categorySelects = document.querySelectorAll('select[name="category_id"]');
            categorySelects.forEach(select => {
                select.innerHTML = '<option value="">Select Category</option>' +
                    data.data.map(cat => `<option value="${cat.category_id}">${cat.category_name}</option>`).join('');
            });
            
            // Populate category filter dropdown (id="categoryFilter")
            const categoryFilter = document.getElementById('categoryFilter');
            if (categoryFilter) {
                categoryFilter.innerHTML = '<option value="">All Categories</option>' +
                    data.data.map(cat => `<option value="${cat.category_id}">${cat.category_name}</option>`).join('');
            }
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

// Load suppliers for dropdown
async function loadSuppliersDropdown() {
    try {
        const data = await apiRequest('/suppliers?per_page=100');
        if (data.success) {
            const supplierSelects = document.querySelectorAll('select[name="supplier_id"]');
            supplierSelects.forEach(select => {
                select.innerHTML = '<option value="">Select Supplier</option>' +
                    data.data.map(sup => `<option value="${sup.supplier_id}">${sup.supplier_name}</option>`).join('');
            });
        }
    } catch (error) {
        console.error('Error loading suppliers:', error);
    }
}

// Load products
async function loadProducts(page = 1) {
    try {
        showLoading('productsTableBody');

        let url = `/products?page=${page}&per_page=${perPage}`;
        if (searchTerm) {
            url += `&search=${encodeURIComponent(searchTerm)}`;
        }
        
        // Add category filter
        const categoryFilter = document.getElementById('categoryFilter');
        if (categoryFilter && categoryFilter.value) {
            url += `&category_id=${categoryFilter.value}`;
        }
        
        // Add status filter
        const statusFilter = document.getElementById('statusFilter');
        if (statusFilter && statusFilter.value && statusFilter.value !== 'all') {
            url += `&status=${statusFilter.value}`;
        }

        const data = await apiRequest(url);

        if (data.success) {
            displayProducts(data.data);
            displayPagination(data.pagination);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        document.getElementById('productsTableBody').innerHTML = `
            <tr><td colspan="7" class="text-center text-danger">
                Error loading products: ${error.message}
            </td></tr>
        `;
    }
}

// Display products in table
function displayProducts(products) {
    const tbody = document.getElementById('productsTableBody');

    if (products.length === 0) {
        tbody.innerHTML = '<tr><td colspan="7" class="text-center text-muted">No products found</td></tr>';
        return;
    }

    tbody.innerHTML = products.map(product => `
        <tr>
            <td><strong>${product.product_name}</strong></td>
            <td><span class="badge bg-secondary">${product.sku}</span></td>
            <td>${product.category ? product.category.category_name : 'N/A'}</td>
            <td>${formatCurrency(product.price)}</td>
            <td>
                <span class="badge ${product.quantity_in_stock <= product.reorder_level ? 'bg-warning' : 'bg-success'}">
                    ${product.quantity_in_stock}
                </span>
            </td>
            <td>
                ${product.is_active 
                    ? '<span class="badge bg-success">Active</span>' 
                    : '<span class="badge bg-danger">Inactive</span>'}
            </td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editProduct(${product.product_id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-info" onclick="viewProduct(${product.product_id})">
                    <i class="fas fa-eye"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteProduct(${product.product_id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Display pagination
function displayPagination(pagination) {
    const paginationElement = document.getElementById('pagination');

    let html = '';

    // Previous button
    html += `
        <li class="page-item ${!pagination.has_prev ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="loadProducts(${pagination.page - 1}); return false;">
                Previous
            </a>
        </li>
    `;

    // Page numbers
    for (let i = 1; i <= pagination.total_pages; i++) {
        if (i === 1 || i === pagination.total_pages ||
            (i >= pagination.page - 2 && i <= pagination.page + 2)) {
            html += `
                <li class="page-item ${i === pagination.page ? 'active' : ''}">
                    <a class="page-link" href="#" onclick="loadProducts(${i}); return false;">
                        ${i}
                    </a>
                </li>
            `;
        } else if (i === pagination.page - 3 || i === pagination.page + 3) {
            html += '<li class="page-item disabled"><span class="page-link">...</span></li>';
        }
    }

    // Next button
    html += `
        <li class="page-item ${!pagination.has_next ? 'disabled' : ''}">
            <a class="page-link" href="#" onclick="loadProducts(${pagination.page + 1}); return false;">
                Next
            </a>
        </li>
    `;

    paginationElement.innerHTML = html;
    currentPage = pagination.page;
}

// Add product form submission
document.getElementById('addProductForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    try {
        const formData = getFormData('addProductForm');

        const response = await apiRequest('/products', {
            method: 'POST',
            body: JSON.stringify(formData)
        });

        if (response.success) {
            showAlert('Product added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addProductModal')).hide();
            resetForm('addProductForm');
            loadProducts(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error adding product: ' + error.message, 'danger');
    }
});

// Edit product
async function editProduct(productId) {
    try {
        const response = await apiRequest(`/products/${productId}`);

        if (response.success) {
            const product = response.data;

            // Fill edit form
            document.getElementById('editProductId').value = product.product_id;
            document.getElementById('edit_product_name').value = product.product_name;
            document.getElementById('edit_price').value = product.price;
            document.getElementById('edit_quantity_in_stock').value = product.quantity_in_stock;
            document.getElementById('edit_reorder_level').value = product.reorder_level;

            // Show modal
            const modal = new bootstrap.Modal(document.getElementById('editProductModal'));
            modal.show();
        }
    } catch (error) {
        showAlert('Error loading product: ' + error.message, 'danger');
    }
}

// Update product form submission
document.getElementById('editProductForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();

    try {
        const productId = document.getElementById('editProductId').value;
        const updateData = {
            product_name: document.getElementById('edit_product_name').value,
            price: parseFloat(document.getElementById('edit_price').value),
            quantity_in_stock: parseInt(document.getElementById('edit_quantity_in_stock').value),
            reorder_level: parseInt(document.getElementById('edit_reorder_level').value)
        };

        const response = await apiRequest(`/products/${productId}`, {
            method: 'PUT',
            body: JSON.stringify(updateData)
        });

        if (response.success) {
            showAlert('Product updated successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('editProductModal')).hide();
            loadProducts(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error updating product: ' + error.message, 'danger');
    }
});

// Delete product
async function deleteProduct(productId) {
    const confirmed = await confirmAction('Are you sure you want to delete this product?');

    if (!confirmed) return;

    try {
        const response = await apiRequest(`/products/${productId}`, {
            method: 'DELETE'
        });

        if (response.success) {
            showAlert('Product deleted successfully!', 'success');
            loadProducts(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting product: ' + error.message, 'danger');
    }
}

// View product details
function viewProduct(productId) {
    window.location.href = `/products/${productId}`;
}

// Search functionality
const searchInput = document.getElementById('searchInput');
if (searchInput) {
    searchInput.addEventListener('input', debounce((e) => {
        searchTerm = e.target.value;
        loadProducts(1);
    }, 500));
}

// Category filter functionality
const categoryFilter = document.getElementById('categoryFilter');
if (categoryFilter) {
    categoryFilter.addEventListener('change', () => {
        loadProducts(1);
    });
}

// Status filter functionality
const statusFilter = document.getElementById('statusFilter');
if (statusFilter) {
    statusFilter.addEventListener('change', () => {
        loadProducts(1);
    });
}

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    loadProducts(1);
    loadCategoriesDropdown();
    loadSuppliersDropdown();
});