
/* =========================
   🌙 الوضع الليلي (Dark Mode)
========================= */
function toggleTheme(){
    document.body.classList.toggle("light");

    if(document.body.classList.contains("light")){
        localStorage.setItem("theme","light");
    }else{
        localStorage.setItem("theme","dark");
    }
}

/* تحميل الوضع المحفوظ */
window.addEventListener("load", () => {
    if(localStorage.getItem("theme") === "light"){
        document.body.classList.add("light");
    }
});


/* =========================
   🚀 تأثير الانتقال بين الصفحات
========================= */

document.addEventListener("DOMContentLoaded", () => {

    // إنشاء طبقة الانتقال إذا مش موجودة
    if(!document.getElementById("pageTransition")){
        let div = document.createElement("div");
        div.id = "pageTransition";
        document.body.appendChild(div);
    }

    let transition = document.getElementById("pageTransition");

    // دخول الصفحة
    transition.classList.add("page-in");

    setTimeout(() => {
        transition.classList.remove("page-in");
    }, 600);
});


/* عند الضغط على أي رابط */
document.addEventListener("click", function(e){

    let link = e.target.closest("a");

    if(link && link.href && link.target !== "_blank"){

        e.preventDefault();

        let transition = document.getElementById("pageTransition");

        transition.classList.add("page-out");

        setTimeout(() => {
            window.location.href = link.href;
        }, 500);
    }
});


/* =========================
   👁️ إظهار/إخفاء كلمة المرور
========================= */
function togglePassword(){
    let pass = document.getElementById("password");

    if(pass){
        pass.type = (pass.type === "password") ? "text" : "password";
    }
}