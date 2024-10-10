from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

###################### Settings #####################
screenshotDir = "Screenshots"
screenWidth = 400
screenHeight = 800
filePath = "Screenshots"

##################### Functions #####################
def setupDriver(url):
    options = webdriver.FirefoxOptions()
    options.headless = False
    options.enable_mobile = False

    driver = webdriver.Firefox(options=options)

    # Actually go to URL
    driver.get(url)
    time.sleep(5)

    wait = WebDriverWait(driver, 10)

    return driver, wait

def takeScreenshot(driver, wait, submission):
    method = By.ID
    handle = "post-title-t3_" + submission.id
    search = wait.until(EC.presence_of_element_located((method, handle)))
    driver.execute_script("window.focus();")

    fileName = f"{screenshotDir}/{filePath}-{handle}.png"
    fp = open(fileName, "wb")
    fp.write(search.screenshot_as_png)
    fp.close()
    return fileName

def getScreenshot(submission):
    driver, wait = setupDriver(submission.url)
    fileName = submission.TitleSC = takeScreenshot(driver, wait, submission)
    driver.quit()
    return fileName