
(() => {

  const style = document.createElement("style");
  style.innerHTML = `
    .page-anim {
      animation: pageIn 0.22s ease-out;
    }

    .page-leave {
      animation: pageOut 0.18s ease-in forwards;
    }

    @keyframes pageIn {
      from {
        opacity: 0;
        transform: scale(0.985);
        filter: blur(6px);
      }
      to {
        opacity: 1;
        transform: scale(1);
        filter: blur(0);
      }
    }

    @keyframes pageOut {
      from {
        opacity: 1;
        transform: scale(1);
        filter: blur(0);
      }
      to {
        opacity: 0;
        transform: scale(1.01);
        filter: blur(8px);
      }
    }
  `;
  document.head.appendChild(style);

  // دخول الصفحة
  window.addEventListener("load", () => {
    document.body.classList.add("page-anim");
  });

  // خروج الصفحة عند الضغط على أي رابط
  document.addEventListener("click", (e) => {
    const link = e.target.closest("a");
    if (!link || !link.href) return;

    e.preventDefault();

    document.body.classList.add("page-leave");

    setTimeout(() => {
      window.location.href = link.href;
    }, 170);
  });

})();