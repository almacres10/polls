import re, pandas as pd, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait

executable_path = r"D:\proyek\scrapper\chromedriver\120\chromedriver.exe"
service = Service(executable_path)
options = webdriver.ChromeOptions()
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False) 
options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(service=service, options=options)

# Fungsi untuk mensimulasikan scroll ke bawah halaman
def scroll_down():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

start_time = time.time()

driver.get("https://mamikos.com/") 
cari = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div[4]/div/div/div/div[1]')))
cari.click()
area = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div[13]/div/div[2]/div[2]/ul/li[2]/a')))
area.click()
kota = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div[13]/div/div[2]/div[4]/div/div[25]/details/summary')))
kota.click()
kota_2 = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="home"]/div[13]/div/div[2]/div[4]/div/div[25]/details/div/a[5]')))
kota_2.click()


list_df = []

# Inisialisasi indeks awal
start_index = 1

while True:
    try:
        # Coba temukan next_button
        next_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[2]/div/a')
        next_button.click()

        # Tunggu hingga halaman selanjutnya dimuat
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[1]/div[1]'))
        )

        scroll_down()
        time.sleep(3)

        # Atur ulang indeks
        start_index += 20

    except ElementNotInteractableException:
        # Tangani popup dengan menekan tombol OK
        alert_button_xpath = '//*[@id="filterKostTypeWrapper"]/div/div[1]/div[1]/div/div/div[3]/button'
        try:
            alert_button = driver.find_element(By.XPATH, alert_button_xpath)
            alert_button.click()
            print("Popup ditangani.")
        except NoSuchElementException:
            print("Tidak dapat menemukan tombol OK pada popup.")
            break
    except NoSuchElementException:
        print("Tidak ada next")
        break

elemen_nama = driver.find_elements(By. CLASS_NAME, 'rc-info')
elemen_fasilitas = driver.find_elements(By. CLASS_NAME, 'rc-facilities')
elemen_harga = driver.find_elements(By. CLASS_NAME, 'rc-price__text')

data = []

for nama, fasilitas, harga in zip(elemen_nama, elemen_fasilitas, elemen_harga):
    fasilitas_text = re.sub(r'[^a-zA-Z0-9\s]', '', fasilitas.text)


    data.append({
        'Nama_Kos': nama.text,
        'Fasilitas': fasilitas_text,
        'Harga': harga.text
    })

# Membuat DataFrame dari list data setelah loop selesai
df = pd.DataFrame(data)
