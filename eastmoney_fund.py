from pyppeteer import launch
import asyncio
import pandas as pd
from lxml import etree

fund_codes = []


async def create_page():
    browser = await launch()
    page = await browser.newPage()
    # 设置页面视图大小
    await page.setViewport(viewport={'width': 1280, 'height': 800})

    return browser, page


async def close_browser(browser):
    await browser.close()


async def get_all_codes(page):
    await page.goto('http://fund.eastmoney.com/HBJJ_dwsy.html')
    # 获取基金代码
    rows = await page.xpath('//table[@class="dbtable"]//tr[contains(@id, "tr")]')

    for row in rows:
        # 获取每一列
        cols = await row.xpath('./td')
        # 获取第4列的基金代码
        fund_code = await (await cols[3].getProperty('textContent')).jsonValue()
        # 获取基金简称的列
        fund_name_col = await cols[4].xpath('./nobr/a')
        fund_name = await (await fund_name_col[0].getProperty('textContent')).jsonValue()
        fund_codes.append([fund_code, fund_name])


def get_data(html, fund_name):
    '''
    获取历史净值表格数据
    :param html:
    :return:
    '''
    res_elements = etree.HTML(html)
    table = res_elements.xpath('//div[@id="jztable"]/table')
    table = etree.tostring(table[0], encoding='utf-8').decode()
    df = pd.read_html(table, encoding='utf-8', header=0)[0]
    df.to_csv('data/{}.csv'.format(fund_name), index=False)

    return df


async def get_history_net_value_detail(page, fund_code, fund_name):
    url = 'http://fundf10.eastmoney.com/jjjz_{}.html'
    print('{}: {}'.format(fund_name, url.format(fund_code)))
    await page.goto(url.format(fund_code))
    html = await page.content()
    df = get_data(html, fund_name)
    print(df)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    browser, page = loop.run_until_complete(create_page())
    loop.run_until_complete(get_all_codes(page))
    print(fund_codes)
    tasks = [asyncio.ensure_future(get_history_net_value_detail(page, fund_code, fund_name)) for fund_code, fund_name in fund_codes[:50]]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.run_until_complete(close_browser(browser))
