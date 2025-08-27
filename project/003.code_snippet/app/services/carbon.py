from playwright.async_api import async_playwright
import tempfile
import os


async def create_carbon_image(content, file_path) -> str:
    """
    Playwright를 이용해 carbon.now.sh에서 코드 이미지를 생성하고 임시 파일 경로를 반환합니다.
    """
    print(f'content: {content}, file_path: {file_path}')
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            
            await page.goto("https://carbon.now.sh")

            # 코드 입력 영역 찾아서 코드 붙여넣기
            # carbon.now.sh의 DOM 구조에 따라 선택자는 변경될 수 있습니다.
            await page.locator('.CodeMirror-code').click()
            await page.keyboard.down('Control')
            await page.keyboard.press('A')
            await page.keyboard.up('Control')
            await page.keyboard.press('Backspace')
            await page.keyboard.type(content)

            # 언어 설정 (자동 감지)
            # await page.locator('text=Automatic').click()
            
            # Export 버튼 클릭
            await page.locator('text=Quick export').click()
            
            # 다운로드 시작을 기다림
            async with page.expect_download() as download_info:
                # PNG 버튼 클릭
                await page.keyboard.press('Enter')
            
            download = await download_info.value
            
            # 임시 파일 생성 및 저장
            temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
            await download.save_as(temp_file.name)
            
            await browser.close()
            
            return temp_file.name
    
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
        