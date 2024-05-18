import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import altair as alt

def main1():
    page = st.sidebar.selectbox("Выбрать страницу", ["Тяжелые хвосты распределений", "Iris Dataset"])

    if page == "Тяжелые хвосты распределений":
        st.header("""Сгенерировать N случайных событий из распределения Фреше с функцией распределения:""")
        st.latex(r'''    
            F(x) = exp(-(\gamma x)^{-1/\gamma}1\{x>0\})
            ''')
        st.text("Для получения результата:")
        st.markdown("* Сгенерируем N нормально распределенных случайных величин $U_i$ [0,1] (нулевое среднее и единичная диспресия).")
        st.markdown("* Вычислим N cлучайных величин с распределением Фреше по формуле:")
        st.latex(r'''    
                    X_i=\dfrac{1}{\gamma}\left(-lnU_i)^{-\gamma}\right)
                ''')
        mu, sigma = 0, 1  # mean and standard deviation
        gamma = st.slider('Желаемая гамма', 0.25, 2.25, 0.5, 0.25)
        N = st.number_input("Желаемое N", 100, 10000, 10000)
        U = np.abs(np.random.normal(mu, sigma, N))
        X = 1 / gamma * (-np.log(U)) ** (-gamma)
        X2 = X[X < 20]
        fig, ax = plt.subplots()
        count, bins, ignored = plt.hist(X2, 100, density=True)
        plt.plot(bins,
                 np.exp(- (gamma * bins) ** (-1 / gamma)) * (1 / gamma) * (gamma * bins) ** (-1 / gamma - 1) * gamma,
                 linewidth=2, color='r')
        st.pyplot(fig)
        


def main():
    selectedPage = st.sidebar.selectbox("Выбрать страницу", ["Статистика", "Классификация"])

    if selectedPage == "Статистика":
        # energy_source = pd.DataFrame({
        #     "EnergyType": ["Electricity","Gasoline","Natural Gas","Electricity","Gasoline","Natural Gas","Electricity","Gasoline","Natural Gas"],
        #     "Price ($)":  [150,73,15,130,80,20,170,83,20],
        #     "Date": ["2022-1-23", "2022-1-30","2022-1-5","2022-2-21", "2022-2-1","2022-2-1","2022-3-1","2022-3-1","2022-3-1"]
        #     })
        
        # bar_chart = alt.Chart(energy_source).mark_bar().encode(
        #         x="month(Date):O",
        #         y="sum(Price ($)):Q",
        #         color="EnergyType:N"
        #     )
        # st.altair_chart(bar_chart, use_container_width=True)

        # Visualizing the data with stacked bar chart
        # plt.figure(figsize=[15, 9])
        # authors = ['Millisent Danielut', 'Deborah Tinn', 'Brendin Bracer',
        #    'Aurel Newvell']
        # python = [15, 21, 9, 25]
        # postgreSQL = [7, 5, 24, 11]
        # mongodb = [23, 17, 21, 15]

        # # Creating a DataFrame from a dictionary
        # blogs = pd.DataFrame({'Authors': authors, 'Python': python, 
        #                     'PostgreSQL': postgreSQL, 'Mongodb': mongodb})

        # # Set the width of the bars
        # wd = 0.4
        # x_pos = np.arange(len(blogs))

        # # Plotting the multiple bar graphs on top on other
        # plt.bar(x_pos, blogs.Python, color='r', width=wd, label='Python')
        # plt.bar(x_pos, blogs.PostgreSQL, color='y', width=wd, label='PostgeSQL', 
        #     bottom=blogs.Python)
        # plt.bar(x_pos, blogs.Mongodb, color='c', width=wd, label='Mongodb', 
        #     bottom=blogs.Python+blogs.PostgreSQL)

        # # Add xticks
        # plt.xticks(x_pos, blogs.Authors.values, fontsize=15)
        # plt.yticks(fontsize=15)
        # plt.title('The blogs posted by Authors', fontsize=20)
        # plt.xlabel('Authors', fontsize=17)
        # plt.ylabel('Blogs', fontsize=17)

        # plt.legend(loc='upper left', fontsize=15)
        # st.pyplot(plt)

        # with st.form('4'):
        #         st.write('Динамика по месяцам инвестиций')
        #         selected_brand1 = st.multiselect(
        #             "Выбрать бренды",
        #                 (list(set(df_fulldata['Brand']))),
        #                 placeholder="Select contact method...",
        #             )
        #         submitted = st.form_submit_button("Submit")
        #         if submitted and selected_category:
        #             bar_chart = alt.Chart(
        #                 df_fulldata[
        #                     df_dashboard['Advertiser'].isin(df_dashboard.drop(columns=['Brand', 'Media Type', 'Year', 'Month', 'Advertisement ID'])
        #                     .groupby(['Advertiser'], as_index = False).agg({'Estimated cost RUB': 'sum'})
        #                     .sort_values(by=['Estimated cost RUB'], ascending=False).head(10)['Advertiser'])]).mark_bar().encode(
        #                     x="Advertiser:O",
        #                     y="sum(Segment_num):Q",
        #                     color="Segment_num:N"
        #                 )
        #             st.altair_chart(bar_chart, use_container_width=True)

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
        st.header("""Классификация рынка""")
        st.write("будет скоро")
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