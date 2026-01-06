<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Zion v8.3 - Colunas Visíveis</title>
    <style>
        /* Estilos de Estrutura */
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; margin: 0; }
        
        /* Logo Clicável */
        .header-zion { background: #1a1a1a; padding: 15px; display: flex; align-items: center; }
        .logo-btn { cursor: pointer; border: 2px solid transparent; transition: 0.3s; }
        .logo-btn:hover { border-bottom: 2px solid #007bff; transform: translateY(-2px); }

        .container { padding: 30px; }
        
        /* TABELA COM COLUNAS FORTES */
        .tabela-zion { 
            width: 100%; 
            border-collapse: collapse; /* Une as bordas */
            background: white; 
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }

        /* Forçando a visualização das colunas */
        .tabela-zion th { 
            background-color: #007bff; 
            color: white; 
            padding: 15px;
            border: 1px solid #0056b3; /* Borda da coluna no topo */
            text-align: left;
            text-transform: uppercase;
            font-size: 14px;
        }

        .tabela-zion td { 
            padding: 12px; 
            border: 1px solid #dee2e6; /* BORDA CINZA CLARA EM TODAS AS COLUNAS */
            color: #333;
        }

        /* Efeito de listras para facilitar a leitura */
        .tabela-zion tr:nth-child(even) { background-color: #f8f9fa; }
        .tabela-zion tr:hover { background-color: #e9ecef; }

        .vazio-msg { text-align: center; font-weight: bold; color: #dc3545; padding: 30px !important; }
        .hidden { display: none; }
        
        /* Menu de Ícones */
        .grid-icones { display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; }
        .card { background: white; padding: 30px; border-radius: 10px; text-align: center; border: 1px solid #ddd; }
    </style>
</head>
<body>

    <header class="header-zion">
        <div class="logo-btn" onclick="trocarTela()">
            <img src="https://via.placeholder.com/150x50?text=ZION+LOGO" alt="Logo Zion" id="main-logo">
        </div>
        <h2 style="color: white; margin-left: 20px;">Sistema de Gestão</h2>
    </header>

    <div class="container">
        <div id="tela-tabela">
            <h3>📋 Grade de Agendamentos</h3>
            <div id="render-alvo"></div>
        </div>

        <div id="tela-menu" class="hidden">
            <h3>📱 Menu Principal</h3>
            <div class="grid-icones">
                <div class="card">📅 Agenda</div>
                <div class="card">👥 Clientes</div>
                <div class="card">📊 Relatórios</div>
            </div>
        </div>
    </div>

    <script>
        // Mesmo sem dados, as colunas vão aparecer
        const listaAgendamentos = []; 

        function carregarTabela() {
            const alvo = document.getElementById('render-alvo');
            
            let tabelaHTML = `
                <table class="tabela-zion">
                    <thead>
                        <tr>
                            <th>Horário</th>
                            <th>Nome do Cliente</th>
                            <th>Serviço Solicitado</th>
                            <th>Status da Reserva</th>
                        </tr>
                    </thead>
                    <tbody>`;

            if (listaAgendamentos.length === 0) {
                // Se estiver vazio, ele preenche as colunas com a mensagem de vazio
                tabelaHTML += `
                    <tr>
                        <td colspan="4" class="vazio-msg">
                            Atenção: Não existem dados lançados para as colunas acima.
                        </td>
                    </tr>`;
            } else {
                listaAgendamentos.forEach(item => {
                    tabelaHTML += `
                        <tr>
                            <td>${item.hora}</td>
                            <td>${item.cliente}</td>
                            <td>${item.servico}</td>
                            <td>${item.status}</td>
                        </tr>`;
                });
            }

            tabelaHTML += `</tbody></table>`;
            alvo.innerHTML = tabelaHTML;
        }

        function trocarTela() {
            const t1 = document.getElementById('tela-tabela');
            const t2 = document.getElementById('tela-menu');
            t1.classList.toggle('hidden');
            t2.classList.toggle('hidden');
        }

        // Inicia a tabela visualmente
        window.onload = carregarTabela;
    </script>
</body>
</html>
