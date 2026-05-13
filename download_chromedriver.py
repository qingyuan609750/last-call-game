import urllib.request
import zipfile
import os

# ChromeDriver 下载地址（对应 Chrome 139.0.7258.140）
url = "https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.140/win64/chromedriver-win64.zip"

download_path = "chromedriver-win64.zip"
extract_path = "D:\\ChromeDriver"

print("正在下载 ChromeDriver...")
urllib.request.urlretrieve(url, download_path)
print(f"下载完成: {download_path}")

print("正在解压...")
with zipfile.ZipFile(download_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)
print(f"解压完成到: {extract_path}")

# 删除压缩包
os.remove(download_path)
print("清理完成")

print(f"\nChromeDriver 已更新到: {extract_path}\\chromedriver-win64\\chromedriver.exe")
import urllib.request
import zipfile
import os

# ChromeDriver 下载地址（对应 Chrome 139.0.7258.140）
url = "https://storage.googleapis.com/chrome-for-testing-public/139.0.7258.140/win64/chromedriver-win64.zip"

download_path = "chromedriver-win64.zip"
extract_path = "D:\\ChromeDriver"

print("正在下载 ChromeDriver...")
urllib.request.urlretrieve(url, download_path)
print(f"下载完成: {download_path}")

print("正在解压...")
with zipfile.ZipFile(download_path, 'r') as zip_ref:
    zip_ref.extractall(extract_path)
print(f"解压完成到: {extract_path}")

# 删除压缩包
os.remove(download_path)
print("清理完成")

print(f"\nChromeDriver 已更新到: {extract_path}\\chromedriver-win64\\chromedriver.exe")
