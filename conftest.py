import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # 指定 ChromeDriver 路径
    # 如果 chromedriver.exe 在项目根目录，用这行：
    service = Service(executable_path="./chromedriver.exe")

    # 如果 chromedriver 在其他位置，修改上面的路径，例如：
    # service = Service(executable_path=r"C:\path\to\chromedriver.exe")

    driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)
