## 安装
安装pyppeteer，确保安装路径不含中文，否则在下一步安装chromium会报错：
```
pip install pyppeteer
```

安装chromium，该安装方式不行的话可以使用下面另一种方法：
```
# 注意不是pyppeteer -install
pyppeteer-install
```

运行项目根目录下的config.py文件获取pyppeteer对应的chrominum版本下载地址和相应的本地配置路径：
```
Input>>> python config.py
Output>>> chromium下载路径：
            - https://storage.googleapis.com/chromium-browser-snapshots/Win/575458/chrome-win32.zip
          压缩包解压路径：
            - C:\Users\LoveTech\AppData\Local\pyppeteer\pyppeteer\local-chromium\575458\chrome-win32\chrome.exe
```

## 问题
运行一段时间后报错
