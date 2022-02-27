import re
import streamlit as st
import pandas as pd
import altair as alt

st.header("My First Streamlit App")

@st.cache
def load(url):
    return pd.read_json(url)

df = load("https://cdn.jsdelivr.net/npm/vega-datasets@2/data/penguins.json")
# st.write(df)

if(st.checkbox("Show Raw Data")):
    st.write(df)

with st.echo():
    scatter = alt.Chart(df).mark_point(
        tooltip=True
    ).encode(
        alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
        alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
        alt.Color("Species", scale=alt.Scale(domain=["Adelie", "Chinstrap", "Gentoo"], range=["orangered", "purple", "seagreen"]))
    )
st.write(scatter)
st.header("Slider")
min_weight = st.slider("Minimum Body Mass", 2500, 6500)
st.write(min_weight)

scatter_filtered = scatter.transform_filter(f"datum['Body Mass (g)'] >= {min_weight}")
st.write(scatter_filtered)

st.header("Selection")
# single selection 
# picked = alt.selection_single(on="mouseover", empty="none")
# mutiple selection 
# picked = alt.selection_multi()
# range selection 
# picked = alt.selection_interval(encodings=["x"])
# selection by field
# picked = alt.selection_single(on="mouseover", fields=["Species"])
# binding selectoin 
input_dropdown = alt.binding_select(options=["Adelie", "Chinstrap", "Gentoo"], name="Species")
picked = alt.selection_single(encodings=["color"], bind=input_dropdown)


scatter = alt.Chart(df).mark_circle(
    tooltip=True,
    size=100
).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    color = alt.condition(picked, "Species", alt.value("Lightgray"))
).add_selection(picked)

st.write(scatter)

st.header("Scales")
scatter = alt.Chart(df).mark_point(
    tooltip=True
).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species", scale=alt.Scale(domain=["Adelie", "Chinstrap", "Gentoo"], range=["orangered", "purple", "seagreen"]))
)

scales = alt.selection_interval(bind="scales")

st.write(scatter.add_selection(scales))
st.header("Interactive")
scatter = alt.Chart(df).mark_point(
    tooltip=True
).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species", scale=alt.Scale(domain=["Adelie", "Chinstrap", "Gentoo"], range=["orangered", "purple", "seagreen"]))
).interactive()
st.write(scatter)

st.header("Histogram")
brush = alt.selection_interval(encodings=["x"])

scatter = alt.Chart(df).mark_point(
    tooltip=True
).encode(
    alt.X("Flipper Length (mm)", scale=alt.Scale(zero=False)),
    alt.Y("Body Mass (g)", scale=alt.Scale(zero=False)),
    alt.Color("Species", scale=alt.Scale(domain=["Adelie", "Chinstrap", "Gentoo"], range=["orangered", "purple", "seagreen"]))
).add_selection(brush)

hist = alt.Chart(df).mark_bar().encode(
    alt.X("Body Mass (g)", bin=True),
    alt.Y("count()"),
    alt.Color("Species")
).transform_filter(brush)

st.write(scatter & hist)