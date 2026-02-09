from flask import Flask, render_template, request, redirect, url_for
from core import SistemaTriagem 
from dados import GerenciadorDados 
from inteligencia import AnalisadorIA 
import random 

app = Flask(__name__)

# --- Instâncias globais ---
sistema = SistemaTriagem()
db = GerenciadorDados()
ia_engine = AnalisadorIA() 

# 1. PÁGINA INICIAL (FILA)
@app.route('/') 
def index():
    return render_template('index.html', fila=sistema.listar_fila())

# 2. CADASTRAR PACIENTE NA TRIAGEM
@app.route('/cadastrar', methods=['POST']) 
def cadastrar():
    nome = request.form.get('nome')
    servico = request.form.get('servico')
    tipo = request.form.get('tipo')
    subtipo = request.form.get('subtipo')
    
    nome_exibicao = f"{nome}"
    if subtipo: nome_exibicao += f" ({subtipo})"

    sistema.adicionar_paciente(nome_exibicao, tipo, servico)
    return redirect(url_for('index'))

# 3. ATENDER (CHAMAR PRÓXIMO E IR PARA FORMULÁRIO)
@app.route('/atender/<int:indice>')
def atender(indice):
    # IMPORTANTE: Esta linha tira o paciente da fila principal
    paciente_atendido = sistema.chamar_proximo() 
    
    if paciente_atendido:
        db.salvar_no_historico(paciente_atendido)
        # Vai para o formulário clínico
        return redirect(url_for('preencher_ficha', cliente_nome=paciente_atendido.nome))
    
    return redirect(url_for('index'))
# 4. FORMULÁRIO DE DADOS CLÍNICOS (CPF, CONVÊNIO, ETC)
@app.route('/preencher_ficha/<string:cliente_nome>')
def preencher_ficha(cliente_nome):
    paciente_dados = next((p for p in db.historico if p['cliente'] == cliente_nome), None)
    
    if not paciente_dados:
        return "Ficha não encontrada no histórico.", 404
    
    return render_template('preencher_ficha.html', paciente=paciente_dados)

# 5. GERAR FICHA FINAL PARA IMPRESSÃO
@app.route('/gerar_ficha', methods=['POST'])
def gerar_ficha():
    # Verifica se marcou convênio sim ou não
    tem_convenio = request.form.get('tem_convenio')
    convenio_final = request.form.get('convenio') if tem_convenio == 'sim' else "Particular / Sem Convênio"
    carteirinha_final = request.form.get('carteirinha') if tem_convenio == 'sim' else "N/A"

    dados_paciente = {
        "nome": request.form.get('nome_completo'),
        "nascimento": request.form.get('nascimento'),
        "cpf": request.form.get('cpf'),
        "convenio": convenio_final,
        "carteirinha": carteirinha_final,
        "tipo_coleta": request.form.get('tipo_exame'),
        "exames": request.form.getlist('detalhes_exame'),
        "senha": f"LB-{random.randint(100, 999)}"
    }
    return render_template('ficha.html', p=dados_paciente)

# 6. RELATÓRIO / DASHBOARD
@app.route('/relatorio')
def relatorio():
    resumo_metricas = db.calcular_metricas()
    analise_da_ia = ia_engine.gerar_parecer(resumo_metricas)
    
    return render_template('dashboard.html', 
                           ia=analise_da_ia, 
                           metricas=resumo_metricas, 
                           atendimentos=db.historico[::-1])

if __name__ == '__main__':
    app.run(debug=True)