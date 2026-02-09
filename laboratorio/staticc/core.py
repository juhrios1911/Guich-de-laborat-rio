import datetime

# --- CONFIGURAÇÕES GERAIS ---

# Serviços válidos
SERVICOS_VALIDOS = ["Coleta", "Urina", "Resultado"]

# Tempo máximo de espera (em segundos) para aplicar Aging
# 15 minutos = 900 segundos
TEMPO_LIMITE_AGING = 900


class Paciente:
    def __init__(self, nome, tipo, servico):
        self.nome = nome
        self.tipo = tipo
        self.servico = servico
        self.data_chegada = datetime.datetime.now()
        self.data_atendimento = None

        # Flag de promoção por espera (aging)
        self.promovido_por_espera = False

    def to_dict(self):
        """Converte o paciente para dicionário (frontend / API)"""
        return {
            "nome": self.nome,
            "tipo": self.tipo,
            "servico": self.servico,
            "chegada": self.data_chegada.strftime("%H:%M:%S"),
            "atendimento": self.data_atendimento.strftime("%H:%M:%S")
            if self.data_atendimento else None,
            "espera_segundos": int(
                (datetime.datetime.now() - self.data_chegada).total_seconds()
            ),
            "status_aging": "Promovido (Demora)"
            if self.promovido_por_espera else "Padrão"
        }

    def __repr__(self):
        return f"{self.nome} ({self.tipo}) - {self.servico}"


class SistemaTriagem:
    def __init__(self):
        self.fila = []
        self.ultimo_chamado = None

        # Menor peso = maior prioridade
        self.tabela_pesos = {
            "Emergência": 0,
            "Prioritario": 1,
            "Normal": 3
        }

    # ---------- VALIDAÇÃO ----------
    def _validar_entrada(self, nome, tipo, servico):
        if not nome or not isinstance(nome, str):
            nome = "Paciente Sem Nome"

        if tipo not in self.tabela_pesos:
            tipo = "Normal"

        if servico not in SERVICOS_VALIDOS:
            servico = "Consulta"

        return nome, tipo, servico

    # ---------- ADICIONAR PACIENTE ----------
    def adicionar_paciente(self, nome, tipo, servico):
        nome, tipo, servico = self._validar_entrada(nome, tipo, servico)

        paciente = Paciente(nome, tipo, servico)
        self.fila.append(paciente)

        self._ordenar_fila()
        return paciente

    # ---------- AGING ----------
    def _aplicar_aging(self):
        agora = datetime.datetime.now()

        for paciente in self.fila:
            tempo_espera = (agora - paciente.data_chegada).total_seconds()

            if (
                paciente.tipo == "Normal"
                and tempo_espera > TEMPO_LIMITE_AGING
            ):
                paciente.promovido_por_espera = True

    # ---------- ORDENAÇÃO ----------
    def _ordenar_fila(self):
        self._aplicar_aging()

        def criterio(paciente):
            peso = self.tabela_pesos.get(paciente.tipo, 3)

            # Se ganhou prioridade por demora, sobe na fila
            if paciente.promovido_por_espera:
                peso = 0.5  # Entre Emergência (0) e Prioritario (1)

            return (peso, paciente.data_chegada)

        self.fila.sort(key=criterio)

    # ---------- CHAMAR PRÓXIMO ----------
    def chamar_proximo(self):
        if not self.fila:
            return None

        self._ordenar_fila()

        paciente = self.fila.pop(0)
        paciente.data_atendimento = datetime.datetime.now()
        self.ultimo_chamado = paciente

        return paciente

    # ---------- VISUALIZAÇÃO ----------
    def listar_fila(self):
        return [p.to_dict() for p in self.fila]


# ---------- SIMULAÇÃO ----------
if __name__ == "__main__":
    sistema = SistemaTriagem()

    sistema.adicionar_paciente("Ana", "Normal", "Consulta")
    sistema.adicionar_paciente("Carlos", "Prioritario", "Raio-X")
    sistema.adicionar_paciente("João", "Normal", "Vacina")

    print("📋 FILA INICIAL:")
    for p in sistema.fila:
        print(p)

    print("\n➡️ CHAMANDO PACIENTES:\n")
    while sistema.fila:
        proximo = sistema.chamar_proximo()
        print(f"Chamado: {proximo.nome} | Tipo: {proximo.tipo} | Serviço: {proximo.servico}")

      