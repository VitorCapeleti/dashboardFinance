import streamlit as st
def set_custom_theme():

    """
    Define e injeta CSS customizado no app Streamlit.
    Isso é usado para alterar a aparência de elementos que
    o Streamlit não permite customizar nativamente (ex: cores de filtros, cards).
    """

    card_bg_color = "#262730" 
    text_color = "#FAFAFA"
    green_color = "#e7f707"
    dark_text = "#1E1E1E"  
    
    css = f"""
    <style>

        [data-testid="stMultiSelect"] div[data-baseweb="select"] > div:first-child {{
            min-height: 100px !important;
            overflow-y: auto !important;
        }}
    
        .metric-card {{
            background-color: {card_bg_color};
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #444;
            box-shadow: 2px 2px 5px rgba(0,0,0,0.3);
            text-align: center;
            margin-bottom: 10px;
        }}

        .metric-card h3 {{
            margin: 0;
            font-size: 1.2rem;
            color: #AAA; /* Cinza claro */
            font-weight: normal;
        }}

        .metric-card h2 {{
            margin: 10px 0 0 0;
            font-size: 2rem;
            color: {text_color};
            font-weight: bold;
        }}

        .metric-card .delta {{
            font-size: 0.9rem;
            color: #4CAF50; /* Verde (padrão) */
            margin-top: 5px;
        }}

        [data-baseweb="tag"] {{
            background-color: {green_color} !important;
            color: {dark_text} !important;
            border-radius: 4px !important;
        }}
        
        [data-baseweb="tag"] svg {{
            color: {dark_text} !important;
        }}
        [data-baseweb="tag"] svg:hover {{
            color: #FF0000 !important; 
        }}
        
    </style>
    """
    
    st.markdown(css, unsafe_allow_html = True)