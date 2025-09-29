document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('articleForm');
    const progressBar = document.getElementById('formProgress');
    const floatingSave = document.getElementById('floatingSave');
    const fileInput = form.querySelector('input[type="file"]');
    const fileDisplay = document.getElementById('fileInputDisplay');
    const imagePreview = document.getElementById('imagePreview');
    const colorInput = form.querySelector('input[name="couleur"]');
    const colorPreview = document.getElementById('colorPreview');
    const saveBtn = document.getElementById('saveBtn');

    // Calcul et mise à jour de la progression du formulaire
    function updateProgress() {
        const inputs = form.querySelectorAll('input[required], select[required], textarea[required]');
        let completed = 0;
        
        inputs.forEach(input => {
            if (input.type === 'checkbox') {
                if (input.checked) completed++;
            } else if (input.value.trim() !== '') {
                completed++;
            }
        });
        
        const progress = (completed / inputs.length) * 100;
        progressBar.style.width = progress + '%';
        
        // Afficher/masquer le bouton flottant
        if (progress > 50 && window.scrollY > 200) {
            floatingSave.classList.add('visible');
        } else {
            floatingSave.classList.remove('visible');
        }
    }

    // Gestion de l'upload d'image
    if (fileInput && fileDisplay) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                fileDisplay.classList.add('has-file');
                fileDisplay.innerHTML = `
                    <i class="fas fa-check-circle fa-2x text-success"></i>
                    <div>
                        <strong>${file.name}</strong>
                        <div class="text-muted">${(file.size / 1024 / 1024).toFixed(2)} MB</div>
                    </div>
                `;
                
                // Prévisualisation de l'image
                const reader = new FileReader();
                reader.onload = function(e) {
                    imagePreview.innerHTML = `
                        <img src="${e.target.result}" alt="Prévisualisation" class="image-preview">
                    `;
                };
                reader.readAsDataURL(file);
            }
            updateProgress();
        });

        // Drag & Drop
        fileDisplay.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = '#0066cc';
            this.style.background = '#e3f2fd';
        });

        fileDisplay.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.borderColor = '#dee2e6';
            this.style.background = '#f8f9fa';
        });

        fileDisplay.addEventListener('drop', function(e) {
            e.preventDefault();
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                fileInput.files = files;
                fileInput.dispatchEvent(new Event('change'));
            }
            this.style.borderColor = '#dee2e6';
            this.style.background = '#f8f9fa';
        });
    }

    // Prévisualisation de la couleur
    if (colorInput && colorPreview) {
        colorInput.addEventListener('input', function() {
            colorPreview.style.background = this.value;
        });
        
        // Initialiser la couleur si elle existe
        if (colorInput.value) {
            colorPreview.style.background = colorInput.value;
        }
    }

    // Validation en temps réel
    const inputs = form.querySelectorAll('input, select, textarea');
    inputs.forEach(input => {
        input.addEventListener('input', updateProgress);
        input.addEventListener('blur', function() {
            if (this.hasAttribute('required') && !this.value.trim()) {
                this.classList.add('is-invalid');
            } else {
                this.classList.remove('is-invalid');
            }
        });
    });

    // Gestion du scroll pour le bouton flottant
    window.addEventListener('scroll', updateProgress);

    // Animation des boutons
    const buttons = document.querySelectorAll('.btn-custom');
    buttons.forEach(btn => {
        btn.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px) scale(1.02)';
        });
        
        btn.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Gestion de la soumission du formulaire
    form.addEventListener('submit', function(e) {
        saveBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i><span>Sauvegarde...</span>';
        saveBtn.disabled = true;
        
        // Validation côté client
        let isValid = true;
        const requiredInputs = form.querySelectorAll('[required]');
        
        requiredInputs.forEach(input => {
            if (!input.value.trim()) {
                input.classList.add('is-invalid');
                isValid = false;
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            saveBtn.innerHTML = '<i class="fas fa-save"></i><span>Enregistrer</span>';
            saveBtn.disabled = false;
            
            // Scroll vers le premier champ en erreur
            const firstError = form.querySelector('.is-invalid');
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                firstError.focus();
            }
        }
    });

    // Auto-sauvegarde (optionnel)
    let autoSaveTimer;
    inputs.forEach(input => {
        input.addEventListener('input', function() {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {
                // Ici vous pourriez implémenter une sauvegarde automatique
                console.log('Auto-sauvegarde déclenchée');
            }, 30000); // 30 secondes
        });
    });

    // Initialisation
    updateProgress();
    
    // Focus sur le premier champ
    const firstInput = form.querySelector('input, select, textarea');
    if (firstInput) {
        firstInput.focus();
    }
});

// Fonction pour confirmer la navigation
window.addEventListener('beforeunload', function(e) {
    const form = document.getElementById('articleForm');
    const formData = new FormData(form);
    let hasData = false;
    
    for (let [key, value] of formData.entries()) {
        if (value && key !== 'csrfmiddlewaretoken') {
            hasData = true;
            break;
        }
    }
    
    if (hasData) {
        e.preventDefault();
        e.returnValue = 'Vous avez des modifications non sauvegardées. Voulez-vous vraiment quitter?';
        return e.returnValue;
    }
});