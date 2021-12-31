import sys
from streamlit import cli as stcli

if __name__ == '__main__':
    # https://stackoverflow.com/questions/62760929/how-can-i-run-a-streamlit-app-from-within-a-python-script
    
    # 유통기한, 이미지 인식 추가 버전
    sys.argv = ["streamlit", "run", "view.py"]

    sys.exit(stcli.main())

#새로고침 1번 해야 페이지 정상 작동
