// Sales Page JavaScript

let currentPage = 1;
const perPage = 20;

// Load products for dropdown
async function loadProductsDropdown() {
    try {
        const data = await apiRequest('/products?per_page=100');
        if (data.success) {
            const productSelect = document.querySelector('select[name="product_id"]');
            if (productSelect) {
                productSelect.innerHTML = '<option value="">Select Product</option>' + 
                    data.data.map(p => `<option value="${p.product_id}" data-price="${p.price}">${p.product_name} (${p.sku})</option>`).join('');
                
                // Auto-fill price when product is selected
                productSelect.addEventListener('change', function() {
                    const selectedOption = this.options[this.selectedIndex];
                    const price = selectedOption.getAttribute('data-price');
                    if (price) {
                        document.querySelector('[name="unit_price"]').value = price;
                        calculateTotal();
                    }
                });
            }
        }
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

// Calculate total amount
function calculateTotal() {
    const quantity = parseFloat(document.querySelector('[name="quantity_sold"]').value) || 0;
    const price = parseFloat(document.querySelector('[name="unit_price"]').value) || 0;
    const total = quantity * price;
    document.querySelector('[name="total_amount"]').value = total.toFixed(2);
}

// Load sales
async function loadSales(page = 1, dateFrom = '', dateTo = '') {
    try {
        showLoading('salesTableBody');
        
        let url = `/sales?page=${page}&per_page=${perPage}`;
        
        if (dateFrom) {
            url += `&start_date=${dateFrom}`;
        }
        if (dateTo) {
            url += `&end_date=${dateTo}`;
        }
        
        const data = await apiRequest(url);
        
        if (data.success) {
            displaySales(data.data, data.pagination ? data.pagination.total : data.data.length);
            await loadSalesSummary(dateFrom, dateTo);
        } else {
            throw new Error(data.message);
        }
    } catch (error) {
        document.getElementById('salesTableBody').innerHTML = `
            <tr><td colspan="9" class="text-center text-danger">
                Error loading sales: ${error.message}
            </td></tr>
        `;
    }
}

// Display sales in table
function displaySales(sales, totalCount) {
    const tbody = document.getElementById('salesTableBody');
    
    if (sales.length === 0) {
        tbody.innerHTML = '<tr><td colspan="9" class="text-center text-muted">No sales records found</td></tr>';
        return;
    }
    
    tbody.innerHTML = sales.map(sale => `
        <tr>
            <td><strong>#${sale.sale_id}</strong></td>
            <td>${formatDate(sale.sale_date)}</td>
            <td>${sale.product ? sale.product.product_name : 'N/A'}</td>
            <td>${sale.customer_name || 'Walk-in'}</td>
            <td>${sale.quantity_sold}</td>
            <td>${formatCurrency(sale.unit_price)}</td>
            <td><strong>${formatCurrency(sale.total_amount)}</strong></td>
            <td>${sale.salesperson ? sale.salesperson.full_name : 'N/A'}</td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="deleteSale(${sale.sale_id})">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        </tr>
    `).join('');
    
    // Update transaction count in summary
    document.getElementById('totalTransactions').textContent = totalCount;
}

// Add sale form submission
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('addSaleForm');
    if (form) {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Ensure total is calculated before submitting
            calculateTotal();
            
            try {
                const formData = getFormData('addSaleForm');
                
                // Make sure total_amount is calculated
                if (!formData.total_amount || formData.total_amount === null) {
                    const quantity = parseFloat(formData.quantity_sold) || 0;
                    const price = parseFloat(formData.unit_price) || 0;
                    formData.total_amount = quantity * price;
                }
                
                const response = await apiRequest('/sales', {
                    method: 'POST',
                    body: JSON.stringify(formData)
                });
                
                if (response.success) {
                    showAlert('Sale recorded successfully!', 'success');
                    const modal = bootstrap.Modal.getInstance(document.getElementById('addSaleModal'));
                    if (modal) {
                        modal.hide();
                    }
                    resetForm('addSaleForm');
                    loadSales(currentPage);
                } else {
                    showAlert('Failed to record sale: ' + response.message, 'danger');
                }
            } catch (error) {
                showAlert('Error recording sale: ' + error.message, 'danger');
            }
        });
    } else {
        console.error('addSaleForm not found');
    }
});

// Load sales summary
async function loadSalesSummary(dateFrom = '', dateTo = '') {
    try {
        let url = '/sales/total';
        
        if (dateFrom) {
            url += `?start_date=${dateFrom}`;
        }
        if (dateTo) {
            if (dateFrom) {
                url += `&end_date=${dateTo}`;
            } else {
                url += `?end_date=${dateTo}`;
            }
        }
        
        console.log('Loading sales summary with URL:', url);
        const data = await apiRequest(url);
        console.log('Sales summary response:', data);
        
        if (data.success) {
            const totalSales = data.data.total_sales || 0;
            console.log('Setting total sales to:', totalSales);
            document.getElementById('totalSalesAmount').textContent = formatCurrency(totalSales);
            
            // Transaction count is already updated in displaySales
            const transactionCount = parseInt(document.getElementById('totalTransactions').textContent) || 0;
            const averageSale = transactionCount > 0 ? totalSales / transactionCount : 0;
            document.getElementById('averageSale').textContent = formatCurrency(averageSale);
        } else {
            console.error('Sales summary API returned error:', data.message);
        }
    } catch (error) {
        console.error('Error loading sales summary:', error);
        // Reset to default values on error
        document.getElementById('totalSalesAmount').textContent = '$0.00';
        document.getElementById('totalTransactions').textContent = '0';
        document.getElementById('averageSale').textContent = '$0.00';
    }
}

// Filter sales function
function filterSales() {
    const dateFrom = document.getElementById('dateFrom').value;
    const dateTo = document.getElementById('dateTo').value;
    
    loadSales(1, dateFrom, dateTo);
}

// Delete sale
async function deleteSale(saleId) {
    const confirmed = await confirmAction('Are you sure you want to delete this sale? This will restore the product stock.');

    if (!confirmed) return;

    try {
        const response = await apiRequest(`/sales/${saleId}`, {
            method: 'DELETE'
        });

        if (response.success) {
            showAlert('Sale deleted successfully!', 'success');
            loadSales(currentPage);
        } else {
            showAlert(response.message, 'danger');
        }
    } catch (error) {
        showAlert('Error deleting sale: ' + error.message, 'danger');
    }
}

// Load initial data
document.addEventListener('DOMContentLoaded', async () => {
    console.log('Sales page loaded');
    await loadSales(1);
    loadProductsDropdown();
    
    // Add event listeners for total calculation
    document.querySelector('[name="quantity_sold"]').addEventListener('input', calculateTotal);
    document.querySelector('[name="unit_price"]').addEventListener('input', calculateTotal);
});