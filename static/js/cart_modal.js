/**
 * cart_modal.js — Modal panier + mise à jour quantités via AJAX
 * Endpoint: /panier/modifier/{produitId}/{quantite}/
 */
document.addEventListener("DOMContentLoaded", () => {
  const cartBtn     = document.getElementById("cartBtn");
  const cartModal   = document.getElementById("cartModal");
  const closeBtn    = document.getElementById("closeCartModal");
  const continueBtn = document.getElementById("continueShopping");

  const openModal  = () => { cartModal?.classList.add("show");    document.body.style.overflow = "hidden"; };
  const closeModal = () => { cartModal?.classList.remove("show"); document.body.style.overflow = "";       cartBtn?.focus(); };

  // ✅ Détecter le flag ?open_cart=1 et ouvrir le modal automatiquement
  const params = new URLSearchParams(window.location.search);
  if (params.get("open_cart") === "1") {
    openModal();
    // Nettoyer l'URL sans recharger la page
    const cleanUrl = window.location.pathname;
    window.history.replaceState({}, document.title, cleanUrl);
  }

  cartBtn?.addEventListener("click", e => { e.preventDefault(); openModal(); });
  closeBtn?.addEventListener("click", closeModal);
  continueBtn?.addEventListener("click", () => { closeModal(); window.location.href = "/produits/"; });
  cartModal?.addEventListener("click", e => { if (e.target === cartModal) closeModal(); });

  function getCsrf() {
    for (const c of document.cookie.split(";")) {
      const [k, v] = c.trim().split("=");
      if (k === "csrftoken") return decodeURIComponent(v);
    }
    return "";
  }

  /**
   * ✅ FIX BUG 3 — Gère le format français "1 800,00 HTG"
   * Étapes : supprimer espaces → remplacer virgule par point → garder chiffres/point
   */
  function parsePrice(text) {
    return parseFloat(
      (text || "0")
        .replace(/\s/g, "")      // "1 800,00 HTG" → "1800,00HTG"
        .replace(",", ".")       // "1800,00HTG"   → "1800.00HTG"
        .replace(/[^\d.]/g, "") // "1800.00HTG"   → "1800.00"
    ) || 0;
  }

  function recalcTotals() {
    let total = 0;
    document.querySelectorAll(".item-total").forEach(el => {
      total += parseFloat(el.textContent) || 0;
    });
    const el = document.getElementById("total-panier");
    const subEl = document.getElementById("subtotal-panier");
    if (el)    el.textContent    = total.toFixed(2) + " HTG";
    if (subEl) subEl.textContent = total.toFixed(2) + " HTG";
  }

  document.querySelectorAll(".quantity-btn").forEach(btn => {
    btn.addEventListener("click", async () => {
      const isUp  = btn.classList.contains("increase");
      const input = isUp ? btn.previousElementSibling : btn.nextElementSibling;
      if (!input) return;

      let qty = parseInt(input.value) || 1;
      const id = input.dataset.produitId;
      const cartItem = input.closest(".cart-item");

      // ✅ FIX BUG 3 — parsePrice() au lieu de replace(/[^\d.]/g,"")
      const unitPrice = parsePrice(
        cartItem?.querySelector(".cart-item-price")?.textContent || "0"
      );

      qty = isUp ? qty + 1 : Math.max(qty - 1, 1);
      input.value = qty;

      const itemTotalEl = cartItem?.querySelector(".item-total");
      if (itemTotalEl) itemTotalEl.textContent = (unitPrice * qty).toFixed(2);
      recalcTotals();

      try {
        const res = await fetch(`/panier/modifier/${id}/${qty}/`, {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
            "X-CSRFToken": getCsrf(),
            "X-Requested-With": "XMLHttpRequest",
          },
        });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const d = await res.json();

        if (itemTotalEl) itemTotalEl.textContent = parseFloat(d.item_total).toFixed(2);

        const totalEl = document.getElementById("total-panier");
        const subEl   = document.getElementById("subtotal-panier");
        if (totalEl) totalEl.textContent = parseFloat(d.total).toFixed(2) + " HTG";
        if (subEl)   subEl.textContent   = parseFloat(d.total).toFixed(2) + " HTG";

        const badge = document.querySelector(".cart-count");
        if (badge) badge.textContent = d.cart_count;

        const payBtn = document.getElementById("btn-payer");
        if (payBtn) {
          if (d.payment_url) { payBtn.href = d.payment_url; payBtn.removeAttribute("disabled"); }
          else               { payBtn.removeAttribute("href"); payBtn.setAttribute("disabled", "true"); }
        }
      } catch (err) {
        console.error("Erreur quantité:", err);
      }
    });
  });
});