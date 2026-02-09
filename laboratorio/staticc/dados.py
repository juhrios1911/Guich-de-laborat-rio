import random
from datetime import datetime, timedelta

class GerenciadorDados:
    def __init__(self):
        # Inicia com os 50 dados falsos da Pessoa 4
        self.historico = self.gerar_mock_data()

    def gerar_mock_data(self):
        nomes = ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo", "Fernanda", "Gabriel", "Helena"]
        sobrenomes = ["Silva", "Santos", "Oliveira", "Souza", "Pereira"]
        servicos = ["Coleta", "Urina", "Resultado"]
        tipos = ["Normal", "Prioritario"]
        dados_ficticios = []
        agora = datetime.now()

        for i in range(50):
            nome_completo = f"{random.choice(nomes)} {random.choice(sobrenomes)}"
            atraso = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
            horario_chegada = agora - atraso
            tipo = random.choice(tipos)
            espera = random.randint(5, 15) if tipo == "Prioritario" else random.randint(15, 45)
            
            atendimento = {
                "id": i + 1,
                "cliente": nome_completo,
                "tipo": tipo,
                "servico": random.choice(servicos),
                "chegada": horario_chegada.strftime("%H:%M"),
                "espera_min": espera,
                "hora_pico": horario_chegada.hour
            }
            dados_ficticios.append(atendimento)
        return dados_ficticios

    def salvar_no_historico(self, paciente_obj): #---------- REVER----------------------------------
        """Converte o objeto Paciente (da Pessoa 3) para o formato de dicionário do Histórico"""
        agora = datetime.now()
        # Calcula espera real baseada na chegada
        espera_real = int((agora - paciente_obj.data_chegada).total_seconds() / 60)
        
        novo = {
            "id": len(self.historico) + 1,
            "cliente": paciente_obj.nome,
            "tipo": paciente_obj.tipo,
            "servico": paciente_obj.servico,
            "chegada": paciente_obj.data_chegada.strftime("%H:%M"),
            "espera_min": espera_real,
            "hora_pico": agora.hour
        }
        self.historico.append(novo)

    def calcular_metricas(self):
        if not self.historico: return {"media_espera": 0, "hora_pico": "00:00", "total": 0}
        media = sum(d['espera_min'] for d in self.historico) / len(self.historico)
        horas = [d['hora_pico'] for d in self.historico]
        hora_pico = max(set(horas), key=horas.count)
        return {
            "media_espera": round(media, 1),
            "hora_pico": f"{hora_pico}:00",
            "total": len(self.historico)
        }