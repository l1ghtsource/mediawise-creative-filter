import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt
import requests
import os
import openpyxl
import tempfile

url = 'http://gnu.itatmisis.ru:8000/predict'
url_excel = 'http://gnu.itatmisis.ru:8000/predict_table'


def main():
    selectedPage = st.sidebar.selectbox("Выбрать страницу", ["Классификация", "Статистика"])

    if selectedPage == "Статистика":
        st.header("""Распределения данных""")

        with st.form('1'):
            st.write('Динамика по отдельным категориям')
            selected_category = st.selectbox(
                "Выбрать категорию",
                (list(set(df_fulldata['Segment_num_1']))),
                key='selected_category'
            )
            submitted = st.form_submit_button("Submit")
            if submitted or selected_category:
                st.write(selected_category)
                bar_chart = alt.Chart(
                    df_fulldata[df_fulldata['Segment_num_1'] == selected_category]).mark_bar().encode(
                        x="Year:O",
                        y="sum(Segment_num):Q",
                        color="Segment_num_1:N"
                    )
                st.altair_chart(bar_chart, use_container_width=True)

        with st.form('2'):
            st.write('Динамика по отдельным брендам')
            selected_brand = st.selectbox(
                "Выбрать категорию",
                (list(set(df_fulldata['Brand']))),
                key='selected_brand'
            )
            submitted1 = st.form_submit_button("Submit")
            if submitted1 or selected_brand:
                bar_chart = alt.Chart(
                    df_fulldata[
                        df_fulldata['Brand'] == selected_brand]).mark_bar().encode(
                        x="Year:O",
                        y="sum(Segment_num):Q",
                        color="Segment_num_1:N"
                    )
                st.altair_chart(bar_chart, use_container_width=True)
        
        selected_year = st.selectbox(
                "Выбрать год",
                (list(set(df_fulldata['Year']))),
                key='selected_year'
            )
        if selected_year:
            with st.form('3'):
                st.write('Динамика по месяцам TRP')
                selected_brand1 = st.multiselect(
                    "Выбрать бренды",
                        (list(set(df_fulldata['Brand']))),
                        key='selected_brands1'
                    )
                st.write(st.session_state.selected_brands1)
                submitted = st.form_submit_button("Submit")
                if submitted or len(selected_brand1):
                    bar_chart = alt.Chart(
                        df_fulldata[df_fulldata['Year'] == selected_year][df_fulldata['Brand'].isin(selected_brand1)]).mark_bar().encode(
                            x="Month:O",
                            y="sum(Segment_num):Q",
                            color="Segment_num_1:N"
                        )
                    st.altair_chart(bar_chart, use_container_width=True)

            with st.form('4'):
                st.write('Динамика по месяцам инвестиций')
                selected_brand2 = st.multiselect(
                    "Выбрать бренды",
                        (list(set(df_fulldata['Brand']))),
                        key='selected_brands2'
                    )
                submitted = st.form_submit_button("Submit")
                st.write(st.session_state.selected_brands2)
                if submitted or len(selected_brand2):
                    bar_chart = alt.Chart(
                        df_fulldata[df_fulldata['Year'] == selected_year][df_fulldata['Brand'].isin(selected_brand1)]).mark_bar().encode(
                            x="Month:O",
                            y="sum(Estimated cost RUB):Q",
                            color="Segment_num_1:N"
                        )
                    st.altair_chart(bar_chart, use_container_width=True)

    if selectedPage == "Классификация":
        st.header("""Классификация""")
        uploaded_excel_file = st.file_uploader("Загрузите excel файл", accept_multiple_files=False)
        upload_excel_btn = st.button("обработать excel")
        if upload_excel_btn and uploaded_excel_file:
            bytes_excel_data = uploaded_excel_file.read()
            predict = requests.post(url_excel, files={'file': (uploaded_excel_file.name, bytes_excel_data)})
            st.write(predict)
            output = open('test.xlsx', 'wb')
            output.write(predict.content)
            output.close()

            with open("test.xlsx", "rb") as file:
                btn_excel = st.download_button(
                        label="Скачать отчёт",
                        data=file,
                        file_name="test.xlsx",
                        mime='application/vnd.ms-excel'
                    )

        
        data_out = {}
        uploaded_files = st.file_uploader("Загрузите видео и аудио файлы", accept_multiple_files=True)
        video_url = st.text_input("url видео")
        upload_btn = st.button("обработать файлы")

        if upload_btn:
            for file in os.listdir():
                if file.endswith(".mp4"):
                    os.remove(file)
            for uploaded_file in uploaded_files:
                bytes_data = uploaded_file.read()
                predict = requests.post(url, files={'file': (uploaded_file.name, bytes_data)}).json()['result']
                # st.write(predict)
                # st.write('Великая магическая машина определила файл ' + f'"{uploaded_file.name}" ' + 'как: ' + predict)
                data_out[uploaded_file.name] = predict
            if video_url:
                if "youtube" in video_url:
                    import yt_dlp
                    ydl_opts = {
                        'ignoreerrors': True,
                        'outtmpl': '%(title)s.%(ext)s'
                    }
                    with yt_dlp.YoutubeDL(ydl_opts) as url_bin_f:
                        error_code = url_bin_f.download(video_url)
                if "rutube" in video_url:
                    pass

                if "vk" in video_url:
                    pass
                try:
                    for file in os.listdir():
                        if file.endswith(".mp4"):
                            predict = requests.post(url, files={'file': (file, open(file, 'rb'))}).json()['result']
                            data_out[file] = predict
                            # st.write(predict)
                            # if predict == None:
                            #     st.warning('Не удалось скачать видео')
                            # else:
                            #     st.write('великая машина определила файл' + f'{file}' + 'как:' + predict)
                except:
                    st.warning('Не удалось скачать видео')
            output_df = pd.DataFrame(list(data_out.items()), columns=['File', 'Category'])
            st.write(output_df)
            with tempfile.TemporaryDirectory() as tmp:
                path = os.path.join(tmp, 'output.xlsx')
                output_df.to_excel(path, engine="openpyxl", index=False)
                with open(path, 'rb') as file:
                    download = st.download_button(
                        label="Download data as Excel",
                        data=file,
                        file_name='output.xlsx',
                        mime='application/vnd.ms-excel'
                    )
        st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")


try:
    if st.session_state.first_load:
        pass
except:
    id2label = {0: 'Промо/Нет/Нет',
            1: 'Имидж/Нет/Нет',
            2: 'Имидж/Нет/Да',
            3: 'Промо/Доставка/Нет',
            4: 'Промо/Нет/Да',
            5: 'Имидж/Доставка/Нет',
            6: 'Промо/Нет/Нет',
            7: 'Имидж',
            8: 'Кредитование',
            9: 'Range',
            10: 'Дебетовые карты',
            11: 'Услуги бизнесу',
            12: 'Кредитные карты',
            13: 'Инвестиционные продукты',
            14: 'Экосистемные сервисы',
            15: 'Музыка',
            16: 'Колонки+Голосовой помощник',
            17: 'Клипы',
            18: 'Соц сети'}
    st.session_state.first_load = True
    df = pd.read_csv("dashboard_data.csv", delimiter=',')
    df['Estimated cost RUB'] = df['Estimated cost RUB'] / 1_000_000
    st.session_state.df_dashboard = df
    st.session_state.df_segments_data = pd.read_csv("train_segments.csv", delimiter=',')
    st.session_state.df_fulldata = pd.merge(st.session_state.df_dashboard, st.session_state.df_segments_data, on='Advertisement ID', how='outer')
    st.session_state.df_fulldata['Segment_num_1'] = st.session_state.df_fulldata['Segment_num'].map(id2label)

df_dashboard = st.session_state.df_dashboard
df_segments_data = st.session_state.df_segments_data
df_fulldata = st.session_state.df_fulldata
top10companies = df_dashboard.drop(columns=['Brand', 'Media Type', 'Year', 'Month', 'Advertisement ID']).groupby(['Advertiser'], as_index = False).agg({'Estimated cost RUB': 'sum'}).sort_values(by=['Estimated cost RUB'], ascending=False).head(10)['Advertiser']
main()