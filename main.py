import asyncio
import os
from datetime import datetime, timedelta

import yagmail
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM  # Nova classe atualizada
from tavily import TavilyClient

# === CARREGA VARIÁVEIS DO .env ===
load_dotenv()
EMAIL = os.getenv("EMAIL")
SENHA = os.getenv("SENHA")

# Verifica se credenciais estão carregadas
if not EMAIL or not SENHA:
    raise ValueError("Credenciais de e-mail não encontradas no .env")

# === CONFIGURAÇÃO DO TAVILY ===
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # também no .env
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

# === MODELO LOCAL OLLAMA ===
llama_local = OllamaLLM(model="gemma3", temperature=0.2)


# === FUNÇÃO PARA GERAR O RELATÓRIO DE NOTÍCIAS ===
def gerar_relatorio_noticias():
    # Data de referência: notícias do dia anterior
    data_referencia = (datetime.now() - timedelta(days=0)).strftime("%Y-%m-%d")

    topicos = [
        "principais notícias sobre Inteligência Artificial",
        "notícias sobre tecnologia",
    ]
    contexto_completo = """

            1 - https://go.dev/blog/
            2 - https://dev.to/t/news
          
            """

    for topico in topicos:
        resultado = tavily_client.search(topico, search_depth="basic", search_lang="pt")
        contexto_topico = f"\n## {topico.upper()} ##\n"
        for artigo in resultado["results"][:3]:
            titulo = artigo.get("title", "Sem título")
            snippet = artigo.get("snippet", "Sem conteúdo")
            url = artigo.get("url", "")
            contexto_topico += f"- {titulo} ({url})\n{snippet}\n\n"
        contexto_completo += contexto_topico

    # Prompt personalizado com a data do dia anterior
    prompt = f"""
Você é um agente jornalista.
- Gere um resumo diário de notícias. A data de referência é {data_referencia}.
- Use apenas as seguintes fontes para obter informações precisas sobre cada tópico e escreva um pequeno artigo sobre ele:{contexto_completo}.
- comente o que você acha mais relevante sobre cada notícia.
- copie o link da notícia e cole no final do artigo.
- Use a data de referência para cada notícia.
"""

    formatted_prompt = prompt.format(context=contexto_completo, date=data_referencia)
    resposta = llama_local.invoke(formatted_prompt)
    return resposta, data_referencia


# === GERA FORMATO PARA LINKEDIN ===
def gerar_formato_linkedin(conteudo: str, data_referencia: str) -> str:
    """Formata o conteúdo para ser mais adequado ao LinkedIn"""

    # Prompt para reformatar para LinkedIn
    prompt_linkedin = f"""
Reformate o seguinte relatório de notícias para ser postado no LinkedIn de forma mais atrativa e profissional:

{conteudo}

INSTRUÇÕES:
- Use emojis relevantes para tecnologia e IA
- Mantenha um tom profissional mas engajador
- Divida em seções claras com bullets
- Adicione hashtags relevantes no final (#IA #Tecnologia #Inovacao #TechNews)
- Limite a 1300 caracteres (limite do LinkedIn)
- Mantenha os links das fontes
- Use formato que incentive engajamento
"""

    resposta_linkedin = llama_local.invoke(prompt_linkedin)

    # Salva também a versão LinkedIn
    nome_arquivo_linkedin = f"linkedin_post_{data_referencia}.txt"
    with open(nome_arquivo_linkedin, "w", encoding="utf-8") as f:
        f.write(resposta_linkedin)

    print(f"\n🎯 POST PARA LINKEDIN GERADO:")
    print("=" * 50)
    print(resposta_linkedin)
    print("=" * 50)
    print(f"📁 Salvo em: {nome_arquivo_linkedin}")

    return resposta_linkedin


# === SALVA O RELATÓRIO EM ARQUIVO ===
def salvar_relatorio(conteudo: str, data_referencia: str) -> str:
    nome_arquivo = f"relatorio_noticias_{data_referencia}.md"
    with open(nome_arquivo, "w", encoding="utf-8") as f:  # Definir encoding UTF-8
        f.write(conteudo)
    print(f"Relatório salvo em {nome_arquivo}")
    return nome_arquivo


# === ENVIA O RELATÓRIO POR E-MAIL ===
async def enviar_email(conteudo: str, caminho_arquivo: str, data_referencia: str):
    destinatario = "coimbrawebs@gmail.com"
    assunto = f"Relatório de Notícias - {data_referencia}"

    try:
        yag = yagmail.SMTP(EMAIL, SENHA)
        await asyncio.to_thread(
            yag.send,
            to=destinatario,
            subject=assunto,
            contents=f"Segue o relatório de notícias do dia {data_referencia}:\n\n{conteudo}",
            attachments=caminho_arquivo,
        )
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar e-mail: {e}")


# === FUNÇÃO PRINCIPAL ===
async def main():
    try:
        relatorio, data_referencia = gerar_relatorio_noticias()
        print("\n=== RELATÓRIO ===\n", relatorio)

        arquivo = salvar_relatorio(relatorio, data_referencia)

        # Gera versão para LinkedIn
        gerar_formato_linkedin(relatorio, data_referencia)

        # Email comentado por problemas de autenticação
        await enviar_email(relatorio, arquivo, data_referencia)

        print(f"\n✅ Processo concluído!")
        print(f"📱 Versão LinkedIn: linkedin_post_{data_referencia}.txt")
        print(
            f"💡 Copie o conteúdo do arquivo LinkedIn e cole diretamente no LinkedIn!"
        )

    except Exception as e:
        print(f"Ocorreu um erro: {e}")


if __name__ == "__main__":
    asyncio.run(main())
