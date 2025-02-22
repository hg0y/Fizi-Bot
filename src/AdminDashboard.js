// src/AdminDashboard.js
import React, { useEffect, useState } from "react";

function AdminDashboard() {
  const [users, setUsers] = useState([]);
  const [search, setSearch] = useState("");

  // جلب قائمة المستخدمين من Flask API
  useEffect(() => {
    fetchUsers();
  }, []);

  const fetchUsers = async () => {
    try {
      const res = await fetch("http://localhost:5000/api/users");
      const data = await res.json();
      setUsers(data.users || []);
    } catch (error) {
      console.error("خطأ في جلب المستخدمين:", error);
    }
  };

  // دالة تحديث الـ XP
  const updateXP = async (userId) => {
    const newXP = prompt("أدخل قيمة XP الجديدة:");
    if (newXP) {
      try {
        await fetch("http://localhost:5000/api/update_xp", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: userId, xp: parseInt(newXP) }),
        });
        fetchUsers();
      } catch (error) {
        console.error("خطأ في تحديث XP:", error);
      }
    }
  };

  // دالة إعادة ضبط المستخدم
  const resetUser = async (userId) => {
    if (window.confirm("هل أنت متأكد أنك تريد إعادة ضبط هذا المستخدم؟")) {
      try {
        await fetch("http://localhost:5000/api/reset_user", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ id: userId }),
        });
        fetchUsers();
      } catch (error) {
        console.error("خطأ في إعادة ضبط المستخدم:", error);
      }
    }
  };

  // فلترة المستخدمين بالاسم
  const filteredUsers = users.filter((u) =>
    u.username.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div style={{ padding: "20px" }}>
      <h1>لوحة تحكم الإدارة</h1>
      <input
        type="text"
        placeholder="ابحث عن مستخدم..."
        onChange={(e) => setSearch(e.target.value)}
        value={search}
      />
      <table style={{ width: "100%", marginTop: "10px", borderCollapse: "collapse" }}>
        <thead>
          <tr>
            <th>المعرف</th>
            <th>الاسم</th>
            <th>XP</th>
            <th>المستوى</th>
            <th>إجراءات</th>
          </tr>
        </thead>
        <tbody>
          {filteredUsers.length > 0 ? (
            filteredUsers.map((user) => (
              <tr key={user.id}>
                <td>{user.id}</td>
                <td>{user.username}</td>
                <td>{user.xp}</td>
                <td>{user.level}</td>
                <td>
                  <button onClick={() => updateXP(user.id)}>تعديل XP</button>
                  <button onClick={() => resetUser(user.id)}>إعادة ضبط</button>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td colSpan="5">لم يتم العثور على مستخدمين</td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}

export default AdminDashboard;
