---
name: skill-creator-estudos-paulo
description: Como usar o Skill Creator para criar, modificar, melhorar e avaliar skills. Foco na implementação dentro do Antigravity (ambiente gratuito) para arquitetar "Agent Skills" sem escrever código.
---

# Skill Creator - Estudos Paulo

Este documento detalha o uso do **Skill Creator**, uma ferramenta oficial da Anthropic projetada para transformar instruções em linguagem natural em habilidades (skills) prontas para agentes de IA.

**Autor da Metodologia:** Sandeco (Professor e Pesquisador em IA - IFG/UFG).
**Impacto da Ferramenta:** A democratização da criação desse tipo de skill (especialmente para análise jurídica) impactou drasticamente o mercado de empresas SaaS (Software as a Service) nos EUA, pois agora qualquer pessoa pode criar ferramentas robustas de análise documental gratuitamente.

Skill Creator foi criado originalmente para ser usado pelo Claude Code
As instruções completas estão aqui: https://claude.com/plugins/skill-creator
Ele é um dos skills de https://github.com/anthropics/skills/tree/main

Mas o Sandeco ensinou a usar no Antigravity
https://www.youtube.com/watch?v=yPoSJbLxbS8

---

## 1. O que é o Skill Creator?
É um plugin originalmente desenvolvido para o ecossistema Claude (Claude Desktop, Claude Calling, Claude Code) que permite criar, melhorar e avaliar skills. Como o código é aberto no GitHub, ele pode ser importado e utilizado dentro do **Antigravity**, um ambiente de execução totalmente gratuito.

---

## 2. Instalação e Uso no Claude Desktop (Visão Geral)
Embora o foco seja o Antigravity, o vídeo demonstra o processo no Claude para fins de comparação:

* **Instalação:** Copia-se o comando de instalação do Skill Creator e executa-se no Prompt de Comando (CMD) do Windows.
* **Geração:** Pede-se ao Claude (modelo Sonnet 4.6 sugerido no vídeo) para criar a skill. O Claude gera um arquivo `.zip` contendo pastas como `/scripts`, `/references` e `/assets`.
* **Importação:** No Claude, acessa-se `Personalizar > Habilidades > Fazer upload de uma habilidade`. Pode-se subir o arquivo `.zip` ou um arquivo `.skill` (que deve conter o `skill.m`).

---

## 3. O "Prompt Mestre" de Exemplo (Legal Document Explainer)
O professor utiliza um caso de uso real e de alto valor: uma skill para auditoria e análise de documentos jurídicos. O prompt exato utilizado foi:

> "Crie uma skill chamada Legal Document Explainer, que quando o usuário enviar qualquer documento jurídico, contrato, termo de serviço, aluguel, política de privacidade, etc., resume o conteúdo em linguagem simples, destaca cláusulas problemáticas como multas, renovação automática e coleta de dados. Atribui um placar de risco (baixo, médio ou alto) e sugere perguntas críticas que o usuário deveria fazer antes de assinar. Todo o código deve ir em `scripts`. A documentação de referências tem que ser em `references` e os templates e arquivos auxiliares em `assets`. Entregue a skill em um arquivo zip."

---

## 4. Instalação e Execução no Antigravity (Passo a Passo Detalhado)
O Antigravity permite usar toda essa estrutura sem custos.

### Passo A: Baixando as Skills Oficiais
* Crie uma pasta chamada `skills` no seu computador (ex: no disco F:).
* No chat do Antigravity, envie o comando pedindo a instalação e cole o link do GitHub da Anthropic:
    * *Comando:* `Instale essas skills [Link do GitHub da Anthropic]`.
* Confirme as solicitações de segurança do Antigravity para permitir o download.
* O sistema baixará um pacote de skills.

### Passo B: Organização do Ambiente
* Crie uma pasta oculta chamada `.agents`.
* Mova as skills baixadas para dentro de `.agents`.
* Você pode apagar as skills que não for usar, mas é crucial manter a pasta `skill-creator` intacta.

### Passo C: Criando a Nova Skill no Antigravity
* Abra uma nova janela de conversa no Antigravity.
* **Macete de Otimização:** Arraste a pasta `skill-creator` diretamente para o chat. Isso cria uma referência direta, economizando tokens e evitando que a IA faça buscas desnecessárias.
* Cole o "Prompt Mestre" (Legal Document Explainer) e envie.
* **Alinhamento:** O Antigravity fará perguntas de ajuste (ex: "Qual o formato de entrada?", "Quais as métricas de risco?"). Você pode definir critérios ou pedir para a IA definir automaticamente.
* A IA criará a pasta `Legal Document Explainer` e um arquivo `.zip`. O `.zip` pode ser apagado, pois a pasta já está pronta para uso.
* Mova essa nova pasta gerada para o seu diretório raiz de `skills`.

---

## 5. Testando a Skill na Prática
Para validar o funcionamento, o vídeo simula a auditoria de um documento com armadilhas da LGPD.

* **Preparação:** Crie uma pasta chamada `políticas` e coloque o documento a ser analisado lá dentro (ex: `políticas_e_privacidade.md`).
* **Execução Otimizada:** Abra um novo chat e arraste tanto a pasta da *nova skill* quanto o *documento* para a área de conversa.
* **Comando:** `Analise, use a skill [Referência da Skill] para analisar o documento [Referência do Documento]. Salve o resultado na pasta políticas.`
* **Resultado:** O Antigravity executa os scripts da skill e salva um relatório em Markdown na pasta indicada.

### O que o Relatório Identificou?
A skill funcionou perfeitamente e encontrou duas cláusulas gravemente ilegais (Seções 6 e 11) que haviam sido plantadas no documento:
1.  Venda de dados pessoais sem aviso e sem opção de recusa.
2.  Negativa arbitrária de direitos dos titulares com cobrança de taxas (risco crítico).