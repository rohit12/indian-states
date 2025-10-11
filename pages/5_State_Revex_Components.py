from utils.revex_capex_dashboard import create_expenditure_dashboard

create_expenditure_dashboard(
    page_title="Revenue Expenditure Components",
    data_path="data/states_revex_components.csv",
    download_filename="cleaned_revex_component_data.csv",
    tab1_title="📊 Revenue Expenditure Composition (%)",
    tab2_title="💰 Revenue Expenditure Composition (Raw)",
    tab3_title="📈 Component Share by State (%)",
    tab4_title="📈 Component Share by State (Raw)"
)