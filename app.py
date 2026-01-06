<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Zion v8.6 - Estabilidade Total</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f0f2f5; margin: 0; }
        
        /* HEADER */
        .navbar { 
            background: #111; 
            padding: 10px 20px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            color: white;
            border-bottom: 3px solid #2563eb;
        }

        /* LOGO E BOTÃO */
        .logo-box { cursor: pointer; padding: 5px; border: 1px solid #333; }
        .btn-operacional { 
            background: #2563eb; 
            color: white; 
            border: none; 
            padding: 12px 25px; 
            border-radius: 5px; 
            font-weight: bold; 
            cursor: pointer;
        }

        .container { padding: 25px; }

        /* TABELA COM GRADE FORTE (EXCEL STYLE) */
        .grade-zion { 
            width: 100%; 
            border-collapse: collapse; 
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }

        .grade-zion th { 
            background: #f8fafc; 
            color: #333; 
            padding: 15px; 
            border: 2px solid #000000; /* Linhas Pretas para visualização clara */
            text-align: left;
        }

        .grade-zion td { 
            padding: 12px; 
            border: 1px solid #000000; /* Colunas bem marcadas */
            color: #444;
        }

        /* AUXILIARES */
        .hidden { display: none; }
        .menu-icones { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr)); 
            gap: 20px; 
        }
        .card-icon { 
            background: white; 
            border: 2px solid #2563eb; 
            padding: 25px; 
            text-align: center; 
            border-radius: 8px;
            font-weight: bold;
        }
    </style>
</head>
<body>

    <header class="navbar">
        <div class="logo-box" onclick="irParaMenu()">
            <img src="https://via.placeholder.com/120x40?text=ZION+V8.6" alt="Zion Logo">
        </div>

        <button class="btn-operacional" onclick="irParaMenu()">
            ☰ ACESSAR ÍCONES
        </button>
    </header>

    <div class="container">
        
        <div id="secao-tabela">
            <h2 style="color: #1a1a1a;">📋 Grade de Agendamentos</h2>
            <table class="grade-zion">
                <thead>
                    <tr>
                        <th style="width: 15%;">HORÁRIO</th>
                        <th style="width: 35%;">CLIENTE</th>
                        <th style="width: 30%;">SERVIÇO</th>
                        <th style="width: 20%;">STATUS</th>
                    </tr>
                </thead>
                <tbody id="corpo-dados">
                    <tr>
                        <td colspan="4" style="text-align: center; padding: 50px; color: #666;">
                            Nenhum agendamento para exibição. As colunas estão prontas.
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div id="secao-icones" class="hidden">
            <h2 style="color: #1a1a1a;">⚙️ Ícones Operacionais</h2>
            <div class="menu-icones">
                <div class="card-icon">📅 AGENDA</div>
                <div class="card-icon">👥 CLIENTES</div>
                <div class="card-icon">💰 FINANCEIRO</div>
                <div class="card-icon">📊 RELATÓRIOS</div>
            </div>
            <br>
            <button onclick="irParaTabela()" style="padding: 10px; cursor: pointer;">← Voltar para a Grade</button>
        </div>

    </div>

    <script>
        // Funções de Navegação Simples
        function irParaMenu() {
            document.getElementById('secao-tabela').classList.add('hidden');
            document.getElementById('secao-icones').classList.remove('hidden');
        }

        function irParaTabela() {
            document.getElementById('secao-icones').classList.add('hidden');
            document.getElementById('secao-tabela').classList.remove('hidden');
        }

        // Se houver qualquer erro no carregamento, ele não afetará o HTML acima
        try {
            console.log("Sistema Zion v8.6 operacional.");
        } catch (e) {
            console.error("Erro detectado, mas a interface foi preservada.");
        }
    </script>

</body>
</html>
