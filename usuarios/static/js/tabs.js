document.addEventListener('DOMContentLoaded', function () {
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
             // Activar pestaña
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');

            // Mostrar contenido asociado
             const target = tab.getAttribute('data-tab');
            tabContents.forEach(content => {
            content.classList.remove('active');
            if (content.id === target) {
                content.classList.add('active');
            }
        });
    });
});
});