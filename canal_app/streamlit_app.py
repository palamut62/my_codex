"""Streamlit interface for canal quantity calculations."""
from __future__ import annotations

import datetime
import json

import streamlit as st

from .geometry import RectangularSection, TrapezoidalSection
from .utils import mm_to_m, section_to_dict, dict_to_yaml_json, draw_section


SECTION_MAP = {
    "Dik Kesit": RectangularSection,
    "Trapez Kesit (0+000-10+000)": TrapezoidalSection,
    "Trapez Kesit (10+000-13+650)": TrapezoidalSection,
    "Dar Trapez": TrapezoidalSection,
}

st.set_page_config(page_title="Kanal Metraj")
st.title("Ovacık Sulaması Kanal Metrajı")

section_type = st.selectbox("Kesit Tipi", list(SECTION_MAP.keys()))

b_mm = st.number_input("Taban Genişliği b (mm)", value=2000.0, step=100.0)
m_val = st.number_input("Yan Şev m (1:m)", value=0.0, step=0.1)
h_mm = st.number_input("Derinlik h (mm)", value=1500.0, step=100.0)
free_mm = st.number_input("Serbest Kote (mm)", value=200.0, step=50.0)
length_m = st.number_input("Kanal Uzunluğu (m)", value=10.0, step=1.0)

b = mm_to_m(b_mm)
h = mm_to_m(h_mm)
free = mm_to_m(free_mm)

SectionClass = SECTION_MAP[section_type]
section = SectionClass(bottom_width=b, depth=h, side_slope=m_val, freeboard=free)

results = section_to_dict(section, length_m)

st.subheader("Sonuçlar")
st.table({
    "Alan (m²)": [results["area_m2"]],
    "Kalıp Uzunluğu (m)": [results["formwork_m"]],
    "Beton Kaplama Alanı (m²)": [results["concrete_area_m2"]],
    "Beton Hacmi (m³)": [results["concrete_volume_m3"]],
})

st.subheader("YAML / JSON")
st.code(dict_to_yaml_json(results))

st.subheader("Kesit Çizimi")
img_buffer = draw_section(section)
st.image(img_buffer)

if st.button("PDF Metraj Raporu Oluştur"):
    st.success("Rapor oluşturma özelliği demo amaçlıdır.")

st.download_button(
    "CSV Kaydet",
    data="area,formwork,concrete_area,concrete_volume\n{area_m2},{formwork_m},{concrete_area_m2},{concrete_volume_m3}".format(**results),
    file_name="metraj.csv",
    mime="text/csv",
)

st.download_button(
    "JSON Kaydet",
    data=json.dumps(results, ensure_ascii=False, indent=2),
    file_name="metraj.json",
    mime="application/json",
)
