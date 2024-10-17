document.addEventListener("DOMContentLoaded", function() {

    
    // Element references
    var addButton = document.getElementById('btn-add');
    var updateButton = document.getElementById('btn-update');
    var deleteButton = document.getElementById('btn-delete');
    
    var addSection = document.getElementById('add-employee-section');
    var updateSection = document.getElementById('update-employee-section');
    var deleteSection = document.getElementById('delete-employee-section');
    
    var menuToggle = document.getElementById('menu-toggle');
    var wrapper = document.getElementById('wrapper');

    // Show a specific section and hide others
    function showSection(section) {
        // Hide all sections
        addSection.style.display = 'none';
        updateSection.style.display = 'none';
        deleteSection.style.display = 'none';
        
        // Show the selected section
        section.style.display = 'block';
    }

    // Event listeners for navigation buttons
    addButton.addEventListener('click', function() {
        showSection(addSection);
    });

    updateButton.addEventListener('click', function() {
        showSection(updateSection);
    });

    deleteButton.addEventListener('click', function() {
        showSection(deleteSection);
    });

    // Event listener for menu toggle
    menuToggle.addEventListener('click', function () {
        wrapper.classList.toggle('toggled');
    });


   
    
});

// Add Employee Form Submission
document.getElementById('add-employee-form')?.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch('/add_employee', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Update Employee Form Submission
document.getElementById('update-employee-form')?.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);

    
    try {
        const response = await fetch(`/update_employee/${data.id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Delete Employee Form Submission
document.getElementById('delete-employee-form')?.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`/delete_employee/${data.id}`, {
            method: 'DELETE'
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error('Error:', error);
    }
});

// Search Employee Form Submission
document.getElementById('search-employee-form')?.addEventListener('submit', async function (event) {
    
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch(`/search_employee`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        
        if (result.error) {
            alert(result.error);
        } else {
            // Populate employee information in the card
            document.getElementById('emp-id').textContent = result.id;
            document.getElementById('first-name').textContent = result.first_name;
            document.getElementById('last-name').textContent = result.last_name;
            document.getElementById('email').textContent = result.email;
            document.getElementById('phone').textContent = result.phone;
            document.getElementById('department').textContent = result.department;
            document.getElementById('position').textContent = result.position;
            document.getElementById('hire-date').textContent = result.hire_date;
            document.getElementById('salary').textContent = result.salary;

            // Show the employee info card
            document.getElementById('employee-info').style.display = 'block';
        }
    } catch (error) {
        console.error('Error:', error);
    }
});


document.getElementById('apply-leave-form')?.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    
    try {
        const response = await fetch('/apply_for_leave', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error('Error:', error);
    }
});



document.getElementById('apply-leave-form')?.addEventListener('submit', async function (event) {
    event.preventDefault();
    const formData = new FormData(this);
    const data = Object.fromEntries(formData);
    console.log(data)
    try {
        const response = await fetch('/apply_leave', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });
        const result = await response.json();
        alert(result.message || result.error);
    } catch (error) {
        console.error('Error:', error);
    }
});


document.querySelectorAll('.approve-btn').forEach(button => {
    button.addEventListener('click', async function () {
        const leaveId = this.getAttribute('data-id'); // Get leave_id from data-id

        console.log(leaveId)
        try {
            const response = await fetch(`/update_leave_status/${leaveId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: 'Approved' })
            });
            
            const result = await response.json();
            alert(result.message || result.error);
            
            if (response.ok) {
                this.closest('tr').querySelector('.status').innerText = 'Approved'; // Update UI
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});



document.querySelectorAll('.reject-btn').forEach(button => {
    button.addEventListener('click', async function () {
        const leaveId = this.getAttribute('data-id'); // Get leave_id from data-id
        try {
            const response = await fetch(`/update_leave_status/${leaveId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ status: 'Rejected' })
            });
            
            const result = await response.json();
            alert(result.message || result.error);
            
            if (response.ok) {
                this.closest('tr').querySelector('.status').innerText = 'Rejected'; // Update UI
            }
        } catch (error) {
            console.error('Error:', error);
        }
    });
});


function fetchEmployeeInfo() {
    const employeeId = document.getElementById('update-id').value;
   
    // Fetching employee info from Flask API
    fetch(`/get_employee/${employeeId}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Employee not found');
            }
            return response.json();
        })
        .then(data => {

            if (!data.end_date) {
                data.end_date = null;
            }

            document.getElementById('update-first-name').value = data.first_name;
            document.getElementById('update-last-name').value = data.last_name;
            document.getElementById('update-salary').value = data.salary;
            document.getElementById('update-department').value = data.department;
            document.getElementById('update-position').value = data.position;
            
            // Populate other fields similarly
            // gender = document.querySelector("input[name='Male']:checked").value
            // console.log(gender)
            document.getElementById('update-role').value = data.role;
            document.getElementById('update-hire-date').value = data.hire_date;
            document.getElementById('update-end-date').value = data.end_date;
            document.getElementById('update-email').value = data.email;
            document.getElementById('update-phone').value = data.phone;
            document.getElementById('address').value = data.address || '';

            
            const optionToSelect = document.getElementById(data.manager_id);
            if (optionToSelect) {
                optionToSelect.selected = true;
            }
        })
        .catch(error => {
            alert(error.message);
            console.log(error.message)
        });
}

