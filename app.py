<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Zion v8.1 - Sistema de Agendamentos</title>
    <style>
        :root {
            --primary: #2563eb;
            --bg: #f8fafc;
            --text: #1e293b;
        }

        body { font-family: sans-serif; background: var(--bg); margin: 0; color: var(--text); }

        /* HEADER E LOGO CLICÁVEL */
        .header {
            background: white;
            padding: 1rem;
            display: flex;
            align-items: center;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        .logo-container {
            cursor: pointer;
            transition: transform 0.2s;
            display: flex;
            align-items: center;
        }

        .logo-container:hover { transform: scale(1.05); }

        .logo-img {
            width: 120px; /* Ajuste o tamanho da sua logo aqui */
            height: auto;
        }

        /* CONTEÚDO */
        .container { padding: 20px; max-width: 1000px; margin: auto; }

        /* TABELA ZION */
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        }

        th { background: var(--primary); color: white; padding: 12px; text-align: left; }
        td { padding: 12px; border-bottom: 1px solid #e2e8f0; }
        
        .empty-row {
            text-align: center;
            color: #64748b;
            font-style: italic;
            padding: 40px !important;
        }

        /* TELA DE ÍCONES (ESCONDIDA POR PADRÃO) */
        #tela-icones {
            display: none;
            grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
            gap: 20px;
            padding: 20px;
        }

        .icon-card {
            background: white;
            padding: 20px;
            text-align: center;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
    </style>
</head>
<body>

    <header class="header">
        <div class="logo-container" onclick="alternarTela()">
            <img src="https://via.placeholder.com/120x40?text=ZION+LOGOTIPO" alt="Zion Logo" class="logo-img">
        </div>
        <span style="margin-left: 15px; font-weight: bold;">Painel Administrativo</span>
    </header>

    <div class="container">
        <div id="area-agendamentos">
            <h2>Agendamentos do Dia</h2>
            <div id="tabela-placeholder"></div>
        </div>

        <div id="tela-icones">
            <div class="icon-card">📅 Agenda</div>
            <div class="icon-card">👥 Clientes</div>
            <div class="icon-card">💰 Financeiro</div>
            <div class="icon-card">⚙️ Ajustes</div>
        </div>
    </div>

    <script>
        // Dados simulados (vazio para testar o ajuste que você pediu)
        const agendamentosZion = []; 

        function renderizarTabela() {
            const placeholder = document.getElementById('tabela-placeholder');
            
            // A estrutura da tabela sempre será renderizada
            let html = `
                <table>
                    <thead>
                        <tr>
                            <th>Horário</th>
                            <th>Cliente</th>
                            <th>Serviço</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            if (agendamentosZion.length === 0) {
                // Se estiver vazio, mostra a linha de aviso em vez de sumir com tudo
                html += `
                    <tr>
                        <td colspan="4" class="empty-row">
                            Nenhum agendamento para exibir no momento.
                        </td>
                    </tr>
                `;
            } else {
                agendamentosZion.forEach(item => {
                    html += `
                        <tr>
                            <td>${item.hora}</td>
                            <td>${item.cliente}</td>
                            <td>${item.servico}</td>
                            <td>${item.status}</td>
                        </tr>
                    `;
                });
            }

            html += `</tbody></table>`;
            placeholder.innerHTML = html;
        }

        // Função para a Logo levar aos ícones
        function alternarTela() {
            const tab = document.getElementById('area-agendamentos');
            const ico = document.getElementById('tela-icones');

            if (ico.style.display === 'none' || ico.style.display === '') {
                ico.style.display = 'grid';
                tab.style.display = 'none';
            } else {
                ico.style.display = 'none';
                tab.style.display = 'block';
            }
        }

        // Inicia a tabela ao carregar a página
        window.onload = renderizarTabela;
    </script>

</body>
</html>
