# Sistema de Vendas ReVeste

Um sistema de desktop para gerenciamento de vendas, clientes e produtos para a ReVeste.

---

### **Tabela de Conteúdos**
1.  Sobre o Projeto
    * Construído Com
2.  Começando
    * Pré-requisitos
    * Instalação
3.  Uso
4.  Roadmap
5.  Licença
6.  Contato

---

### **Sobre o Projeto**

Este projeto é um sistema de vendas de desktop construído para a "ReVeste". Ele permite o gerenciamento completo de cadastros, vendas e históricos. A aplicação possui uma interface gráfica intuitiva com abas, facilitando a navegação entre as diferentes funcionalidades. O sistema utiliza um banco de dados SQLite para armazenar e gerenciar os dados de forma persistente.

**Funcionalidades principais:**
* Cadastro de clientes e produtos.
* Registro de vendas detalhado, associando clientes e produtos.
* Visualização do histórico de todas as transações.
* Listagem e remoção de clientes cadastrados.
* Cálculo e exibição de totais de vendas por dia, semana e mês.

---

### **Construído Com**

Esta seção lista os principais frameworks e bibliotecas usadas para criar o projeto.

* ![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
* ![PyQt5](https://img.shields.io/badge/PyQt5-414345?style=for-the-badge&logo=qt&logoColor=white)
* ![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)

---

### **Começando**

Para obter uma cópia local em funcionamento, siga estes passos simples.

#### **Pré-requisitos**

Certifique-se de que você tem o Python instalado em sua máquina. A biblioteca `PyQt5` é necessária para a interface gráfica. **AVISO: O projeto não funciona no PyCharm devido a alguma incompatibilidade.**

* Instale o PyQt5 via pip:
    ```sh
    pip install PyQt5
    ```

#### **Instalação**

1.  Baixe e descompacte os arquivos do projeto em um diretório de sua preferência.
2.  Navegue até a pasta do projeto.
3.  Execute o script Python. O banco de dados (`ReVesteDB.db`) será criado automaticamente no primeiro uso.
    ```sh
    python nome_do_seu_script.py
    ```

---

### **Uso**

Após iniciar a aplicação, você verá uma janela com quatro abas principais:

1.  **Cadastro**: Use esta aba para adicionar novos clientes ou produtos ao banco de dados. Simplesmente preencha o nome e clique em "Salvar".
2.  **Registro de Vendas**: Registre uma nova venda selecionando a data, um cliente e um produto das listas suspensas. Você também pode adicionar detalhes adicionais sobre a transação.
3.  **Histórico de Vendas**: Visualize todas as vendas registradas em uma tabela. Use o botão "Calcular Totais" para ver um resumo das vendas por período.
4.  **Clientes Cadastrados**: Veja uma lista de todos os clientes. Você pode selecionar um cliente na tabela e removê-lo clicando no botão "Remover Cliente", desde que ele não tenha vendas associadas.

---

### **Roadmap**

* [ ] Adicionar mais validações de entrada
* [ ] Implementar edição de registros existentes (clientes, produtos, vendas)
* [ ] Criar um sistema de login para diferentes tipos de perfil
* [ ] Suporte a múltiplos idiomas

---

### **Licença**

Distribuído sob a Licença Unlicense.

---

### **Autores**

Igor Alves (Coding, Documentação)  
Luis Augusto (Coding)  
Pedro Rodrigues (Coding, Documentação)  
Morgana Barbosa (Coding)  
Vanda Vitorio (Coding)
