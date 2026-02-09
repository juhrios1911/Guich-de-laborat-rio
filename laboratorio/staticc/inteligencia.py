from google import genai  # Importação correta para a versão nova
import os
import json

class AnalisadorIA:
    def __init__(self):
        # Buscando a chave de API
        api_key = os.getenv("GEMINI_API_KEY", "AIzaSyBxCsQW7d-NcaMzwFjnDP-OS_tJfDqBlNU")
        
        # NA VERSÃO NOVA: Usamos genai.Client em vez de configure
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-1.5-flash'

    def gerar_parecer(self, metricas):
        prompt = f"""
        Você é um Diretor de Operações Hospitalares. Analise os dados de hoje:
        - Média de Espera: {metricas.get('media_espera')} min
        - Horário de Pico: {metricas.get('hora_pico')}
        - Total de Atendimentos: {metricas.get('total')}

        Retorne um JSON estritamente neste formato:
        {{
            "status": "Classificação (Estável/Alerta/Crítico) + uma justificativa técnica curta",
            "tempo_estimado": "{metricas.get('media_espera')} minutos",
            "fluxo": "Análise do volume vs. capacidade instalada",
            "sugestao": "Plano de ação imediato para o gargalo das {metricas.get('hora_pico')}"
        }}
        Não use markdown, retorne apenas o objeto JSON puro.
        """

        try:
            # NA VERSÃO NOVA: A chamada mudou para models.generate_content
            response = self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config={
                    'response_mime_type': 'application/json'
                }
            )
            
            # Para pegar o texto na versão nova:
            return json.loads(response.text)

        except Exception as e:
            print(f"Erro na IA: {e}")
            return {
                "status": "Indisponível - Monitoramento Manual Requerido",
                "tempo_estimado": f"{metricas.get('media_espera')} min",
                "fluxo": "Erro na conexão com o motor de análise.",
                "sugestao": "Verifique a escala de plantão presencialmente."
            }