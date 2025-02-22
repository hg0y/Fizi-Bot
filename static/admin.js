// 🔍 البحث الفوري عن المستخدمين
function filterUsers() {
    let input = document.getElementById("search").value.toLowerCase();
    let rows = document.querySelectorAll("tbody tr");
    rows.forEach(row => {
        let username = row.children[1].textContent.toLowerCase();
        row.style.display = username.includes(input) ? "" : "none";
    });
}

// ✏️ تعديل XP
function editUser(userId) {
    let newXP = prompt("أدخل قيمة XP الجديدة:");
    if (newXP) {
        fetch(`/update_xp/${userId}/${newXP}/`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => location.reload());
    }
}

// 🗑️ حذف المستخدم
function deleteUser(userId) {
    if (confirm("هل أنت متأكد أنك تريد حذف هذا المستخدم؟")) {
        fetch(`/delete_user/${userId}/`, {
            method: 'POST'
        })
        .then(response => response.json())
        .then(data => location.reload());
    }
}
