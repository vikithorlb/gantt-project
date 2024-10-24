// Aguarda o DOM estar completamente carregado
document.addEventListener("DOMContentLoaded", function() {
    
    // Animação de fade-in para os elementos
    document.body.classList.add('fade-in');

    // Botão de download - alerta simples
    const downloadButton = document.querySelector('a[download="task.json"]');
    if (downloadButton) {
        downloadButton.addEventListener('click', function() {
            alert('Download do arquivo task.json em andamento!');
        });
    }

    // Validação simples do formulário
    const form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        const taskInput = document.querySelector('#task');
        const durationInput = document.querySelector('#duration');

        if (!taskInput.value.trim()) {
            alert('O nome da tarefa não pode estar vazio.');
            event.preventDefault();
        } else if (durationInput.value <= 0) {
            alert('A duração da tarefa deve ser um número positivo.');
            event.preventDefault();
        }
    });
    
});

