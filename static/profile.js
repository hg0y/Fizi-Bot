document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ ملف profile.js تم تحميله بنجاح!");

    // 🟢 تحديث شريط XP بشكل ديناميكي
    const xpBar = document.querySelector(".xp-bar");
    if (xpBar) {
        const currentXP = parseInt(xpBar.style.width);
        xpBar.style.transition = "width 1.5s ease-in-out";
        xpBar.style.width = currentXP + "%";
    }

    // 🟢 إظهار رسالة ترحيب متحركة
    const usernameElement = document.querySelector(".username");
    if (usernameElement) {
        usernameElement.style.opacity = "0";
        usernameElement.style.transform = "translateY(-10px)";
        setTimeout(() => {
            usernameElement.style.opacity = "1";
            usernameElement.style.transform = "translateY(0)";
            usernameElement.style.transition = "all 1s ease-in-out";
        }, 500);
    }

    // ✅ إزالة أي زر مكرر
    const existingXPButton = document.querySelector(".update-xp-btn");
    if (existingXPButton) {
        existingXPButton.remove();
    }

    // 🟢 إنشاء زر تحديث XP
    const updateXPButton = document.createElement("button");
    updateXPButton.innerHTML = "🔄 تحديث XP";
    updateXPButton.classList.add("update-xp-btn");
    document.querySelector(".container").appendChild(updateXPButton);

    updateXPButton.addEventListener("click", function () {
        fetch("/update_xp")  // استدعاء API لتحديث XP
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert(`✅ تم تحديث XP إلى ${data.new_xp}`);
                    document.querySelector(".user-info b:nth-of-type(2)").nextSibling.textContent = ` ${data.new_xp}`;
                    xpBar.style.width = (data.new_xp % 100) + "%";
                } else {
                    alert("❌ حدث خطأ أثناء تحديث XP.");
                }
            })
            .catch(error => console.error("❌ خطأ في جلب بيانات XP:", error));
    });
});
