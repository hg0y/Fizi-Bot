from flask import Flask, redirect, url_for, session, render_template, request, jsonify
from authlib.integrations.flask_client import OAuth
import sqlite3
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__, template_folder="templates")
app.permanent_session_lifetime = timedelta(days=7)  # اجعل الجلسة تدوم لمدة 7 أيام

CORS(app)
app.secret_key = "supersecretkey"  # استخدم مفتاحًا أكثر أمانًا في بيئة الإنتاج

ADMIN_IDS = [339558424507449359]  # تأكد أن معرفك موجود هنا

oauth = OAuth(app)
discord = oauth.register(
    name="discord",
    client_id="1342058097555935304",  # استبدل بـ Client ID الفعلي
    client_secret="Ip9eHWC4nlorwwLHJd35G5MRx20l1c7y",  # استبدل بـ Client Secret الفعلي
    access_token_url="https://discord.com/api/oauth2/token",
    authorize_url="https://discord.com/api/oauth2/authorize",
    api_base_url="https://discord.com/api/",
    client_kwargs={"scope": "identify"},
)

@app.route("/")
def home():
    if "user" not in session:
        return render_template("index.html")

    user_id = int(session["user"]["id"])
    
    conn = sqlite3.connect("database/database.db")
    cur = conn.cursor()
    cur.execute("SELECT xp, level FROM xp WHERE user_id=?", (user_id,))
    result = cur.fetchone()
    conn.close()

    xp, level = result if result else (0, 1)

    return render_template("profile.html", user=session["user"], xp=xp, level=level)

@app.route("/login")
def login():
    if "user" in session:  # إذا كان المستخدم مسجلاً بالفعل، لا حاجة لإعادة تسجيل الدخول
        return redirect(url_for("home"))
    
    return discord.authorize_redirect(redirect_uri="http://127.0.0.1:5000/callback")

@app.route("/callback")
def callback():
    if "user" in session:  # التحقق إذا كان المستخدم مسجلاً بالفعل لمنع إعادة التوجيه المتكرر
        return redirect(url_for("home"))

    token = discord.authorize_access_token()
    user = discord.get("users/@me", token=token).json()

    if not user:
        return "❌ فشل في جلب بيانات المستخدم من Discord", 400  # منع التكرار إذا كان المستخدم غير موجود

    session.permanent = True  # جعل الجلسة دائمة
    session["user"] = user
    session["token"] = token

    return redirect(url_for("home"))

@app.route("/logout")
def logout():
    session.clear()  # مسح الجلسة بالكامل
    return redirect(url_for("home"))

@app.route("/admin")
def admin_dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    user_id = int(session["user"]["id"])
    
    if user_id not in ADMIN_IDS:
        return "❌ ليس لديك صلاحية الوصول إلى هذه الصفحة!", 403  # رسالة خطأ في حالة عدم توفر الصلاحية

    conn = sqlite3.connect("database/database.db")
    cur = conn.cursor()
    cur.execute("SELECT user_id, xp, level FROM xp")
    users = [{"id": row[0], "xp": row[1], "level": row[2]} for row in cur.fetchall()]
    conn.close()

    # تأكد من أن القالب admin.html موجود
    try:
        return render_template("admin.html", users=users)
    except:
        return "❌ لم يتم العثور على ملف admin.html داخل مجلد templates!", 500

@app.route("/server")
def server_info():
    if "user" not in session:
        return redirect(url_for("login"))

    server_data = {
        "name": "اسم السيرفر",
        "member_count": 150,
        "owner": "مالك السيرفر"
    }

    return render_template("server_info.html", server=server_data)

if __name__ == "__main__":
    app.run(debug=True)
