// Función para buscar RUC - VERSIÓN CORREGIDA
function buscarRUC(event) {
    const ruc = document.getElementById('id_ruc').value;

    if (!ruc || ruc.length !== 11) {
        alert('Por favor ingresa un RUC válido de 11 dígitos');
        return;
    }

    // Mostrar loading en el botón
    const btnBuscar = event.target;
    const textoOriginal = btnBuscar.textContent;
    btnBuscar.textContent = 'Buscando...';
    btnBuscar.disabled = true;

    // CORRECCIÓN: Usar la ruta correcta que está definida en Django
    fetch(`/usuarios/buscar-ruc/?ruc=${ruc}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                const razonSocialInput = document.getElementById('id_razon_social');
                
                // Usar método seguro para actualizar valor
                if (razonSocialInput && razonSocialInput.actualizarValor) {
                    razonSocialInput.actualizarValor(data.razon_social || '');
                } else {
                    // Fallback si la función segura no está disponible
                    razonSocialInput.value = data.razon_social || '';
                }

                mostrarMensaje('Datos de la empresa encontrados y cargados correctamente', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarMensaje('Error al buscar el RUC. Intenta nuevamente.', 'error');
        })
        .finally(() => {
            btnBuscar.textContent = textoOriginal;
            btnBuscar.disabled = false;
        });
}

// Función para buscar DNI (ya funciona correctamente)
function buscarDNI(event) {
    const dni = document.getElementById('id_dni').value;

    if (!dni || dni.length !== 8) {
        alert('Por favor ingresa un DNI válido de 8 dígitos');
        return;
    }

    // Mostrar loading en el botón
    const btnBuscar = event.target;
    const textoOriginal = btnBuscar.textContent;
    btnBuscar.textContent = 'Buscando...';
    btnBuscar.disabled = true;

    fetch(`/usuarios/buscar-dni/?dni=${dni}`)
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                alert('Error: ' + data.error);
            } else {
                // Usar funciones seguras para setear los datos
                const nombreInput = document.getElementById('id_nombre');
                const apellidoInput = document.getElementById('id_apellido');

                let apellidos = '';
                if (data.apellido_paterno) apellidos += data.apellido_paterno;
                if (data.apellido_materno) apellidos += ' ' + data.apellido_materno;

                // Usar método seguro para actualizar valores
                if (nombreInput && nombreInput.actualizarValor) {
                    nombreInput.actualizarValor(data.nombres || '');
                } else {
                    nombreInput.value = data.nombres || '';
                }

                if (apellidoInput && apellidoInput.actualizarValor) {
                    apellidoInput.actualizarValor(apellidos.trim());
                } else {
                    apellidoInput.value = apellidos.trim();
                }

                mostrarMensaje('Datos encontrados y cargados correctamente', 'success');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            mostrarMensaje('Error al buscar el DNI. Intenta nuevamente.', 'error');
        })
        .finally(() => {
            btnBuscar.textContent = textoOriginal;
            btnBuscar.disabled = false;
        });
}

// Función para mostrar mensajes (reemplaza los alerts)
function mostrarMensaje(mensaje, tipo) {
    // Remover mensaje anterior si existe
    const mensajeAnterior = document.querySelector('.mensaje-temporal');
    if (mensajeAnterior) {
        mensajeAnterior.remove();
    }
    
    // Crear nuevo mensaje
    const div = document.createElement('div');
    div.className = `mensaje-temporal alert-${tipo}`;
    div.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 12px 20px;
        border-radius: 4px;
        color: white;
        font-weight: bold;
        z-index: 1000;
        animation: slideIn 0.3s ease-out;
        ${tipo === 'success' ? 'background-color: #28a745;' : 'background-color: #dc3545;'}
    `;
    div.textContent = mensaje;
    
    // Agregar animación CSS si no existe
    if (!document.querySelector('#mensaje-styles')) {
        const style = document.createElement('style');
        style.id = 'mensaje-styles';
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);
    }
    
    document.body.appendChild(div);
    
    // Remover después de 3 segundos
    setTimeout(() => {
        if (div.parentNode) {
            div.remove();
        }
    }, 3000);
}

// Validación adicional en tiempo real
document.addEventListener('DOMContentLoaded', function() {
    const dniInput = document.getElementById('id_dni');
    const rucInput = document.getElementById('id_ruc');
    
    // Función para validar solo números
    function soloNumeros(event) {
        const key = event.key;
        if (!/[0-9]/.test(key) && key !== 'Backspace' && key !== 'Delete' &&
            key !== 'Tab' && key !== 'ArrowLeft' && key !== 'ArrowRight') {
            event.preventDefault();
        }
    }

    // Validar DNI solo números
    if (dniInput) {
        dniInput.addEventListener('keydown', soloNumeros);
        dniInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 8) {
                this.value = this.value.slice(0, 8);
            }
        });
    }
    
    // Validar RUC solo números
    if (rucInput) {
        rucInput.addEventListener('keydown', soloNumeros);
        rucInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '');
            if (this.value.length > 11) {
                this.value = this.value.slice(0, 11);
            }
        });
    }
});