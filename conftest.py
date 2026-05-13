import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")

    # 指定 ChromeDriver 路径（修改为你的实际路径）
    # 方式1：放在项目根目录
    # service = Service(executable_path="./chromedriver.exe")

    # 方式2：指定绝对路径
    # service = Service(executable_path=r"D:\tools\chromedriver.exe")

    # 方式3：让 Selenium 自动查找（需要能联网下载）
    driver = webdriver.Chrome(options=options)

    # 如果指定了路径，用这行：
    # driver = webdriver.Chrome(service=service, options=options)

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def wait(driver):
    return WebDriverWait(driver, 10)
