# 🤖 AI Chatbot

> Chatbot com inteligência artificial usando a API do Claude (Anthropic), com interface web desenvolvida em Python puro.

![Python](https://img.shields.io/badge/Python-3.6+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![HTML](https://img.shields.io/badge/HTML5-Interface-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![Claude](https://img.shields.io/badge/Claude-API-D97706?style=for-the-badge&logo=anthropic&logoColor=white)
![License](https://img.shields.io/badge/License-REBELO49-22c55e?style=for-the-badge&logo=github&logoColor=white)
![Status](https://img.shields.io/badge/Status-Concluído-7c6af7?style=for-the-badge)

---

## 🚀 Funcionalidades

- 🤖 **IA real** — respostas geradas pelo Claude (Anthropic)
- 💬 **Histórico de conversa** — o bot lembra-se do contexto
- ✨ **Formatação** — suporte a markdown, código e negrito
- 💡 **Sugestões rápidas** — botões para começar a conversa
- 🗑️ **Limpar conversa** — reinicia o chat quando quiseres
- 🎨 **Interface dark mode** responsiva e animada

---

## 🛠️ Tecnologias

| Tecnologia | Utilização |
|---|---|
| Python 3 | Servidor HTTP e chamadas à API |
| HTML + CSS + JS | Interface web (dark mode) |
| Claude API (Anthropic) | Motor de inteligência artificial |

---

## ⚡ Como executar

### Pré-requisitos
- Python 3.6 ou superior
- Chave de API da Anthropic (gratuita)

### 1. Obtém a tua API key
1. Vai a [console.anthropic.com](https://console.anthropic.com)
2. Cria uma conta gratuita
3. Em **API Keys**, clica em **Create Key**
4. Copia a chave gerada

### 2. Configura o projeto
Abre o ficheiro `chatbot.py` e substitui:
```python
API_KEY = "COLOCA_AQUI_A_TUA_API_KEY"
```
pela tua chave real.

### 3. Corre a app
```bash
# 1. Clona o repositório
git clone https://github.com/Rebelo49/ai-chatbot.git
cd ai-chatbot

# 2. Corre a app
python3 chatbot.py
```

O browser abre automaticamente em `http://localhost:8768` 🎉

Para parar: **Ctrl + C**

---

## 🗂️ Estrutura do projeto

```
ai-chatbot/
├── chatbot.py   # Servidor HTTP + interface web + integração com API
└── README.md
```

---

## 👤 Autor

**Pedro Rebelo**
- GitHub: [@Rebelo49](https://github.com/Rebelo49)

---

## 📄 Licença

Pedro Rebelo © 2026 