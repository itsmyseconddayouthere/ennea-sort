import streamlit as st
import pandas as pd

if 'turn' not in st.session_state:
    st.session_state.turn = 0

def highlight(df):
    is_duplicate = df.duplicated(keep=False)
    return ['background-color: #f0f2f6' if trait else '' for trait in is_duplicate]

center_intelligence = pd.Series(['gut', 'heart', 'heart', 'heart', 'head', 'head', 'head', 'gut', 'gut'], index=['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'])
harmonic = pd.Series(['competency', 'positive-outlook', 'competency', 'reactive', 'competency', 'reactive', 'positive-outlook', 'reactive', 'positive-outlook'], index=['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'])
hornevian = pd.Series(['compliant', 'compliant', 'assertive', 'withdrawn', 'withdrawn', 'compliant', 'assertive', 'assertive', 'withdrawn'], index=['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'])
object_relations = pd.Series(['frustration', 'rejection', 'attachment', 'frustration', 'rejection', 'attachment', 'frustration', 'rejection', 'attachment'], index=['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'])
freudian = pd.Series(['superego', 'ego', 'ego', 'ego', 'superego', 'superego', 'ID', 'ID', 'ID'], index=['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'])
love = pd.Series(['admirative', 'compassionate', 'erotic', 'compassionate', 'admirative', 'admirative', 'erotic', 'erotic', 'compassionate'], index=['E1', 'E2', 'E3', 'E4', 'E5', 'E6', 'E7', 'E8', 'E9'])

grouped_center_intelligence = pd.DataFrame({'gut': ['E1', 'E8', 'E9'], 'heart': ['E2', 'E3', 'E4'], 'head': ['E5', 'E6', 'E7']})
grouped_harmonic = pd.DataFrame({'competency': ['E1', 'E3', 'E5'], 'positive-outlook': ['E2', 'E7', 'E9'], 'reactive': ['E4', 'E6', 'E8']})
grouped_hornevian = pd.DataFrame({'compliant': ['E1', 'E2', 'E6'], 'assertive': ['E3', 'E7', 'E8'], 'withdrawn': ['E4', 'E5', 'E9']})
grouped_object_relations = pd.DataFrame({'frustration': ['E1', 'E4', 'E7'], 'rejection': ['E2', 'E5', 'E8'], 'attachment': ['E3', 'E6', 'E9']})
grouped_freudian = pd.DataFrame({'superego': ['E1', 'E5', 'E6'], 'ego': ['E2', 'E3', 'E4'], 'ID': ['E7', 'E8', 'E9']})
grouped_love = pd.DataFrame({'admirative': ['E1', 'E5', 'E6'], 'compassionate': ['E2', 'E4', 'E9'], 'erotic': ['E3', 'E7', 'E8']})

all_triads = pd.DataFrame({'passional': center_intelligence,'harmonic': harmonic,'hornevian': hornevian,'object relations': object_relations,'freudian': freudian,'love': love})
grouped_triads = pd.concat({'passional': grouped_center_intelligence, 'harmonic': grouped_harmonic, 'hornevian': grouped_hornevian, 'object relations': grouped_object_relations, 'freudian': grouped_freudian, 'love': grouped_love}, axis=1)

types = all_triads.index.tolist()
triads = all_triads.columns.tolist()

table_triad = pd.DataFrame({'types': types,'triads': triads + ["", "", ""]}, index=["", "", "", "", "", "", "", "", ""])

st.title("enneagram trait sorter")
st.markdown( ":orange-badge[under construction️]" )
menu_options = {0: 'type and triad options', 1: 'type profiles', 2: 'triad info',  3: 'compare types',  4: 'filter by triads',  5: 'glossary'}

choice = st.selectbox("menu", options=list(menu_options.keys()), format_func=lambda x: menu_options[x])

if choice == 0:
    st.dataframe(table_triad, hide_index=True)

elif choice == 1:
    selected_type = st.selectbox("choose type", types)
    col1, col2 = st.columns(2)
    with col1:
        st.write(all_triads.loc[selected_type])
    with col2:
        st.write("")

elif choice == 2:
    selected_triad = st.selectbox("choose triad", triads)
    on_off = st.checkbox("all")
    if on_off:
        st.write(all_triads)
    elif not on_off:
        st.dataframe(grouped_triads[selected_triad], hide_index=True)

elif choice == 3:
    num_types = st.slider("choose # of types to compare", 2, 8)
    selected = []
    for i in range(num_types):
        type_select = st.selectbox(f"choose type {i+1}", types, key=f"compare_type_{i}")
        if type_select not in selected:
            selected.append(type_select)
    if selected:
        if len(selected) <= 1:
            st.write(all_triads.loc[selected])
        elif len(selected) > 1:
            st.write((all_triads.loc[selected]).style.apply(highlight))

elif choice == 4:
    exc_incl = st.checkbox("toggle exclusive/inclusive")
    selected_triads = st.multiselect("select triads to filter", triads)
    if exc_incl:
        if selected_triads:
            for triad in selected_triads:
                trait_val = all_triads[triad].unique().tolist()
                select_val = st.selectbox(f"which {triad.lower()} type?", trait_val, key=f"filter_{triad}")
                filtered = all_triads[all_triads[triad] == select_val]
                st.write(filtered[[triad]])
    elif not exc_incl:
        if selected_triads:
            filtered = all_triads.copy()
            for triad in selected_triads:
                trait_val = all_triads[triad].unique().tolist()
                select_val = st.selectbox(f"which {triad.lower()} type?", trait_val, key=f"filter_{triad}")
                filtered = filtered[filtered[triad] == select_val]
            st.write(filtered)


elif choice == 5:
    st.info("[ennealib.carrd.co](https://ennealib.carrd.co), [pdb wiki triads](https://wiki.personality-database.com/books/enneagram/chapter/triads) for further reading (actual section coming 🔜)")


