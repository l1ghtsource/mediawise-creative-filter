import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt


def main():
    selectedPage = st.sidebar.selectbox("Выбрать страницу", ["Статистика", "Классификация"])

    if selectedPage == "Статистика":
        st.header("""Пример из приложения""")

        with st.form('1'):
            st.write('Динамика по отдельным категориям')
            selected_category = st.selectbox(
                "Выбрать категорию",
                (list(set(df_fulldata['Segment_num']))),
                key='selected_category'
            )
            submitted = st.form_submit_button("Submit")
            if submitted or selected_category:
                st.write(selected_category)
                bar_chart = alt.Chart(
                    df_fulldata[df_fulldata['Segment_num'] == selected_category]).mark_bar().encode(
                        x="Year:O",
                        y="sum(Segment_num):Q",
                        color="Segment_num:N"
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
                        color="Segment_num:N"
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
                            color="Segment_num:N"
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
                            color="Segment_num:N"
                        )
                    st.altair_chart(bar_chart, use_container_width=True)


    if selectedPage == "Классификация":
        st.header("""Классификация""")
        text = st.text_area(
            "Text to analyze",
            "",
            )
        uploaded_files = st.file_uploader("Choose a files", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("filename:", uploaded_file.name)
            st.write(bytes_data)
        upload_btn = st.button("обработать")
        if upload_btn:
            st.write("Предсказанный класс:" + st.session_state.classifier.predict(text))
        st.markdown("![Alt Text](https://media.giphy.com/media/vFKqnCdLPNOKc/giphy.gif)")


try:
    if st.session_state.first_load:
        pass
except:
    st.session_state.first_load = True
    df = pd.read_csv("dashboard_data.csv", delimiter=',')
    df['Estimated cost RUB'] = df['Estimated cost RUB'] / 1_000_000
    st.session_state.df_dashboard = df
    st.session_state.df_segments_data = pd.read_csv("train_segments.csv", delimiter=',')
    st.session_state.df_fulldata = pd.merge(st.session_state.df_dashboard, st.session_state.df_segments_data, on='Advertisement ID', how='outer')


df_dashboard = st.session_state.df_dashboard
df_segments_data = st.session_state.df_segments_data
df_fulldata = st.session_state.df_fulldata 
top10companies = df_dashboard.drop(columns=['Brand', 'Media Type', 'Year', 'Month', 'Advertisement ID']).groupby(['Advertiser'], as_index = False).agg({'Estimated cost RUB': 'sum'}).sort_values(by=['Estimated cost RUB'], ascending=False).head(10)['Advertiser']
main()