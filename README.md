# 🌐 Assistente Diversa — Educação Inclusiva

Este é o protótipo funcional para o Trabalho de Conclusão de Curso (TCC) da **Equipe Hélice (SoulCode / Accenture)**. 

O projeto consiste em um assistente virtual (Chatbot) focado em **Educação Inclusiva**, utilizando uma base de conhecimento curada a partir de artigos do Portal Diversa. O assistente realiza buscas por relevância usando **TF-IDF (Cosine Similarity)** e gera respostas contextualizadas via API da **Groq** usando o modelo **Llama 3.1** (ou em modo demonstração local sem a chave de API).

---

## 📂 Estrutura do Projeto

* `app.py`: Script Python principal para rodar o chatbot localmente de forma simples.
* `prototipo_funcional_assistente_diversa.ipynb`: Jupyter Notebook contendo a análise, limpeza de dados e prototipagem da interface (ideal para Google Colab).
* `artigos.csv`: A base de dados em formato tabular contendo títulos, links e textos dos artigos do Portal Diversa.
* `requirements.txt`: Lista de dependências e bibliotecas Python necessárias para execução do projeto.
* `.env`: Arquivo de variáveis de ambiente para armazenamento seguro de chaves de API.
* `imagens_do_tcc/`: Diretório que contém os arquivos SVG utilizados na estilização da interface visual do chat (borda de cordão do autismo/TEA e ícone da Equipe Hélice).

---

## 🛠️ Pré-requisitos e Instalação

Siga os passos abaixo para configurar o ambiente e rodar o projeto em sua máquina local:

### 1. Clonar ou Acessar a Pasta do Projeto
Certifique-se de estar no terminal do seu sistema dentro da pasta raiz do projeto:
```bash
cd "~/tcc"
```

### 2. Criar um Ambiente Virtual (Recomendado)
Para evitar conflitos com outros pacotes do seu Python global, crie e ative um ambiente virtual:

* No Linux/macOS:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```
* No Windows:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```

### 3. Instalar as Dependências
Com o ambiente virtual ativado, instale as bibliotecas requeridas executando:
```bash
pip install -r requirements.txt
```

---

## 🔑 Configuração da Chave de API (.env)

O assistente foi desenhado para rodar em dois modos:
1. **Modo Groq/Llama 3.1 (Geração Completa por IA)**: Requer uma chave de API gratuita da Groq.
2. **Modo Demonstração (Simulado)**: Caso nenhuma chave seja configurada, o assistente responderá apenas recuperando os trechos literais mais relevantes da base.

Para configurar a chave da Groq:
1. Obtenha uma chave gratuita no painel da [Groq Console](https://console.groq.com/).
2. Abra o arquivo `.env` localizado na raiz do projeto.
3. Insira a sua chave após o sinal de igual:
   ```ini
   GROQ_KEY=gsk_suachaveaqui...
   ```
4. Salve e feche o arquivo.

---

## 🚀 Como Executar o Projeto

### Executar via Jupyter Notebook / Google Colab
Caso prefira inspecionar o código por etapas, testar a vetorização ou exportar DataFrames:
1. Abra o Jupyter Lab ou Notebook na pasta do projeto:
   ```bash
   jupyter notebook
   ```
2. Abra o arquivo `prototipo_funcional_assistente_diversa.ipynb`.
3. Execute as células sequencialmente (`Shift + Enter`).
4. *(Opcional)* Se estiver executando no **Google Colab**, lembre-se de fazer o upload da pasta `imagens_do_tcc` e do arquivo `artigos.csv` para manter a estilização visual completa.

---

## 👨‍💻 Equipe Hélice
* Desenvolvido para fins de Trabalho de Conclusão de Curso (TCC) - **SoulCode Academy / Accenture**.
