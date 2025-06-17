// Funciones para manejar el modal de edición de perfil
function openEditProfileModal() {
    console.log('✏️ Abriendo modal de edición de perfil...');
    const modal = document.getElementById('editProfileModal');
    if (modal) {
        modal.style.display = 'flex';
        modal.classList.add('show');
    } else {
        console.error('❌ No se encontró el modal de edición');
    }
}

function cerrarModalEdicion() {
    console.log('❌ Cerrando modal de edición...');
    const modal = document.getElementById('editProfileModal');
    if (modal) {
        modal.style.display = 'none';
        modal.classList.remove('show');
    }
}

// Cerrar modal al hacer clic fuera del contenido
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('editProfileModal');
    if (modal) {
        modal.addEventListener('click', function(e) {
            if (e.target === modal) {
                cerrarModalEdicion();
            }
        });
    }
});

// Manejar el envío del formulario de edición
document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('form-editar-perfil');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('📝 Enviando formulario de edición...');
            
            // Mostrar indicador de carga
            const submitBtn = form.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Guardando...';
            submitBtn.disabled = true;
            
            const formData = new FormData(this);
            
            // Obtener el token CSRF del DOM
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
            
            fetch(window.location.origin + '/usuarios/actualizar_perfil/', {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': csrfToken
                }
            })
            .then(response => {
                console.log('📡 Respuesta recibida:', response.status);
                return response.json();
            })
            .then(data => {
                console.log('📊 Datos recibidos:', data);
                
                // Restaurar botón
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                if (data.success) {
                    // Mostrar mensaje de éxito
                    showNotification('✅ Perfil actualizado correctamente', 'success');
                    
                    // Cerrar modal
                    cerrarModalEdicion();
                    
                    // Recargar la página después de un breve delay
                    setTimeout(() => {
                        location.reload();
                    }, 1000);
                } else {
                    // Mostrar error
                    showNotification('❌ Error al actualizar: ' + (data.error || 'Intenta de nuevo.'), 'error');
                }
            })
            .catch(err => {
                console.error('❌ Error en la petición:', err);
                
                // Restaurar botón
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
                
                showNotification('❌ Error en la conexión. Intenta de nuevo.', 'error');
            });
        });
    } else {
        console.warn('⚠️ No se encontró el formulario de edición');
    }
});

// Función para mostrar notificaciones
function showNotification(message, type = 'info') {
    // Crear elemento de notificación
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    // Estilos inline para la notificación
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000;
        font-family: inherit;
        font-size: 14px;
        max-width: 300px;
        word-wrap: break-word;
        transform: translateX(100%);
        transition: transform 0.3s ease;
    `;
    
    // Agregar al DOM
    document.body.appendChild(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.style.transform = 'translateX(0)';
    }, 100);
    
    // Remover después de 4 segundos
    setTimeout(() => {
        notification.style.transform = 'translateX(100%)';
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 300);
    }, 4000);
}

// Función para validar el formulario antes del envío
function validateForm(form) {
    const nombres = form.querySelector('[name="nombres"]').value.trim();
    const apellidos = form.querySelector('[name="apellidos"]').value.trim();
    
    if (!nombres) {
        showNotification('❌ El nombre es obligatorio', 'error');
        return false;
    }
    
    if (!apellidos) {
        showNotification('❌ Los apellidos son obligatorios', 'error');
        return false;
    }
    
    const telefono = form.querySelector('[name="telefono"]').value.trim();
    if (telefono && !/^\d{9}$/.test(telefono)) {
        showNotification('❌ El teléfono debe tener 9 dígitos', 'error');
        return false;
    }
    
    const precioHora = form.querySelector('[name="precio_hora"]').value;
    if (precioHora && (isNaN(precioHora) || parseFloat(precioHora) < 0)) {
        showNotification('❌ El precio por hora debe ser un número válido', 'error');
        return false;
    }
    
    return true;
}

// Función para previsualizar imagen
function setupImagePreview() {
    const fileInput = document.querySelector('input[name="foto"]');
    if (fileInput) {
        fileInput.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                // Validar tipo de archivo
                if (!file.type.startsWith('image/')) {
                    showNotification('❌ Por favor selecciona una imagen válida', 'error');
                    this.value = '';
                    return;
                }
                
                // Validar tamaño (máximo 5MB)
                if (file.size > 5 * 1024 * 1024) {
                    showNotification('❌ La imagen no debe superar los 5MB', 'error');
                    this.value = '';
                    return;
                }
                
                // Crear preview (opcional)
                const reader = new FileReader();
                reader.onload = function(e) {
                    // Aquí podrías mostrar una vista previa de la imagen
                    console.log('📸 Imagen cargada para preview');
                };
                reader.readAsDataURL(file);
            }
        });
    }
}

// Inicializar funcionalidades adicionales
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Inicializando guardarPerfil.js...');
    
    // Configurar preview de imagen
    setupImagePreview();
    
    // Agregar manejo de teclas para cerrar modal
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const modal = document.getElementById('editProfileModal');
            if (modal && modal.style.display === 'flex') {
                cerrarModalEdicion();
            }
        }
    });
    
    console.log('✅ guardarPerfil.js inicializado correctamente');
});

// Exponer funciones globalmente para compatibilidad con onclick:
window.openEditProfileModal = openEditProfileModal;
window.cerrarModalEdicion = cerrarModalEdicion;