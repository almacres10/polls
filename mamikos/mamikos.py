import pandas as pd
from datetime import datetime
import os, sys
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException, JavascriptException, UnexpectedAlertPresentException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait, Select

executable_path = r"C:\Users\817932702\mamikos\chromedriver\120\chromedriver.exe"
# executable_path = r"D:\proyek\chromedriver\120\chromedriver.exe"
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

# oke_button = driver.find_element(By.XPATH, '//*[@id="desktopBannerWrapped"]/div/div[3]/div[1]/button[1]')
# oke_button.click()

list_df = []

# Inisialisasi indeks awal
start_index = 1

while True:
    try:
        for i in range(start_index, start_index + 20):
            xpath = '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[1]/div[' + str(i) + ']'
            
            
            try:
                elemen = driver.find_element(By.XPATH, xpath)
                isi_elemen = elemen.text
                data_elemen = isi_elemen.split('\n')

                df = pd.DataFrame({
                    'Jenis': [data_elemen[0]],
                    'Status Kamar': [data_elemen[1]] if len(data_elemen) > 1 else None,
                    'Nama Kost': [data_elemen[2]] if len(data_elemen) > 1 else None,
                    'Lokasi': [data_elemen[3]],
                    'Fasilitas': [data_elemen[4]],
                    'Rating': [data_elemen[5]],
                    'Diskon': [data_elemen[6]] if len(data_elemen) > 1 else None,
                    'Harga': [data_elemen[7]]
                })

                list_df.append(df)

                        # Coba temukan next_button
                next_button = driver.find_element(By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[2]/div/a')
                next_button.click()

                # Tunggu hingga halaman selanjutnya dimuat
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[5]/div/div[1]/div/div/div[1]/div[1]/div[1]'))
                )

                # Scroll ke bawah untuk memuat lebih banyak data
                scroll_down()
                time.sleep(2)  # Tunggu sebentar setelah setiap scroll

            except UnexpectedAlertPresentException:
                # Tangani popup dengan menekan tombol OK
                alert = driver.switch_to.alert
                alert.accept()
                print("Popup ditangani.")
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

        # Gabungkan semua DataFrames menjadi satu
        final_df = pd.concat(list_df, ignore_index=True)

        # Atur ulang indeks
        start_index += 20
        print(final_df)

    # except NoSuchElementException:
    #     # Jika next_button tidak ditemukan, keluar dari loop
    #     break
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


