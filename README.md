# 🎶 Gerador de Slides de Louvores

Este projeto tem como objetivo automatizar a criação de slides de louvores a partir de um banco de dados estruturado com informações de hinos e hinários cristãos.

## 📌 Visão Geral

A aplicação foi desenvolvida para facilitar a geração de apresentações de hinos utilizadas em cultos, eventos e reuniões. Em vez de criar slides manualmente, o sistema lê os dados armazenados em um banco e gera automaticamente os slides com base em um template configurável.

Isso permite:

* Padronização visual dos slides
* Economia de tempo
* Facilidade para atualizar apresentações quando o template muda

## 🗂️ Estrutura dos Dados

O sistema utiliza um banco de dados que armazena informações sobre:

### 📚 Coletâneas / Hinários

* Cantor Cristão
* Hinário para o Culto Cristão
* Voz de Melodia
* Hinos de Louvor
* Corinhos diversos

### 🎵 Hinos

Cada registro de hino contém:

* **Título**
* **Número** na coletânea (opcional)
* **Autor**
* **Letra do hino** (armazenada em formato `.txt`)

## ⚙️ Funcionamento da Aplicação

A aplicação segue o seguinte fluxo:

1. **Leitura dos dados**

   * Consulta o banco de dados
   * Recupera os dados do hino selecionado

2. **Processamento da letra**

   * Separa automaticamente:
     * Estrofes
     * Refrões
   * Utiliza regras baseadas em formatação (linhas em branco, indentação, etc.)

3. **Geração dos slides**

   * Aplica um **template configurável**
   * Distribui o conteúdo do hino em múltiplos slides
   * Gera uma apresentação pronta para uso

## 🎨 Templates

Os slides são gerados com base em um template.

### Vantagens:

* Permite alteração rápida do layout (cores, fontes, posicionamento)
* Não exige recriação manual dos slides
* Basta trocar o template e re-criar os slides

## 🚀 Benefícios

* Automatização completa do processo
* Reutilização de dados estruturados
* Facilidade de manutenção e evolução
* Redução de erros manuais
* Consistência visual entre apresentações

## 🧠 Lógica de Separação do Hino

A aplicação possui uma lógica específica para interpretar a letra dos hinos:

* **Estrofes**: iniciam no começo da linha
* **Refrões**: possuem indentação (espaços ou tabulação)
* **Separação**: feita por linhas em branco

Essa abordagem permite transformar textos simples em slides organizados automaticamente.

## 📦 Possíveis Extensões

* Interface gráfica para seleção de hinos
* Exportação para diferentes formatos (PowerPoint, PDF, etc.)
* Integração com APIs ou sistemas de projeção
* Edição visual de templates

## 🛠️ Tecnologias Utilizadas

* Python
* Banco de dados relacional
* Processamento de texto
* Geração de apresentações

## 📄 Licença

Este projeto está licenciado sob a **MIT License**.

Você pode usar, modificar, distribuir e até vender este software livremente, desde que mantenha a devida atribuição ao autor original.

Consulte o arquivo `LICENSE` para mais detalhes.

---

💡 *Dica: mantenha o banco de dados atualizado para garantir que novos hinos estejam sempre disponíveis para geração automática de slides.*



<!-- $env:PYTHONPATH = "$env:PYTHONPATH;C:\Users\N2SE\OneDrive - TRANSPETRO\Documentos\Projetos\sap_automation\src" -->