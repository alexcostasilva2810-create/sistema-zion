<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Zion v8.5 - Tabela com Grade e Botão Auxiliar</title>
    <style>
        body { font-family: 'Segoe UI', Arial, sans-serif; background-color: #f4f7f9; margin: 0; }

        /* HEADER */
        .header { 
            background: #1a1a1a; 
            padding: 15px 25px; 
            display: flex; 
            justify-content: space-between; 
            align-items: center; 
            color: white; 
        }

        /* LOGO CLICÁVEL */
        .logo-area { cursor: pointer; display: flex; align-items: center; }
        .logo-img { height: 45px; border: 1px solid #444; border-radius: 4px; }

        /* BOTÃO AUXILIAR */
        .btn-auxiliar {
            background: #2563eb;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 6px;
            cursor: pointer;
            font-weight: bold;
            transition: 0.3s;
        }
        .btn-auxiliar:hover { background: #1d4ed8; transform: scale(1.05); }

        .container { padding: 30px; }

        /* TABELA COM COLUNAS BEM VISÍVEIS */
        .tabela-container { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }
        
        .tabela-zion { 
            width: 100%; 
            border-collapse: collapse; /* Crucial para as bordas aparecerem juntas */
        }

        .tabela-zion th { 
            background: #e2e8f0; 
            color: #334155; 
            padding: 15px; 
            text-align: left;
            border: 2px solid #cbd5e1; /* Borda da Coluna */
        }

        .tabela-zion td { 
            padding: 12px; 
            border: 2px solid #cbd5e1; /* Borda da Linha/Coluna */
            color: #1e293b;
        }

        .aviso-vazio { 
            text-align: center; 
            color: #94a3b8; 
            padding: 40px !important; 
            font-style: italic;
        }

        /* TELAS */
        .hidden { display: none; }
        .grid-icones { 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); 
            gap: 20px; 
        }
        .card-operacional {
            background: white;
            border: 2px solid #2563eb;
            padding: 30px;
            text-align: center;
            border-radius: 12px;
            font-weight: bold;
            cursor: pointer;
        }
    </style>
</head>
<body>

    <header class="header">
        <div class="logo-area" onclick="irParaMenu()">
            <img src="https://via.placeholder.com/130x45?text=ZION+LOGO" alt="Zion" class="logo-img">
        </div>

        <button class="btn-auxiliar" onclick="irParaMenu()">
            ☰ ÍCONES OPERACIONAIS
        </button>
    </header>

    <div class="container">
        
        <div id="tela-tabela">
            <h2 style="margin-top:0;">📋 Agendamentos Cadastrados</h2>
            <div class="tabela-container">
                <table class="tabela-zion">
                    <thead>
                        <tr>
                            <th>HORA</th>
                            <th>CLIENTE</th>
                            <th>PROCEDIMENTO</th>
                            <th>PROFISSIONAL</th>
                            <th>STATUS</th>
                        </tr>
                    </thead>
                    <tbody id="corpo-tabela">
                        <tr>
                            <td colspan="5" class="aviso-vazio">Nenhum registro encontrado. As colunas acima estão prontas para novos dados.</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <div id="tela-icones" class="hidden">
            <h2 style="margin-top:0;">⚙️ Operacional</h2>
            <div class="grid-icones">
                <div class="card-operacional">📅 AGENDA</div>
                <div class="card-operacional">👥 CLIENTES</div>
                <div class="card-operacional">📦 ESTOQUE</div>
                <div class="card-operacional">💰 CAIXA</div>
            </div>
            <button onclick="irParaTabela()" style="margin-top: 20px; cursor: pointer;">← Voltar para Tabela</button>
        </div>

    </div>

    <script>
        function irParaMenu() {
            document.getElementById('tela-tabela').classList.add('hidden');
            document.getElementById('tela-icones').classList.remove('hidden');
        }

        function irParaTabela() {
            document.getElementById('tela-icones').classList.add('hidden');
            document.getElementById('tela-tabela').classList.remove('hidden');
        }

        // Simulação de segurança para garantir que a tabela seja desenhada
        window.onload = function() {
            console.log("Zion v8.5 Ativa. Colunas renderizadas via CSS Fixo.");
        };
    </script>

</body>
</html>
