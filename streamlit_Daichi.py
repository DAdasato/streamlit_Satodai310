import streamlit as st
from PIL import Image
import requests
from io import BytesIO

def recommend_meal(calorie):
    if calorie < 1500:
        return "消費カロリーが低いため、バランスの取れた食事を心掛けよう。例えば、筑前煮など１食400kcal程度の食事がおすすめ!", "https://assets.st-note.com/production/uploads/images/28963188/picture_pc_e1df18e1d01c2ebfa4de4348ea92b9b5.jpg?width=800" 
    if 1500 <= calorie < 2000:
        return "消費カロリーに合わせて、野菜、たんぱく質、炭水化物をバランスよく摂取することが大切。例えば、鶏もも肉のソテーなどの１食600kcal程度の食事がおすすめ!", "https://www.marukome.co.jp/recipe/special/eiyoshi/img/menu/img_menu01.png?tm=1654071308"
    else:
        return "アスリート並みの消費カロリーのため、たんぱく質と炭水化物をしっかり取ろう。例えば、高カロリーの食事で、１食800kcal程度の食事がおすすめ！", "https://athtrition.com/wp/wp-content/uploads/2017/01/IMG_9944s.jpg"

def calculate_calorie(gender, age, weight, height, activity_level):
    if gender == "男性":
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    if activity_level == 1:
        calorie = bmr * 1.2
    elif activity_level == 2:
        calorie = bmr * 1.375
    elif activity_level == 3:
        calorie = bmr * 1.55
    elif activity_level == 4:
        calorie = bmr * 1.725
    else:
        return "適切な選択肢を入力してください"

    return calorie

def main():
    st.title('1日消費カロリーメーター')
    st.write('一日の消費カロリーを知って、食事や運動に生かそう！')
    st.write('※これはあくまでも目安です。これを指標として、日々の運動と食事を意識しましょう！')

    gender = st.selectbox("性別を選択してください", ["男性", "女性"])
    age = st.number_input("年齢を入力してください", min_value=0, max_value=150, value=30)
    weight = st.number_input("体重(kg)を入力してください", min_value=0.0, max_value=300.0, value=60.0)
    height = st.number_input("身長(cm)を入力してください", min_value=0.0, max_value=300.0, value=170.0)
    activity_level = st.selectbox("身体レベルを選んでください",["ほとんど運動しない", "軽い運動", "運動量が普通", "運動量が高い"])

    if st.button("計算"):
        if activity_level == "ほとんど運動しない":
            activity_level = 1
        elif activity_level == "軽い運動":
            activity_level = 2
        elif activity_level == "運動量が普通":
            activity_level = 3
        elif activity_level == "運動量が高い":
            activity_level = 4

        calorie = calculate_calorie(gender, age, weight, height / 100, activity_level)
        st.write(f"あなたの消費カロリーは {calorie:.2f} kcalです。")
        
        meal_recommendation, meal_image_url = recommend_meal(calorie)
        
        st.write("おすすめの食事:")
        st.write(meal_recommendation)
        meal_image = Image.open(BytesIO(requests.get(meal_image_url).content))
        st.image(meal_image, caption='おすすめの食事', use_column_width=True)

        if calorie > 2500:
            overeat_text = "消費カロリーが基準を超えています。適切な摂取量を意識しましょう。"
            overeat_url = "https://nosh.jp/magazine/health/3070/"

            st.write("食べ過ぎ対処法:")
            st.write(overeat_text)
            st.write(overeat_url)

            overeat_image = Image.open(BytesIO(requests.get(overeat_url).content))
            st.image(overeat_image, caption='食べ過ぎ対処法', use_column_width=True)

if __name__ == "__main__":
    main()
