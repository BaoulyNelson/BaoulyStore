document.addEventListener("DOMContentLoaded", () => {
  // Variables globales
  let currentView = "grid";
  let currentSort = "date_ajout";

  // Fonction pour basculer entre les vues
  function toggleView(viewType) {
    currentView = viewType;

    const gridView = document.getElementById("grid-view");
    const listView = document.getElementById("list-view");
    const viewButtons = document.querySelectorAll(".view-btn");

    // Mise à jour des boutons
    viewButtons.forEach((btn) => {
      btn.classList.remove("active");
      if (btn.dataset.view === viewType) {
        btn.classList.add("active");
      }
    });

    // Basculement des vues
    if (viewType === "grid") {
      gridView.classList.add("active");
      gridView.style.display = "grid";
      listView.classList.remove("active");
      listView.style.display = "none";
    } else {
      listView.classList.add("active");
      listView.style.display = "block";
      gridView.classList.remove("active");
      gridView.style.display = "none";
    }

    // Sauvegarder la préférence
    localStorage.setItem("preferred_view", viewType);
  }

  // Fonction de tri des produits
  function sortProducts(sortBy) {
    const url = new URL(window.location);
    url.searchParams.set("sort", sortBy);

    showLoading();
    window.location.href = url.toString();
  }

  // Afficher le spinner de chargement
  function showLoading() {
    document.getElementById("loading").style.display = "block";
    document.getElementById("grid-view").style.opacity = "0.5";
    document.getElementById("list-view").style.opacity = "0.5";
  }

  // Masquer le spinner de chargement
  function hideLoading() {
    document.getElementById("loading").style.display = "none";
    document.getElementById("grid-view").style.opacity = "1";
    document.getElementById("list-view").style.opacity = "1";
  }

  // Ajouter au panier
  function addToCart(productId) {
    // Simulation d'un appel AJAX
    fetch(`/panier/ajouter/${productId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      },
      body: JSON.stringify({
        quantite: 1
      })
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showToast("cartToast");
          updateCartCounter();
        } else {
          alert("Erreur lors de l'ajout au panier");
        }
      })
      .catch((error) => {
        console.error("Erreur:", error);
        alert("Erreur lors de l'ajout au panier");
      });
  }

  // Ajouter aux favoris
  function addToWishlist(productId) {
    // Simulation d'un appel AJAX
    fetch(`/favoris/ajouter/${productId}/`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": getCookie("csrftoken")
      }
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          showToast("wishlistToast");
          // Mettre à jour l'icône du coeur
          const heartIcon = event.target.closest("button").querySelector("i");
          heartIcon.classList.remove("far");
          heartIcon.classList.add("fas");
          heartIcon.style.color = "#e74c3c";
        } else {
          alert("Erreur lors de l'ajout aux favoris");
        }
      })
      .catch((error) => {
        console.error("Erreur:", error);
        alert("Erreur lors de l'ajout aux favoris");
      });
  }

  // Afficher les notifications toast
  function showToast(toastId) {
    const toast = new bootstrap.Toast(document.getElementById(toastId));
    toast.show();
  }

  // Mettre à jour le compteur du panier
  function updateCartCounter() {
    // Simulation de mise à jour du compteur
    const cartCounter = document.querySelector(".cart-counter");
    if (cartCounter) {
      const currentCount = parseInt(cartCounter.textContent) || 0;
      cartCounter.textContent = currentCount + 1;
    }
  }

  // Obtenir le token CSRF
  function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
      const cookies = document.cookie.split(";");
      for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === name + "=") {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }

  // Filtrage en temps réel
  function setupLiveFilter() {
    const searchInput = document.querySelector('input[name="search"]');
    let searchTimeout;

    if (searchInput) {
      searchInput.addEventListener("input", function () {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
          filterProducts();
        }, 500);
      });
    }

    // Filtrage par catégorie, couleur, etc.
    const filterSelects = document.querySelectorAll(
      'select[name="categorie"], select[name="nom"], select[name="couleur"]'
    );
    filterSelects.forEach((select) => {
      select.addEventListener("change", filterProducts);
    });

    // Checkboxes
    const filterCheckboxes = document.querySelectorAll(
      'input[name="populaire"], input[name="nouveau"]'
    );
    filterCheckboxes.forEach((checkbox) => {
      checkbox.addEventListener("change", filterProducts);
    });
  }

  // Filtrer les produits côté client (optionnel)
  function filterProducts() {
    const formData = new FormData(document.getElementById("filter-form"));
    const params = new URLSearchParams();

    for (let [key, value] of formData.entries()) {
      if (value.trim() !== "") {
        params.append(key, value);
      }
    }

    // Redirection avec les nouveaux paramètres
    window.location.search = params.toString();
  }

  // Animation d'apparition des cartes
  function animateCards() {
    const cards = document.querySelectorAll(
      ".product-card, .product-list-item"
    );

    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.style.opacity = "0";
            entry.target.style.transform = "translateY(20px)";
            entry.target.style.transition =
              "opacity 0.6s ease, transform 0.6s ease";

            setTimeout(() => {
              entry.target.style.opacity = "1";
              entry.target.style.transform = "translateY(0)";
            }, 100);

            observer.unobserve(entry.target);
          }
        });
      },
      {
        threshold: 0.1
      }
    );

    cards.forEach((card) => observer.observe(card));
  }

  // Aperçu rapide
  function showQuickView(productId) {
    // Charger les données du produit via AJAX
    fetch(`/detail_produit/${productId}/`)
      .then((response) => response.text())
      .then((html) => {
        document.getElementById("quickViewContent").innerHTML = html;
        const modal = new bootstrap.Modal(
          document.getElementById("quickViewModal")
        );
        modal.show();
      })
      .catch((error) => {
        console.error("Erreur:", error);
        alert("Erreur lors du chargement de l'aperçu");
      });
  }

  // Lazy loading des images
  function setupLazyLoading() {
    const images = document.querySelectorAll("img[data-src]");

    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.classList.remove("lazy");
          observer.unobserve(img);
        }
      });
    });

    images.forEach((img) => imageObserver.observe(img));
  }

  // Gestion des favoris
  function toggleFavorite(productId, element) {
    const icon = element.querySelector("i");
    const isFavorite = icon.classList.contains("fas");

    fetch(`/favoris/${isFavorite ? "retirer" : "ajouter"}/${productId}/`, {
      method: "POST",
      headers: {
        "X-CSRFToken": getCookie("csrftoken")
      }
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.success) {
          if (isFavorite) {
            icon.classList.remove("fas");
            icon.classList.add("far");
            icon.style.color = "";
          } else {
            icon.classList.remove("far");
            icon.classList.add("fas");
            icon.style.color = "#e74c3c";
            showToast("wishlistToast");
          }
        }
      })
      .catch((error) => console.error("Erreur:", error));
  }

  // Gestion du scroll infini (optionnel)
  function setupInfiniteScroll() {
    let loading = false;
    let page = 1;

    window.addEventListener("scroll", () => {
      if (loading) return;

      if (
        window.innerHeight + window.scrollY >=
        document.body.offsetHeight - 1000
      ) {
        loading = true;
        loadMoreProducts();
      }
    });
  }

  function loadMoreProducts() {
    // Implémentation du chargement de plus de produits
    // Cette fonction devrait être adaptée selon votre backend
  }

  // Initialisation au chargement de la page
  document.addEventListener("DOMContentLoaded", function () {
    // Restaurer la vue préférée
    const preferredView = localStorage.getItem("preferred_view");
    if (preferredView && preferredView !== currentView) {
      toggleView(preferredView);
    }

    // Initialiser les fonctionnalités
    setupLiveFilter();
    animateCards();
    setupLazyLoading();
    hideLoading();

    // Gestion des événements sur les boutons d'action
    document.addEventListener("click", function (e) {
      // Aperçu rapide
      if (e.target.closest('.action-btn[title="Aperçu rapide"]')) {
        e.preventDefault();
        const productCard = e.target.closest(".product-card");
        const productId = productCard.dataset.productId || 1; // À adapter
        showQuickView(productId);
      }

      // Favoris
      if (e.target.closest('.action-btn[title="Ajouter aux favoris"]')) {
        e.preventDefault();
        const productCard = e.target.closest(".product-card");
        const productId = productCard.dataset.productId || 1; // À adapter
        addToWishlist(productId);
      }
    });

    // Auto-submit du formulaire de tri
    const sortSelect = document.querySelector(
      'select[onchange="sortProducts(this.value)"]'
    );
    if (sortSelect) {
      // Récupérer le tri actuel depuis l'URL
      const urlParams = new URLSearchParams(window.location.search);
      const currentSort = urlParams.get("sort");
      if (currentSort) {
        sortSelect.value = currentSort;
      }
    }

    // Gestion responsive du toggle view sur mobile
    if (window.innerWidth <= 768) {
      // Par défaut en vue liste sur mobile
      toggleView("list");
    }
  });

  // Gestion du redimensionnement de la fenêtre
  window.addEventListener("resize", function () {
    // Ajustements responsive si nécessaire
    if (window.innerWidth <= 768 && currentView === "grid") {
      // Optionnel: basculer automatiquement en vue liste sur mobile
      // toggleView('list');
    }
  });

  // Fonction utilitaire pour formater les prix
  function formatPrice(price) {
    return new Intl.NumberFormat("fr-FR", {
      style: "currency",
      currency: "EUR"
    }).format(price);
  }

  // Fonction pour mettre à jour l'URL sans rechargement
  function updateURL(params) {
    const url = new URL(window.location);
    Object.keys(params).forEach((key) => {
      if (params[key]) {
        url.searchParams.set(key, params[key]);
      } else {
        url.searchParams.delete(key);
      }
    });
    history.pushState(null, "", url.toString());
  }
});
