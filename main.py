from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc
import csv
import time
import json

# ========== CONFIGURA NAVEGADOR ==========
options = uc.ChromeOptions()
# options.add_argument('--headless=new')
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
driver = uc.Chrome(options=options)

# ========== ACESSA PÁGINA ==========
url = "https://www.pichau.com.br/computadores/pichau-gamer"
# url = "https://www.pichau.com.br/computadores/pichau-gamer?page=18"
driver.get(url)

wait = WebDriverWait(driver, 15)
dados = []
NO_ITEM = "Sem item no momento"

# ========== INICIALIZA CSV ==========
csvfile = open('pcs.csv', 'w', newline='', encoding='utf-8')
writer = csv.writer(csvfile)
writer.writerow([
    "SKU",
    "Disponibilidade",
    "Preço de",
    "Preço à vista no Pix",
    "Parcelamento no cartão",
    "Processador",
    "Cooler",
    "Placa Mãe",
    "Memória",
    "Armazenamento",
    "Placa de Vídeo",
    "Fonte",
    "Gabinete",
    "Cabo de Vídeo",
    "Cabo de Força",
    "Monitor",
    "Kit Periféricos"
])

# ========== LOOP DE PAGINAÇÃO ==========
pagina = 1
while True:
    print(f"\n📄 Página {pagina}...")

    try:
        computadores = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.MuiGrid2-grid-xs-6')))
    except:
        print("❌ Não foi possível carregar os computadores desta página.")
        break

    # ========== LOOP NOS PRODUTOS ==========
    for i in range(len(computadores)):
        try:
            computadores = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.MuiGrid2-grid-xs-6')))
            link = computadores[i].find_element(By.TAG_NAME, 'a')
            link.click()

            div_info = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mui-15vzl0p-availability_sku')))
            time.sleep(2)
            spans = div_info.find_elements(By.TAG_NAME, 'span')
            disponibilidade = spans[0].text.strip()
            indice_etiqueta = spans[1].text.strip()

            div_info_valores = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'mui-10zcgyp-mainWrapper')))
            valor_cortado = div_info_valores.find_element(By.CLASS_NAME, 'mui-1tsvxj0-dePor').text
            valor_limpo = valor_cortado.replace("deR$", "").replace("por", "").strip().replace(".", "").replace(",", ".")
            valor_limpo = float(valor_limpo)

            valor_avista_pix = div_info_valores.find_element(By.CLASS_NAME, 'mui-1s7x6y7-price_vista').text.strip()
            parcelas_cartao = div_info_valores.find_element(By.CLASS_NAME, 'mui-11gafbb-price_parcelado_text-smallFontsPricePix').text.strip()

            button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.mui-1pdyvwj-completeButtonWrapper button')))
            button.click()

            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.mui-1ysi7iz-mainContainer')))
            itens = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "mui-175gxkb-listItem")))

            def get_text_from_item(index):
                try:
                    return itens[index].find_element(By.TAG_NAME, 'p').text.strip()
                except (IndexError, Exception):
                    return NO_ITEM

            descricao_processador = get_text_from_item(0)
            cooler = get_text_from_item(1)
            placa_mae = get_text_from_item(2)
            memoria = get_text_from_item(3)
            armazenamento = get_text_from_item(4)
            placa_de_video = get_text_from_item(5)
            fonte = get_text_from_item(6)
            gabinete = get_text_from_item(7)
            cabo_video = get_text_from_item(8)
            cabo_de_forca = get_text_from_item(9)
            monitor = get_text_from_item(10)
            kit_periferico = get_text_from_item(11)

            print(f"[{i+1}] Produto capturado com sucesso.")

            linha = [
                indice_etiqueta,
                disponibilidade,
                valor_limpo,
                valor_avista_pix,
                parcelas_cartao,
                descricao_processador,
                cooler,
                placa_mae,
                memoria,
                armazenamento,
                placa_de_video,
                fonte,
                gabinete,
                cabo_video,
                cabo_de_forca,
                monitor,
                kit_periferico
            ]

            dados.append(linha)
            writer.writerow(linha)  # 🔥 Salva item no CSV imediatamente

            driver.back()
            time.sleep(2)

        except Exception as e:
            print(f"[{i+1}] Erro ao processar item: {e}")
            driver.back()
            time.sleep(2)

    # ========== TENTA IR PARA PRÓXIMA PÁGINA ==========
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li button[aria-label="Go to next page"]')
        classes = next_button.get_attribute("class")

        if "Mui-disabled" in classes:
            print("🚫 Última página alcançada.")
            break
        else:
            next_button.click()
            pagina += 1
            time.sleep(3)
    except Exception as e:
        print(f"❌ Erro ao tentar avançar para próxima página: {e}")
        break

# ========== SALVA JSON ==========
json_dados = []
for linha in dados:
    json_dados.append({
        "SKU": linha[0],
        "Disponibilidade": linha[1],
        "Preço de": linha[2],
        "Preço à vista no Pix": linha[3],
        "Parcelamento no cartão": linha[4],
        "Processador": linha[5],
        "Cooler": linha[6],
        "Placa Mãe": linha[7],
        "Memória": linha[8],
        "Armazenamento": linha[9],
        "Placa de Vídeo": linha[10],
        "Fonte": linha[11],
        "Gabinete": linha[12],
        "Cabo de Vídeo": linha[13],
        "Cabo de Força": linha[14],
        "Monitor": linha[15],
        "Kit Periféricos": linha[16]
    })

with open('pcs.json', 'w', encoding='utf-8') as f:
    json.dump(json_dados, f, ensure_ascii=False, indent=2)

print("\n✅ Arquivo 'pcs.json' salvo com sucesso!")

# ========== FECHA ARQUIVO CSV ==========
csvfile.close()
print("✅ Arquivo 'pcs.csv' finalizado e salvo com sucesso!")

driver.quit()
