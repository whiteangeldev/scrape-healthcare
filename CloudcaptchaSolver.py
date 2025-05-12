import os
import random
import asyncio
import aiohttp
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from pydub import AudioSegment
import speech_recognition as sr

class RecaptchaSolver:
    def __init__(self, driver):
        self.driver = driver

    async def download_audio(self, url, path):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(path, 'wb') as f:
                    f.write(await response.read())
        print("Downloaded audio asynchronously.")

    def solveCaptcha(self):
        try:
            # Switch to the CAPTCHA iframe
            
            iframe_inner = WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[contains(@title, 'DataDome CAPTCHA')]"))
            )
            
            # Click on the CAPTCHA box
            print('1234')
            # time.sleep(100)
            WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'captcha__audio__button'))
            ).click()
            print('2345')
            self.solveAudioCaptcha()

        except Exception as e:
            print(f"An error occurred while solving CAPTCHA: {e}")
            self.driver.switch_to.default_content()  # Ensure we switch back in case of error
            raise

    def words_to_number(self, word_string):
        word_to_digit = {
            'zero': '0',
            'one': '1',
            'two': '2',
            'three': '3',
            'four': '4',
            'five': '5',
            'six': '6',
            'seven': '7',
            'eight': '8',
            'nine': '9'
        }
        
        words = word_string.lower().split()
        digits = [word_to_digit[word] for word in words if word in word_to_digit]
        return digits


    def solveAudioCaptcha(self):
        try:
            self.driver.switch_to.default_content()
            
            # Switch to the audio CAPTCHA iframe
            iframe_audio = WebDriverWait(self.driver, 10).until(
                EC.frame_to_be_available_and_switch_to_it((By.XPATH, '//iframe[@title="DataDome CAPTCHA"]'))
            )

            # Click on the audio button
            audio_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.NAME, 'Listen to the numbers to write'))
            )
            audio_button.click()

            # Get the audio source URL
            # <audio class="audio-captcha-track" src="https://dd.prod.captcha-delivery.com/audio/2025-04-29/en/ac5ec483feaae0cbfc9b6c145a6a800d.wav" preload="none"></audio>
            audio_source = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'audio-captcha-track'))
            ).get_attribute('src')
            print(f"Audio source URL: {audio_source}")
            
            # Download the audio to the temp folder asynchronously
            temp_dir = os.getenv("TEMP") if os.name == "nt" else "/tmp/"
            path_to_mp3 = os.path.normpath(os.path.join(temp_dir, f"{random.randrange(1, 1000)}.mp3"))
            path_to_wav = os.path.normpath(os.path.join(temp_dir, f"{random.randrange(1, 1000)}.wav"))
            
            asyncio.run(self.download_audio(audio_source, path_to_wav))

            # Convert mp3 to wav
            # sound = AudioSegment.from_mp3(path_to_mp3)
            # sound.export(path_to_wav, format="wav")
            # print("Converted MP3 to WAV.")

            # Recognize the audio
            recognizer = sr.Recognizer()
            with sr.AudioFile(path_to_wav) as source:
                audio = recognizer.record(source)
            captcha_text = recognizer.recognize_google(audio).lower()
            print(f"Recognized CAPTCHA text: {captcha_text}")
            
            captcha_text.replace("please type the numbers you hear ", "")
            nums = self.words_to_number(captcha_text)
            print(nums)
            
            
            # Enter the CAPTCHA text
            # audio_inputs = WebDriverWait(self.driver, 10).until(
            #     EC.presence_of_element_located((By.CLASS_NAME, 'audio-captcha-inputs'))
            # )
            audio_inputs = self.driver.find_elements(By.CLASS_NAME, 'audio-captcha-inputs')
            cnt = 0
            # for inp in audio_inputs:
            #     time.sleep(random.uniform(0.5, 1))
            #     inp.send_keys(nums[cnt])
            #     cnt = cnt + 1
            
            print("Entered and submitted CAPTCHA text.")

            time.sleep(100)
            # Verify CAPTCHA is solved
            # if self.isSolved():
            #     print("Audio CAPTCHA solved.")
            # else:
            #     print("Failed to solve audio CAPTCHA.")
            #     raise Exception("Failed to solve CAPTCHA")
            
            # WebDriverWait(self.driver, 10).until(
            #     EC.element_to_be_clickable((By.NAME, 'submit'))
            # ).click()

        except Exception as e:
            print(f"An error occurred while solving audio CAPTCHA: {e}")
            self.driver.switch_to.default_content()  # Ensure we switch back in case of error
            raise

        finally:
            # Always switch back to the main content
            self.driver.switch_to.default_content()

    def isSolved(self):
        try:
            # Switch back to the default content
            self.driver.switch_to.default_content()

            # Switch to the reCAPTCHA iframe
            iframe_check = self.driver.find_element(By.XPATH, "//iframe[contains(@title, 'reCAPTCHA')]")
            self.driver.switch_to.frame(iframe_check)
            # Find the checkbox element and check its aria-checked attribute
            checkbox = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, 'recaptcha-anchor'))
            )
            
            
            print("checkbox+")
            print(checkbox)
            aria_checked = checkbox.get_attribute("aria-checked")
            print(aria_checked)
            # Return True if the aria-checked attribute is "true" or the checkbox has the 'recaptcha-checkbox-checked' class
            #return True
            return aria_checked == "true" or 'recaptcha-checkbox-checkmark' in checkbox.get_attribute("class")

        except Exception as e:
            print(f"An error occurred while checking if CAPTCHA is solved: {e}")
            return False