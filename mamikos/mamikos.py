import pandas as pd
from datetime import datetime
import os, sys, re
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, JavascriptException, UnexpectedAlertPresentException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select

# executable_path = r"C:\Users\817932702\mamikos\chromedriver\120\chromedriver.exe"
executable_path = r"D:\proyek\chromedriver\120\chromedriver.exe"
# executable_path = r'D:\proyek\scrapper\chromedriver\120\chromedriver.exe'
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

time.sleep(5)

cari = driver.find_element(By. XPATH, '//*[@id="home"]/div[4]/div/div/div/div[1]')
cari.click()

time.sleep(2)

area = driver.find_element(By. XPATH, '//*[@id="home"]/div[13]/div/div[2]/div[2]/ul/li[2]/a')
area.click()

time.sleep(2)

kota = driver.find_element(By. XPATH, '//*[@id="home"]/div[13]/div/div[2]/div[4]/div/div[25]/details/summary')
kota.click()

time.sleep(2)

kota_2 = driver.find_element(By. XPATH, '//*[@id="home"]/div[13]/div/div[2]/div[4]/div/div[25]/details/div/a[5]')
kota_2.click()

time.sleep(5)

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
        time.sleep(2)

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
        break

time.sleep(3)


nama_kos = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[1]/div[*]/div/div/div/div[2]/div[2]/div/span[1]')
alamat_kos = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[1]/div[*]/div/div/div/div[2]/div[2]/div/span[2]')
fasilitas = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[1]/div[*]/div/div/div/div[2]/div[3]/div')
harga = driver.find_elements(By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[1]/div[*]/div/div/div/div[2]/div[4]/div/div/div/span[1]')

# Buat list untuk menyimpan data
data = []

for nama, alamat, fasilitas, harga in zip(nama_kos, alamat_kos, fasilitas, harga):
    fasilitas_text = re.sub(r'[^a-zA-Z0-9\s]', '', fasilitas.text)

    data.append({
        'Nama Kos': nama.text,
        'Alamat Kos': alamat.text,
        'Fasilitas': fasilitas.text,
        'Harga': harga.text
    })

# Membuat DataFrame dari list data setelah loop selesai
df = pd.DataFrame(data)

df.to_csv('output3.csv', index=False)

end_time = time.time()
execution_time = end_time - start_time
print("Waktu eksekusi:", execution_time, "detik")
