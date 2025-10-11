from utils.revex_capex_dashboard import create_expenditure_dashboard

create_expenditure_dashboard(
    page_title="Capital Expenditure Components",
    data_path="data/states_capex_components.csv",
    download_filename="cleaned_capex_component_data.csv",
    tab1_title="📊 Capital Expenditure Composition (%)",
    tab2_title="💰 Capital Expenditure Composition (Raw)",
    tab3_title="📈 Component Share by State (%)",
    tab4_title="📈 Component Share by State (Raw)"
)