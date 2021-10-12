import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
np.random.seed(seed=0)

st.set_page_config(page_title="리사야 냉장고를 부탁해", page_icon="🍎", layout="wide")
st.set_option('deprecation.showPyplotGlobalUse', False)

# row1.config
row1_spacer1, row1_2, row1_spacer2 = st.columns(
    (3,4,3)
    )


# row2.config
row2_spacer1, row2_1, row2_spacer2, row2_2, row2_spacer3,row2_3 = st.columns(
    (.4, 1.6, .1, 1.6, .1, .4)
    )
row3_spacer1, row3_1, row3_spacer2, row3_2, row3_spacer3 = st.columns(
    (.4, 1.6, .1, 1.6, .1)
    )
# load data
path = 'data\\db\\recipe_final.xlsx'
df = pd.read_excel(path)

# tf-idf

def scaled_score(score):
    return round(((2 * score) - (score)**2) ** 0.5 , 4) * 100

def tfidf_make(df):
    # 1글자 재료도 인식할 수 있도록 처리
    tfidf = TfidfVectorizer(token_pattern=r"(?u)\b\w+\b")
    tfidf_matrix = tfidf.fit_transform(df['재료'])
    return tfidf_matrix


def show_ingredients(my, menu):
    tmp = []
    for m in menu:
        intersect_ingre = ','.join(list(set(my).intersection(m)))
        if len(intersect_ingre) == 0:
            tmp.append('--겹치는 재료 없음--')
        else:
            tmp.append(intersect_ingre)

    intersects = pd.Series(tmp, name='겹치는 재료')
    return intersects


def get_recommendations(a, title, df):
    df = df.append({'이름': '메뉴', '재료': a}, ignore_index=True)

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

    result = df.iloc[movie_indices].reset_index(drop=True)

    # 겹치는 재료 변환
    menu = [res.split(',') for res in result['재료']]
    my_ingredient = [i.strip() for i in a.split(',')]
    intersect_ingre = show_ingredients(my_ingredient, menu)
    result = pd.concat([result, intersect_ingre], axis=1)
    result = pd.concat([result, scores], axis=1)

    return result


with row1_2:
    st.write("""# 👩‍🍳리사야 냉장고를 부탁해""")
    st.write(' ')
    st.write(' ')
    input_ingredient = st.text_input('재료를 입력해 주세요           🦐🥕🌽🧅🦀')
    output_df = get_recommendations(input_ingredient, '메뉴',df)
    output_df = output_df.reset_index()
    output_df = output_df.drop(['index'],axis = 1)
    output_df = output_df[:3]
ingredients = df['재료'].apply(lambda x : x.split(','))
# set row2
with row2_1:
    menu = [menu for menu in output_df['이름']]
    st.header('🧾Recipe')
    for i in range(3):
        for index, j in zip(['요리 이름', '재료', '겹치는 재료'], range(0, 3)):
            if j == 2:
                j = -2
            if index == '요리 이름':
                st.write(f'#### {i+1}.  ',output_df.iloc[i,j])
            else:
                st.write(f"{index}  :  ", output_df.iloc[i, j])
    # st.dataframe(output_df[['이름', '재료','겹치는 재료']])
with row2_2:
    st.header('🗸 Recipe Choice')
    name = st.selectbox('',menu)
    image_url = output_df[output_df['이름'] == name].iloc[0, -4]
    st.image(image_url, width=250,use_column_width = 'auto')
    recipe_url = output_df[output_df['이름'] == name].iloc[0, -3]
    st.write("조리법 주소")
    st.write(recipe_url)