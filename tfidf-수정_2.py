# -*- coding: utf-8 -*-

from os import name
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def tfidf_make(df):
    
    # 1글자 재료도 인식할 수 있도록 처리
    tfidf = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    tfidf_matrix = tfidf.fit_transform(df['재료'])
    return tfidf_matrix

def get_recommendations(a, title, df):
    
    df = df.append({'이름' : '메뉴', '재료': a}, ignore_index=True)

    # TF-IDF matrix 생성
    tfidf_matrix = tfidf_make(df)

    # Cosine Similarity matrix 생성
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    
    # title과 비교할 cosine 유사도 계산
    indices = pd.Series(df.index, index=df['이름']).drop_duplicates()
    idx = indices[title]

    # 코사인 유사도 큰 수별로 순위 매기기
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 상위 10개 추출(자신 제외)
    sim_scores = sim_scores[1:11]
    
    movie_indices = [i[0] for i in sim_scores]
    scores = [i[1] for i in sim_scores]
    
    result = df.iloc[movie_indices].reset_index(drop = True)

    # 겹치는 재료 변환
    menu = [res.split(',') for res in result['재료']]
    my_ingredient = [i.strip() for i in a.split(',')]
    intersect_ingre = show_ingredients(my_ingredient, menu)
    result = pd.concat([result, intersect_ingre], axis = 1)
        
    return result

# 입력 재료와 추천 레시피의 재료 중, 공통된 재료들을 시리즈로 반환
def show_ingredients(my, menu):
    tmp = []
    for m in menu:
        intersect_ingre = list(set(my).intersection(m))
        if len(intersect_ingre) == 0:
            tmp.append(['--겹치는 재료 없음--'])
        
        tmp.append(intersect_ingre)
    
    intersects = pd.Series(tmp, name = '겹치는 재료')
    return intersects



path = '.\\data\\db\\recipe_final.xlsx'
df = pd.read_excel(path)
ingredients = df['재료'].apply(lambda x : x.split(','))


if __name__ == '__main__':

    # 입력 받을 때, 무조건 콤마(,) 단위로 split한다 (ex. '새송이버섯, 가지, 고추장, 김치, 참치, 마요네즈')
    input_ingredient = input('재료를 입력하세요 : ')
    result = get_recommendations(input_ingredient, '메뉴', df)
    print(result)




