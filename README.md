

🖥️ **Pichau Web Scraper - Selenium + Undetected ChromeDriver**

Este projeto é um web scraper automatizado desenvolvido em Python. Ele coleta dados de computadores da seção "Pichau Gamer" no site da Pichau Informática, acessando páginas, extraindo informações dos produtos e salvando tudo em arquivos CSV e JSON.

---

**Funcionalidades:**

* Acessa automaticamente todas as páginas de produtos.
* Coleta informações como:

  * SKU e disponibilidade
  * Preço normal, à vista (Pix) e parcelado
  * Componentes: processador, placa-mãe, memória, GPU, fonte, etc.
* Exporta os dados para dois arquivos:

  * `pcs.csv` (planilha)
  * `pcs.json` (formato estruturado)

---

**Tecnologias usadas:**

* Python 3.x
* Selenium
* undetected-chromedriver
* Módulos padrão: csv, json, time

---

**Instalação:**

1. Clone o repositório:

   * git clone [https://github.com/seu-usuario/webscrapt-items.git](https://github.com/seu-usuario/webscrapt-items.git)
   * cd webscrapt-items

2. Crie e ative um ambiente virtual:

   * `python -m venv venv`
   * Windows: `venv\Scripts\activate`
   * Linux/macOS: `source venv/bin/activate`

3. Instale as dependências:

   * `pip install -r requirements.txt`

---

**Como executar:**

* Execute o script principal com o comando: `python main.py`
* O navegador será iniciado automaticamente, e o scraper começará a coletar os dados.

---

**Estrutura do projeto:**

* `csv do codigo/`: Pasta onde os arquivos gerados podem ser salvos
* `venv/`: Ambiente virtual (ignorado pelo Git)
* `main.py`: Código principal do scraper
* `requirements.txt`: Bibliotecas necessárias
* `.gitignore`: Arquivos/pastas ignorados pelo Git
* `README.md`: Este arquivo de descrição

---

**Observações importantes:**

* O scraper usa navegação real com o navegador Chrome, então pode ser detectado se for usado de forma repetitiva.
* Caso o site da Pichau mude seu layout, pode ser necessário atualizar os seletores de classe e CSS no código.

---

**Licença:**

Este projeto é de código aberto, licenciado sob a MIT License.

---

