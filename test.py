import streamlit as st
import matplotlib.pyplot as plt
from fpdf import FPDF
import base64
import numpy as np
from tempfile import NamedTemporaryFile

from sklearn.datasets import load_iris

def create_download_link(val, filename):
    b64 = base64.b64encode(val)  # val looks like b'...'
    return f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="{filename}.pdf">Download file</a>'


df = load_iris(as_frame=True)["data"]


figs = []

for col in df.columns:
    fig, ax = plt.subplots()
    ax.plot(df[col])
    st.pyplot(fig)
    figs.append(fig)

export_as_pdf = st.button("Export Report")

if export_as_pdf:
    pdf = FPDF()
    for fig in figs:
        pdf.add_page()
        with NamedTemporaryFile(delete=False, suffix=".png") as tmpfile:
                fig.savefig(tmpfile.name)
                pdf.image(tmpfile.name, 10, 10, 200, 100)
    html = create_download_link(pdf.output(dest="S").encode("latin-1"), "testfile")
    st.markdown(html, unsafe_allow_html=True)