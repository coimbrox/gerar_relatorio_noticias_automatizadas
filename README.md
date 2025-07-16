# 📰 Gerador Automático de Relatórios de Notícias

Este projeto gera automaticamente relatórios diários de notícias sobre Inteligência Artificial e Tecnologia, utilizando IA local (Ollama) e busca inteligente (Tavily). O relatório é enviado por email e pode ser automatizado para postagem no LinkedIn.

## 🚀 Funcionalidades

- **Busca inteligente de notícias** usando Tavily API
- **Geração de relatórios** com IA local (Llama 3.1 via Ollama)
- **Envio automático por email** com anexo em Markdown
- **Integração com n8n** para automação no LinkedIn

## 📋 Pré-requisitos

### 1. Ollama (Obrigatório)
Você precisa instalar o Ollama localmente:

1. Baixe e instale o [Ollama](https://ollama.ai/)
2. Após a instalação, baixe o modelo Llama 3.1:
```bash
ollama pull llama3.1:8b
```
3. Verifique se o modelo está funcionando:
```bash
ollama run llama3.1:8b
```

### 2. Python 3.8+
Certifique-se de ter Python instalado.

## ⚙️ Configuração

### 1. Clone o repositório
```bash
git clone <seu-repositorio>
cd AttPostsLinkedin
```

### 2. Instale as dependências
```bash
pip install asyncio yagmail python-dotenv tavily-python langchain-ollama
```

### 3. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto:

```env
# Credenciais de email
EMAIL=seu-email@gmail.com
SENHA=sua-senha-de-app

# API Key do Tavily
TAVILY_API_KEY=sua-chave-tavily
```

**⚠️ Importante:**
- Para Gmail, use uma [senha de app](https://support.google.com/accounts/answer/185833)
- Obtenha sua chave da Tavily em [tavily.com](https://tavily.com)

### 4. Configure o destinatário
No arquivo [`main.py`](main.py), altere a linha 75:
```python
destinatario = "seuemail@email.com"  # Substitua pelo email desejado
```

## 🔧 Como usar

### Execução manual
```bash
python main.py
```

### Arquivos gerados
- `relatorio_noticias_YYYY-MM-DD.md` - Relatório em Markdown
- Email enviado com o relatório anexo

## 🤖 Automação com n8n

Para automatizar a postagem no LinkedIn:

1. **Configure um workflow no n8n** com os seguintes nós:
   - **Trigger por schedule** (execução diária)
   - **Email trigger** para ler o relatório do email
   - **LinkedIn node** para postar o conteúdo

2. **Fluxo sugerido:**
   ```
   Schedule → Email Trigger → Text Processing → LinkedIn Post
   ```

3. **Configuração do LinkedIn:**
   - Use o nó oficial do LinkedIn no n8n
   - Configure as credenciais da API do LinkedIn
   - Processe o texto do relatório para formato de post

## 📁 Estrutura do projeto

```
.
├── .env                 # Variáveis de ambiente (não versionado)
├── .gitignore          # Arquivos ignorados pelo Git
├── main.py             # Script principal
└── README.md           # Este arquivo
```

## 🛠️ Personalização

### Modificar tópicos de busca
Edite a lista `topicos` na função [`gerar_relatorio_noticias`](main.py):
```python
topicos = [
    "principais notícias sobre Inteligência Artificial",
    "notícias sobre tecnologia",
    "suas-categorias-personalizadas"
]
```

### Alterar modelo de IA
Modifique o modelo Ollama na linha 24:
```python
llama_local = OllamaLLM(model="llama3.1:8b", temperature=0.2)
```

## 📄 Licença

Este projeto está sob a licença MIT.

## 🤝 Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests.

---

**💡 Dica:** Para melhor automação, configure um cron job ou use o Windows Task Scheduler para executar o script diariamente.