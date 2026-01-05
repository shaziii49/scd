// Suppliers Page JavaScript

let currentPage = 1;
const perPage = 20;

// Load suppliers
async function loadSuppliers(page = 1) {
    try {
        showLoading('suppliersTableBody');
        
        const data = await apiRequest(`/suppliers?page=${page}&per_page=${perPage}`);
        
        if (data.success) {
            displaySuppliers(data.data);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        document.getElementById('suppliersTableBody').innerHTML = `
            <tr><td colspan="6" class="text-center text-danger">
                Error loading suppliers: ${error.message}
            </td></tr>
        `;
    }
}

// Display suppliers in table
function displaySuppliers(suppliers) {
    const tbody = document.getElementById('suppliersTableBody');
    
    if (suppliers.length === 0) {
        tbody.innerHTML = '<tr><td colspan="6" class="text-center text-muted">No suppliers found</td></tr>';
        return;
    }
    
    tbody.innerHTML = suppliers.map(supplier => `
        <tr>
            <td><strong>${supplier.supplier_name}</strong></td>
            <td>${supplier.contact_person || 'N/A'}</td>
            <td>${supplier.email || 'N/A'}</td>
            <td>${supplier.phone || 'N/A'}</td>
            <td><span class="badge bg-info">${supplier.products_count || 0}</span></td>
            <td>
                <button class="btn btn-sm btn-primary" onclick="editSupplier(${supplier.supplier_id})">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-danger" onclick="deleteSupplier(${supplier.supplier_id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
}

// Add supplier form submission
document.getElementById('addSupplierForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        const formData = getFormData('addSupplierForm');
        
        const response = await apiRequest('/suppliers', {
            method: 'POST',
            body: JSON.stringify(formData)
        });
        
        if (response.success) {
            showAlert('Supplier added successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('addSupplierModal')).hide();
            resetForm('addSupplierForm');
            loadSuppliers(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error adding supplier: ' + error.message, 'danger');
    }
});

// Edit supplier
async function editSupplier(supplierId) {
    try {
        const response = await apiRequest(`/suppliers/${supplierId}`);
        
        if (response.success) {
            const supplier = response.data;
            
            // Populate edit form
            document.getElementById('editSupplierId').value = supplier.supplier_id;
            document.getElementById('edit_supplier_name').value = supplier.supplier_name;
            document.getElementById('edit_contact_person').value = supplier.contact_person || '';
            document.getElementById('edit_email').value = supplier.email || '';
            document.getElementById('edit_phone').value = supplier.phone || '';
            document.getElementById('edit_address').value = supplier.address || '';
            
            // Show modal
            new bootstrap.Modal(document.getElementById('editSupplierModal')).show();
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error loading supplier: ' + error.message, 'danger');
    }
}

// Edit supplier form submission
document.getElementById('editSupplierForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    try {
        const supplierId = document.getElementById('editSupplierId').value;
        const formData = getFormData('editSupplierForm');
        
        const response = await apiRequest(`/suppliers/${supplierId}`, {
            method: 'PUT',
            body: JSON.stringify(formData)
        });
        
        if (response.success) {
            showAlert('Supplier updated successfully!', 'success');
            bootstrap.Modal.getInstance(document.getElementById('editSupplierModal')).hide();
            loadSuppliers(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error updating supplier: ' + error.message, 'danger');
    }
});

// Delete supplier
async function deleteSupplier(supplierId) {
    const confirmed = await confirmAction('Are you sure you want to delete this supplier?');
    
    if (!confirmed) return;
    
    try {
        const response = await apiRequest(`/suppliers/${supplierId}`, {
            method: 'DELETE'
        });
        
        if (response.success) {
            showAlert('Supplier deleted successfully!', 'success');
            loadSuppliers(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting supplier: ' + error.message, 'danger');
    }
}

// Load initial data
document.addEventListener('DOMContentLoaded', () => {
    loadSuppliers(1);
});