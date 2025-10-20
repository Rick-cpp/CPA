# GDD — CPP Project Assistant
**Versão:** 0.1  
**Autor:** Rickz
**Data:** 18/10/2025

---

## 1. Visão Geral
O aplicativo é um utilitário de linha de comando (CMD App) para auxiliar no desenvolvimento de projetos C++.  
Seu objetivo inicial é automatizar tarefas comuns de setup e organização de código, mantendo compatibilidade com o sistema de build **SCons**.

---

## 2. Propósito
Fornecer um ambiente rápido e padronizado para iniciar, configurar e manter projetos C++ no Windows, usando comandos simples e diretos.

---

## 3. Público-Alvo
Desenvolvedores C++ que desejam automatizar a criação de templates de projeto e manipulação de arquivos sem depender de IDEs.

---

## 4. Funções Principais (Versão Inicial)

### 1. Gerar Template de SCons
- **Comando:** `app --template basic`
- **Descrição:** Cria estrutura padrão:
    src/
    include/
    build/
    SConstruct
    main.cpp
- Gera automaticamente um **SConstruct** funcional com configurações básicas de compilação.

---

### 2. Conversor `.hpp` → `.h` + `.cpp`
- **Comando:** `app --split header.hpp`
- **Descrição:** Lê um arquivo `.hpp` e gera:
- `header.h` (declarações)
- `header.cpp` (definições)
- Detecta automaticamente **namespaces** e **classes**.
- Ajusta **includes** e **header guards**.

---

### 3. Ajuda / Help
- **Comando:** `app --help`
- **Descrição:** Exibe todos os comandos disponíveis e uma breve explicação de cada um.

---

## 5. Estrutura Interna
/core → scripts principais e parsers de template
/templates → arquivos .txt dos templates SCons
/utils → funções auxiliares (ex: parser de header)
/cmd → interface de linha de comando (.bat ou .py)

---

## 6. Fluxo de Execução
1. Usuário executa um comando (`app --template basic`, por exemplo).  
2. O CMD App interpreta o comando.  
3. Executa a função correspondente:
   - Cria arquivos/pastas (template)
   - Lê e divide `.hpp` (split)
   - Exibe ajuda (help)  
4. Exibe mensagens formatadas no terminal.

---

## 7. Expansões Futuras
- Criação de projetos **CMake** e **Makefile**.  
- Integração com **Git**.  
- Geração automática de **Doxygen**.  
- Template customizável por arquivo `.cfg`.

---

## 8. Estado Atual
Fase de **planejamento e estruturação inicial**.  
Nenhuma função implementada ainda.
