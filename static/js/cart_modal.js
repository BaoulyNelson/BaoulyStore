document.addEventListener("DOMContentLoaded", () => {
  const cartBtn = document.getElementById("cartBtn");
  const cartModal = document.getElementById("cartModal");
  const closeCartModal = document.getElementById("closeCartModal");
  const continueShopping = document.getElementById("continueShopping");

  // -------------------------
  // Modal
  // -------------------------
  if (cartBtn && cartModal) {
    cartBtn.addEventListener("click", (e) => {
      e.preventDefault();
      cartModal.classList.add("show");
      document.body.style.overflow = "hidden";
    });
  }

  const closeModal = () => {
    cartModal?.classList.remove("show");
    document.body.style.overflow = "";
    cartBtn?.focus(); // accessibilité : retour focus
  };

  if (closeCartModal) closeCartModal.addEventListener("click", closeModal);
  if (continueShopping) continueShopping.addEventListener("click", closeModal);

  cartModal?.addEventListener("click", (e) => {
    if (e.target === cartModal) closeModal();
  });

  // -------------------------
  // CSRF
  // -------------------------
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let cookie of cookies) {
        cookie = cookie.trim();
        if (cookie.startsWith(name + "=")) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  const csrftoken = getCookie("csrftoken");

  // -------------------------
  // Fonction mise à jour globales
  // -------------------------
  function updateTotals() {
    let subtotal = 0;

    document.querySelectorAll(".item-total").forEach((el) => {
      const value = parseFloat(el.textContent.replace(/[^\d.]/g, "")) || 0;
      subtotal += value;
    });

    const livraison = 0; // gratuit pour l’instant

    const subtotalElement = document.getElementById("subtotal-panier");
    if (subtotalElement) {
      subtotalElement.textContent = subtotal.toFixed(2) + " HTG";
    }

    const totalElement = document.getElementById("total-panier");
    if (totalElement) {
      totalElement.textContent = (subtotal + livraison).toFixed(2) + " HTG";
    }
  }

  // -------------------------
  // Gestion des quantités
  // -------------------------
  document
    .querySelectorAll(".quantity-btn.increase, .quantity-btn.decrease")
    .forEach((button) => {
      button.addEventListener("click", async () => {
        const input = button.classList.contains("increase")
          ? button.previousElementSibling
          : button.nextElementSibling;

        if (!input) return;

        let value = parseInt(input.value) || 1;
        const produitId = input.dataset.produitId;

        const cartItem = input.closest(".cart-item");
        const unitPriceText = cartItem?.querySelector(".cart-item-price")?.textContent || "0";
        const unitPrice = parseFloat(unitPriceText.replace(/[^\d.]/g, "")) || 0;

        // 🔹 Mise à jour optimiste (instantanée)
        if (button.classList.contains("increase")) {
          value = Math.min(value + 1, 10);
        } else {
          value = Math.max(value - 1, 1);
        }
        input.value = value;

        const itemTotal = unitPrice * value;
        const itemTotalElement = cartItem?.querySelector(".item-total");
        if (itemTotalElement) {
          itemTotalElement.textContent = itemTotal.toFixed(2);
        }

        updateTotals(); // recalcul rapide côté client

        // 🔹 Correction avec le backend
        try {
       
          const response = await fetch(`/modifier-quantite/${produitId}/${value}/`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": csrftoken,
                    "X-Requested-With": "XMLHttpRequest",
                },
                });

   


          const data = await response.json();

          // Mise à jour sécurisée avec les vraies données du backend
          if (itemTotalElement) {
            itemTotalElement.textContent = parseFloat(data.item_total).toFixed(2);
          }

          const subtotalElement = document.getElementById("subtotal-panier");
          if (subtotalElement) {
            subtotalElement.textContent = data.total.toFixed(2) + " HTG";
          }

          const totalElement = document.getElementById("total-panier");
          if (totalElement) {
            totalElement.textContent = data.total.toFixed(2) + " HTG";
          }

          const cartCount = document.querySelector(".cart-count");
          if (cartCount) {
            cartCount.textContent = data.panier_count;
          }

                const payButton = document.getElementById("btn-payer");
                if (payButton) {
                    payButton.style.display = "inline-block";
                    if (data.payment_url) {
                        payButton.setAttribute("href", data.payment_url);
                        payButton.disabled = false;
                    } else {
                        payButton.removeAttribute("href");
                        payButton.disabled = true;
                        payButton.textContent = "MonCash non disponible pour ce panier";
                    }
                }


        } catch (error) {
          console.error("Erreur (quantité):", error);
          alert("⚠️ Impossible de mettre à jour la quantité. Réessaie plus tard.");
        }
      });
    });
});
