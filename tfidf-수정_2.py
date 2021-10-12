# -*- coding: utf-8 -*-

from os import name
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

def tfidf_make(df):
    
    # 1글자 재료도 인식할 수 있도록 처리
    tfidf = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    tfidf_matrix = tfidf.fit_transform(df['재료'])
    return tfidf_matrix

# 원 방정식
def scaled_score(score):
    return round(((2 * score) - (score)**2) ** 0.5 , 4) * 100

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
    top_scores = sim_scores[1:11]
    
    movie_indices = [i[0] for i in top_scores]
    scores = pd.Series([scaled_score(i[1]) for i in top_scores], name='점수')
    
    result = df.iloc[movie_indices].reset_index(drop = True)

    # 겹치는 재료 변환
    menu = [res.split(',') for res in result['재료']]
    my_ingredient = [i.strip() for i in a.split(',')]
    intersect_ingre = show_ingredients(my_ingredient, menu)
    result = pd.concat([result, intersect_ingre], axis = 1)
    result = pd.concat([result, scores], axis = 1)

    return result

# 입력 재료와 추천 레시피의 재료 중, 공통된 재료들을 시리즈로 반환
def show_ingredients(my, menu):
    tmp = []
    for m in menu:
        intersect_ingre = ','.join(list(set(my).intersection(m)))
        if len(intersect_ingre) == 0:
            tmp.append('--겹치는 재료 없음--')
        else:
            tmp.append(intersect_ingre)
    
    intersects = pd.Series(tmp, name = '겹치는 재료')
    return intersects

# 상위 5개 선택 가능
def graph_show(df):
    
    # bar 너비 번경
    def change_width(ax, new_value) :
        for patch in ax.patches :
            current_width = patch.get_width()
            diff = current_width - new_value

            patch.set_width(new_value)

            patch.set_x(patch.get_x() + diff * .5)

    fig, ax = plt.subplots()
    sns.barplot(data=df[:3], x = '이름', y='점수', ax=ax, palette='Reds_r')
    rank = ['1st', '2nd', '3rd']

    change_width(ax, .3)
    ax.set_xticklabels(rank)
    # y 범위 설정
    min_val = min(df['점수'][:3]) - 5
    max_val = min(max(df['점수'][:3]), 100.0)
    ax.set(ylim=(min_val, max_val))
    # 세부설정(색깔, 투명도)
    
    ax.set_xlabel('Rank')
    ax.set_ylabel('Score')
    ax.patch.set_alpha(0.1)
    ax.spines['bottom'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.xaxis.label.set_color('white')
    ax.yaxis.label.set_color('white')

    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')

    plt.grid(linewidth=0.4)
    
    plt.show()



path = '.\\data\\db\\recipe_final.xlsx'
df = pd.read_excel(path)
ingredients = df['재료'].apply(lambda x : x.split(','))


if __name__ == '__main__':

    # 입력 받을 때, 무조건 콤마(,) 단위로 split한다 (ex. '새송이버섯, 가지, 고추장, 김치, 참치, 마요네즈')
    input_ingredient = input('재료를 입력하세요 : ')
    result = get_recommendations(input_ingredient, '메뉴', df)
    print(result)
    graph_show(result)




