# KT Bizmeka 자동 로그인

1. 개요

    KT Bizmeka 자동 로그인을 위한 파이썬 자동화 프로그램입니다.
    실행 환경은 안정적인 `Chrome Browser` 버전 사용을 위하여 `LINUX` ('Rocky LINUX 9')에서의 사용을 전제로 합니다.

2. 설명

   KT Bizmeka 자동 로그인을 위하여 다음의 파일을 풀어서 사용합니다.

   * 브라우저 개발자 도구를 이용한 자동 출근

        브라우저의 개발자 도구를 열고, `console` 탭에서 `prt-auto_commute.js`의 내용을 복사 & 붙여넣기(`Ctrl` + `C` && `Ctrl` + `V`) <br>붙여넣어서 실행하기 전에 사용자의 `그룹웨어 ID`, `그룹웨어 PW`, `사용자 이름`과 텔레그램 BOT을 통해서 알릴 수 있도록 텔레그램 BOT의 `TELEGRAM BOT TOKEN값`, `TELEGRAM BOT CHAT ID`를 필히 수정하여 사용하여야 합니다.

   * 파이썬 프로그램을 이용한 자동 출근 (OS:LINUX)

     * `CRONTAB`을 이용한 프로그램 자동 실행
        사용자의 `CRONTAB`에 다음과 같이 등록

        ```
        # 매일 월(1)-금(5) 08:45분에 실행
        45 9 * * 1,2,3,4,5 export DISPLAY=:0 && /home/gouwon/venv/py_venv3.9/bin/python /home/gouwon/development/02.Project/001.Auto_Commute/prt-auto_commute.py prt-auto_commute.toml > /home/gouwon/auto_commute.log
        ```
     * SHELL SCRIPT 을 이용한 프로그램 실행

        ```
        source ./prt-auto_commute.sh
        ```
     * PYTHON SCRIPT 를 이용한 프로그램 실행

        ```
        /home/gouwon/venv/py_venv3.9/bin/python /home/gouwon/development/02.Project/001.Auto_Commute/prt-auto_commute.py prt-auto_commute.toml > /home/gouwon/auto_commute.log 2>&1
        ```

3. 필요 라이브러리 및 드라이버

   * 파이썬 버전
     * `Python3.9.16`

   * 필요 라이브러리
     * `selenium`
     * `toml`
     * `telegram`
     * `asynio`

   * 필요 드라이버
     * `google-chrome` : `116.0.5845.110`
     * `chromedriver` : `google-chrome` 버전에 맞춰서 다음의 사이트에서 다운로드 [chromedriver](https://sites.google.com/chromium.org/driver/downloads/version-selection)
