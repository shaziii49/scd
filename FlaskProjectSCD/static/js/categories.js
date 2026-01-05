// Categories Page JavaScript

let currentPage = 1;
const perPage = 20;

// Load categories
async function loadCategories(page = 1) {
    try {
        showLoading('categoriesTableBody');
        
        const data = await apiRequest(`/categories?page=${page}&per_page=${perPage}`);
        
        if (data.success) {
            displayCategories(data.data);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        document.getElementById('categoriesTableBody').innerHTML = `
            <tr><td colspan="5" class="text-center text-danger">
                Error loading categories: ${error.message}
            </td></tr>
        `;
    }
}

// Display categories in table
function displayCategories(categories) {
    const tbody = document.getElementById('categoriesTableBody');
    
    if (categories.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="text-center text-muted">No categories found</td></tr>';
        return;
    }
    
    tbody.innerHTML = categories.map(category => `
        <tr>
            <td><strong>${category.category_name}</strong></td>
            <td>${category.description || 'N/A'}</td>
            <td>${category.parent_category ? category.parent_category.category_name : 'Root Category'}</td>
            <td><span class="badge bg-info">${category.subcategories ? category.subcategories.length : 0}</span></td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editCategory(${category.category_id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteCategory(${category.category_id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Add category form submission
document.getElementById('addCategoryForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        const formData = getFormData('addCategoryForm');
        
        const response = await apiRequest('/categories', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        if (response.success) {
            showAlert('Category added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addCategoryModal')).hide();
            resetForm('addCategoryForm');
            loadCategories(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error adding category: ' + error.message, 'danger');
    }
});

// Delete category
async function deleteCategory(categoryId) {
    const confirmed = await confirmAction('Are you sure you want to delete this category?');
    
    if (!confirmed) return;
    
    try {
        const response = await apiRequest(`/categories/${categoryId}`, {
            method: 'DELETE'
        });
        
        if (response.success) {
            showAlert('Category deleted successfully!', 'success');
            loadCategories(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting category: ' + error.message, 'danger');
    }
}

// Edit category
async function editCategory(categoryId) {
    try {
        const response = await apiRequest(`/categories/${categoryId}`);
        
        if (response.success) {
            const category = response.data;
            
            // Populate edit form
            document.getElementById('editCategoryId').value = category.category_id;
            document.getElementById('editCategoryName').value = category.category_name;
            document.getElementById('editCategoryDescription').value = category.description || '';
            
            // Load parent categories for dropdown
            await loadParentCategories(category.parent_category_id);
            
            // Show modal
            new bootstrap.Modal(document.getElementById('editCategoryModal')).show();
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error loading category: ' + error.message, 'danger');
    }
}

// Load parent categories for dropdown
async function loadParentCategories(selectedParentId = null) {
    try {
        const response = await apiRequest('/categories?per_page=1000');
        
        if (response.success) {
            const select = document.getElementById('editParentCategory');
            if (select) {
                // Clear existing options
                select.innerHTML = '';
                
                // Add default option
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'None (Root Category)';
                select.appendChild(defaultOption);
                
                if (Array.isArray(response.data)) {
                    response.data.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category.category_id;
                        option.textContent = category.category_name;
                        if (category.category_id == selectedParentId) {
                            option.selected = true;
                        }
                        select.appendChild(option);
                    });
                }
            }
        }
    } catch (error) {
        console.error('Error loading parent categories:', error);
    }
}

// Edit category form submission
document.getElementById('editCategoryForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        const categoryId = document.getElementById('editCategoryId').value;
        const formData = getFormData('editCategoryForm');
        
        const response = await apiRequest(`/categories/${categoryId}`, {
            method: 'PUT',
            body: JSON.stringify(formData)
        });
        
        if (response.success) {
            showAlert('Category updated successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('editCategoryModal')).hide();
            loadCategories(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error updating category: ' + error.message, 'danger');
    }
});

// Load initial data
document.addEventListener('DOMContentLoaded', () => {

    loadCategories(1);
    // Delay loading parent categories to ensure DOM is ready
    setTimeout(() => {
        loadParentCategoriesForAdd();
        loadParentCategoriesForEdit(); // Also load for edit modal
    }, 100);
});

// Load parent categories for edit form on page load
async function loadParentCategoriesForEdit() {
    try {
        const response = await apiRequest('/categories?per_page=1000');
        
        if (response.success) {
            const select = document.getElementById('editParentCategory');
            if (select) {
                // Clear existing options
                select.innerHTML = '';
                
                // Add default option
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'None (Root Category)';
                select.appendChild(defaultOption);
                
                if (Array.isArray(response.data)) {
                    response.data.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category.category_id;
                        option.textContent = category.category_name;
                        select.appendChild(option);
                    });
                }
            }
        }
    } catch (error) {
        console.error('Error loading parent categories for edit form:', error);
    }
}

// Load parent categories when add modal is shown
document.getElementById('addCategoryModal')?.addEventListener('show.bs.modal', () => {
    loadParentCategoriesForAdd();
});

// Load parent categories for add form
async function loadParentCategoriesForAdd() {
    try {
        const response = await apiRequest('/categories?per_page=1000');
        
        if (response.success) {
            const select = document.getElementById('addParentCategory');
            if (select) {
                // Clear existing options
                select.innerHTML = '';
                
                // Add default option
                const defaultOption = document.createElement('option');
                defaultOption.value = '';
                defaultOption.textContent = 'None (Root Category)';
                select.appendChild(defaultOption);
                
                if (Array.isArray(response.data)) {
                    response.data.forEach(category => {
                        const option = document.createElement('option');
                        option.value = category.category_id;
                        option.textContent = category.category_name;
                        select.appendChild(option);
                    });
                }
            }
        }
    } catch (error) {
        console.error('Error loading parent categories for add form:', error);
    }
}