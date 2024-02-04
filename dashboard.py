import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import plotly.express as px
import statsmodels.formula.api as smf
import plotly.graph_objects as go

st.title("Projekt PAD s18803")

selected = option_menu(
    menu_title = None,
    options = ['Strona główna', 'Wykresy', 'Regresja'],
    icons=['house', 'book', 'envelope'],
    menu_icon='cast',
    default_index=0,
    orientation = 'horizontal'
)

cleandata_df = pd.read_csv("clean_data.csv", sep=",")
cleandata_df = cleandata_df.drop(cleandata_df.columns[0], axis=1)

if selected == 'Strona główna':
    st.subheader("Strona główna")
    st.dataframe(cleandata_df)

elif selected == 'Wykresy':
    st.subheader("Wykresy")

    columnlist = cleandata_df.columns.to_list()
    columnlist.remove("price")

    column = st.selectbox("Wybierz kolumnę:",columnlist)

    col1, col2, col3 = st.columns(3)

    fig1 = px.histogram(cleandata_df, column, title=f"Rozkład zmiennych dla {column}")
    col1.plotly_chart(fig1,use_container_width = True)

    fig2 = px.scatter(cleandata_df, column, "price", title=f"{column} vs price")
    col2.plotly_chart(fig2,use_container_width = True)

    price_comparison_df = cleandata_df[["price", column]]
    price_comparson_groups = price_comparison_df.groupby(["price", column]).size().unstack()
    fig3 = px.bar(price_comparson_groups, title=f"Zależność price od {column}")
    fig3.update_layout(legend_title=column)
    col2.plotly_chart(fig3,use_container_width = True)


elif selected == 'Regresja':
    st.subheader("Regresja")

    col1 = st.columns(1)

    myformula = "price ~ carat + x_dimension + y_dimension + z_dimension"

    model = smf.ols(formula=myformula, data=cleandata_df).fit()
    st.write(print(model.summary()))

    cleandata_df["fitted"] = model.fittedvalues

    fig_reg = px.scatter(cleandata_df, x="fitted", y="price", title=f"Regresja: Cena vs fitted")
    fig_reg.add_scatter(x=model.fittedvalues, y=model.fittedvalues, mode='lines', name='Regresja liniowa')
    st.plotly_chart(fig_reg, use_container_width=True)






