// Aguarda até que o DOM esteja totalmente carregado
$(document).ready(function() {
    // Função para exibir um alerta quando o botão é clicado
    $('button').click(function() {
        alert('Tarefa adicionada ou editada com sucesso!');
    });

    // Adiciona animação ao passar o mouse sobre os botões
    $('button').hover(
        function() {
            $(this).css('background-color', '#27ae60'); // Verde mais escuro ao passar o mouse
        },
        function() {
            $(this).css('background-color', '#2ecc71'); // Verde original
        }
    );

    // Adiciona efeito de foco aos inputs
    $('input').focus(function() {
        $(this).css('border-color', '#e74c3c'); // Vermelho ao focar
    }).blur(function() {
        $(this).css('border-color', '#3498db'); // Azul ao desfocar
    });

    // Efeito de animação ao mostrar a tabela de tarefas
    if ($('table').length > 0) {
        $('table').hide().fadeIn(1000); // Mostra a tabela com uma animação de desvanecimento
    }
});

