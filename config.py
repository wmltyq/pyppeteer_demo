'''
运行该文件获取chromnium下载URL和解压配置路径
'''
import os
from pathlib import Path
import sys
from pyppeteer import __chromium_revision__, __pyppeteer_home__

DOWNLOADS_FOLDER = Path(__pyppeteer_home__) / 'local-chromium'
DEFAULT_DOWNLOAD_HOST = 'https://storage.googleapis.com'
DOWNLOAD_HOST = os.environ.get(
    'PYPPETEER_DOWNLOAD_HOST', DEFAULT_DOWNLOAD_HOST)
BASE_URL = f'{DOWNLOAD_HOST}/chromium-browser-snapshots'

REVISION = os.environ.get(
    'PYPPETEER_CHROMIUM_REVISION', __chromium_revision__)

downloadURLs = {
    'linux': f'{BASE_URL}/Linux_x64/{REVISION}/chrome-linux.zip',
    'mac': f'{BASE_URL}/Mac/{REVISION}/chrome-mac.zip',
    'win32': f'{BASE_URL}/Win/{REVISION}/chrome-win32.zip',
    'win64': f'{BASE_URL}/Win_x64/{REVISION}/chrome-win32.zip',
}

chromiumExecutable = {
    'linux': DOWNLOADS_FOLDER / REVISION / 'chrome-linux' / 'chrome',
    'mac': (DOWNLOADS_FOLDER / REVISION / 'chrome-mac' / 'Chromium.app' /
            'Contents' / 'MacOS' / 'Chromium'),
    'win32': DOWNLOADS_FOLDER / REVISION / 'chrome-win32' / 'chrome.exe',
    'win64': DOWNLOADS_FOLDER / REVISION / 'chrome-win32' / 'chrome.exe',
}


def current_platform() -> str:
    """Get current platform name by short string."""
    if sys.platform.startswith('linux'):
        return 'linux'
    elif sys.platform.startswith('darwin'):
        return 'mac'
    elif (sys.platform.startswith('win') or
          sys.platform.startswith('msys') or
          sys.platform.startswith('cyg')):
        if sys.maxsize > 2 ** 31 - 1:
            return 'win64'
        return 'win32'
    raise OSError('Unsupported platform: ' + sys.platform)


def get_url() -> str:
    """Get chromium download url."""
    return downloadURLs[current_platform()]

print('chromium下载路径：\n  - {}'.format(get_url()))
print('压缩包解压路径：\n  - {}'.format(chromiumExecutable[current_platform()]))
