# TerlineT - Assistente Virtual

Um chatbot/assistente virtual desenvolvido em Python com Kivy.

## Versões Disponíveis

### 1. Versão Simples (main_simple.py)

- Interface básica de chat
- Respostas baseadas em palavras-chave
- Funciona apenas com Kivy
- Ideal para testar a interface

### 2. Versão Completa (main.py)

- Suporte a modelos GGUF (llama-cpp-python)
- Reconhecimento e síntese de voz
- Funcionalidades avançadas de IA
- Requer mais dependências

## Instalação

### Requisitos Mínimos

```bash
pip install kivy
```

### Para Versão Completa

```bash
pip install -r requirements.txt
```

## Como Executar

### Versão Simples (Recomendada para testes)

```bash
python main_simple.py
```

### Versão Completa

```bash
python main.py
```

## Dependências

### Básicas (Versão Simples)

- kivy==2.2.0

### Completas (Versão Avançada)

- kivy==2.2.0
- llama-cpp-python==0.2.77
- gtts==2.4.0
- pygame==2.5.2
- SpeechRecognition==3.10.0
- pyaudio==0.2.13
- plyer==2.1.0

## Estrutura do Projeto

```
TerlineT_Kivy/
├── main.py              # Versão completa com IA
├── main_simple.py       # Versão simples
├── logger.py            # Módulo de logging
├── requirements.txt     # Dependências
├── README.md           # Este arquivo
└── modelo/             # Pasta para modelos GGUF (versão completa)
```

## Funcionalidades

### Versão Simples

- [x] Interface de chat responsiva
- [x] Respostas baseadas em palavras-chave
- [x] Tema escuro moderno
- [x] Timestamp nas mensagens

### Versão Completa

- [x] Modelo de IA GGUF
- [x] Reconhecimento de voz
- [x] Síntese de voz (TTS)
- [x] Contexto de conversação
- [x] Ativação por voz ("TerlineT")
- [x] Suporte Android (experimental)

## Troubleshooting

### Erro de importação do Kivy

```bash
pip install --upgrade kivy[base]
```

### Problemas com pyaudio no Windows

```bash
pip install pipwin
pipwin install pyaudio
```

### Problemas com llama-cpp-python

```bash
pip install llama-cpp-python --force-reinstall --no-cache-dir
```

## Desenvolvimento

Para contribuir com o projeto:

1. Clone o repositório
2. Instale as dependências: `pip install -r requirements.txt`
3. Execute a versão simples para testar: `python main_simple.py`
4. Faça suas modificações
5. Teste em ambas as versões

## Licença

Este projeto é de código aberto. Use livremente para fins educacionais e pessoais.