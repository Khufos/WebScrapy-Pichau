import os
import csv
import json
import time
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc

# ========== CONFIGURA NAVEGADOR ==========
options = uc.ChromeOptions()
options.add_argument('--disable-gpu')
options.add_argument('--window-size=1920,1080')
driver = uc.Chrome(options=options)

# ========== CONTROLE DE PROGRESSO ==========
progress_file = 'progress.json'
if os.path.exists(progress_file):
    with open(progress_file, 'r') as f:
        progresso = json.load(f)
        pagina = progresso.get('pagina', 1)
        skus_existentes = set(progresso.get('skus', []))
else:
    pagina = 1
    skus_existentes = set()

# ========== INICIALIZA CSV ==========
csv_path = 'pcs.csv'
csv_existe = os.path.exists(csv_path)
csvfile = open(csv_path, 'a', newline='', encoding='utf-8')
writer = csv.writer(csvfile)

if not csv_existe:
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

# ========== NAVEGAÇÃO ==========
url_base = "https://www.pichau.com.br/computadores/pichau-gamer?page="
wait = WebDriverWait(driver, 15)
dados = []
NO_ITEM = "Sem item no momento"

while True:
    print(f"\n📄 Página {pagina}...")
    driver.get(url_base + str(pagina))

    try:
        computadores = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.MuiGrid2-grid-xs-6')))
    except:
        print("❌ Não foi possível carregar os computadores desta página.")
        break

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

            if indice_etiqueta in skus_existentes:
                print(f"[{i+1}] Produto já processado (SKU: {indice_etiqueta}), pulando.")
                driver.back()
                time.sleep(1)
                continue

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

            linha = [
                indice_etiqueta,
                disponibilidade,
                valor_limpo,
                valor_avista_pix,
                parcelas_cartao,
                get_text_from_item(0),  # Processador
                get_text_from_item(1),  # Cooler
                get_text_from_item(2),  # Placa Mãe
                get_text_from_item(3),  # Memória
                get_text_from_item(4),  # Armazenamento
                get_text_from_item(5),  # Placa de Vídeo
                get_text_from_item(6),  # Fonte
                get_text_from_item(7),  # Gabinete
                get_text_from_item(8),  # Cabo de Vídeo
                get_text_from_item(9),  # Cabo de Força
                get_text_from_item(10), # Monitor
                get_text_from_item(11)  # Kit Periféricos
            ]

            writer.writerow(linha)
            dados.append(linha)
            skus_existentes.add(indice_etiqueta)
            print(f"[{i+1}] Produto (SKU: {indice_etiqueta}) capturado com sucesso.")

            driver.back()
            time.sleep(2)

        except Exception as e:
            print(f"[{i+1}] Erro ao processar item: {e}")
            driver.back()
            time.sleep(2)

    # Salva progresso a cada página
    with open(progress_file, 'w', encoding='utf-8') as f:
        json.dump({'pagina': pagina + 1, 'skus': list(skus_existentes)}, f)

    try:
        next_button = driver.find_element(By.CSS_SELECTOR, 'li button[aria-label="Go to next page"]')
        if "Mui-disabled" in next_button.get_attribute("class"):
            print("🚫 Última página alcançada.")
            break
        else:
            pagina += 1
            time.sleep(3)
    except Exception as e:
        print(f"❌ Erro ao tentar avançar para próxima página: {e}")
        break

# Finaliza
csvfile.close()
driver.quit()
print("✅ Scraping finalizado com sucesso.")
