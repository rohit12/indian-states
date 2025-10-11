from utils.revex_capex_dashboard import create_expenditure_dashboard

create_expenditure_dashboard(
    page_title="Public Liability and Debt Components",
    data_path="data/states_public_liability_debt.csv",
    download_filename="cleaned_pld_component_data.csv",
    tab1_title="📊 Public Liability and Debt Composition (%)",
    tab2_title="💰 Public Liability and Debt Composition (Raw)",
    tab3_title="📈 Component Share by State (%)",
    tab4_title="📈 Component Share by State (Raw)"
)