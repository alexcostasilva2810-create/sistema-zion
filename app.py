<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Zion v9.1 - Correção de Erro</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f4; margin: 0; }
        .header { background: #000; color: #fff; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; }
        
        /* LOGO CLICÁVEL */
        .logo-click { cursor: pointer; border: 1px solid #555; padding: 5px; transition: 0.3s; }
        .logo-click:hover { background: #333; }

        /* BOTÃO AUXILIAR */
        .btn-nav { background: #2563eb; color: white; border: none; padding: 10px 15px; border-radius: 4px; cursor: pointer; font-weight: bold; }

        .content { padding: 20px; }
        
        /* TABELA COM COLUNAS FORTES */
        .tabela-fixa { width: 100%; border-collapse: collapse; background: white; margin-top: 15px; }
        .tabela-fixa th { background: #ddd; color: #000; border: 2px solid #000; padding: 12px; text-align: left; }
        .tabela-fixa td { border: 2px solid #000; padding: 10px; color: #333; }
        
        .hidden { display: none; }

        /* MENU DE ÍCONES */
        .grid-icones { display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 15px; }
        .card-sistema { background: #fff; border: 2px solid #2563eb; padding: 30px; text-align: center; border-radius: 8px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>

    <header class="header">
        <div class="logo-click" id="trigger-logo">
            <img src="https://via.placeholder.com/120x40?text=ZION+LOGO" alt="Logo">
        </div>

        <button class="btn-nav" id="btn-operacional">☰ ÍCONES OPERACIONAIS</button>
    </header>

    <div class="content">
        
        <div id="tela-agendamentos">
            <h2>📋 Grade de Agendamentos</h2>
            <table class="tabela-fixa">
                <thead>
                    <tr>
                        <th>HORA</th>
                        <th>CLIENTE</th>
                        <th>SERVIÇO</th>
                        <th>STATUS</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td colspan="4" style="text-align: center; padding: 30px;">As colunas estão ativas. Nenhum dado lançado.</td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div id="tela-menu" class="hidden">
            <h2>⚙️ Operacional</h2>
            <div class="grid-icones">
                <div class="card-sistema">📅 AGENDA</div>
                <div class="card-sistema">👥 CLIENTES</div>
                <div class="card-sistema">💰 CAIXA</div>
            </div>
            <br>
            <button id="btn-voltar" style="cursor:pointer; padding: 8px;">← Voltar para Grade</button>
        </div>

    </div>

    <script>
        // ESTA É A FORMA MAIS SEGURA DE EVITAR ERRO DE LINHA
        document.addEventListener('DOMContentLoaded', function() {
            
            const telaTabela = document.getElementById('tela-agendamentos');
            const telaMenu = document.getElementById('tela-menu');
            
            // Função para alternar
            function alternar() {
                if (telaMenu.classList.contains('hidden')) {
                    telaMenu.classList.remove('hidden');
                    telaTabela.classList.add('hidden');
                } else {
                    telaMenu.classList.add('hidden');
                    telaTabela.classList.remove('hidden');
                }
            }

            // Atribuindo os eventos de clique de forma segura
            document.getElementById('trigger-logo').onclick = alternar;
            document.getElementById('btn-operacional').onclick = alternar;
            document.getElementById('btn-voltar').onclick = alternar;

            console.log("Zion v9.1: Sistema carregado sem erros de linha.");
        });
    </script>
</body>
</html>
