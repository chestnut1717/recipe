# 리사야 냉장고를 부탁해

## Description
- 냉장고의 남은 식재료들을 처리하기 위해 개발한 프로그램으로, 식재료를 입력하면 알맞는 음식을 추천해주는 서비스
- TF-IDF와 Cosine 유사도를 활용
- main branch는 레시피 추천 기능만 구현, expiration branch에서 유통기한 알림 기능을 추가적으로 구현함
- 🥇 광주형 인공지능 아이디어 공모전 수상작(우수상)

## Environment / Prerequisite
- Python == 3.8
- main branch 기준 requirements.txt를 실행하면 된다

## Files
- crawling.ipynb : 만개의 레시피에서 레시피 정보를 크롤링하여 db 구축
- data/db : 레시피 DB, 유통기한 DB 가 저장된 디렉토리
- main.py : 프로그램 실행 코드
- recipe_recom.py : 행렬 연산을 통한 레시피 추천 코드
- view.py : streamlit 라이브러리를 통한 간단한 웹어플리케이션 코드
- show_expiration : 유통기한 관리 코드(<b>expiration branch</b>에 구현)

## Usage
- 식재료를 입력하면 (comma(",")로 구분), 입력 재료에 기반하여 크롤링한 데이터(10,000여개)를 토대로 추천
![image](https://user-images.githubusercontent.com/62554639/147818177-7d5c6164-6891-4707-9da5-93567ddb3e10.png)  
- 링크를 클릭해서 상세 조리법 또한 검색할 수 있음
![image](https://user-images.githubusercontent.com/62554639/147818806-9e4e7261-c4ed-4080-94eb-8dc55290cfb9.png)  
- 또한 영수증 사진을 첨부하면 이미지 인식을 통해 추출한 식재료와 구매날짜를 사진 첨부날짜 기준으로 expiration.xlsx파일에 저장해 놓고, 유통기한 확인 버튼을 누르면 어떤 식재료가 유통기한이 임박했는지 출력해줌
![image](https://user-images.githubusercontent.com/62554639/147818770-34c2c75d-c020-4859-8369-54e55c3dc3a5.png)  

## Feedback / Complement
1. 식재료에 특화된 독자적인 이미지 인식 모델 개발 필요성 느낌
2. 제조일자가 아닌 구매일자와 비교하기 때문에 유통기한이 다소 차이가 있을 수 있음
3. DB 규모가 커질수록 벡터 생성 및 유사도 계산에 있어 속도 감소 우려 => Spark를 사용해보자
4. 재료의 종류 뿐만 아니라 양도 고려하면 남은 재료 관리에 더욱 효율적

