import plotly.colors as pc

indian_states = [
    "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chhattisgarh", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jharkhand",
    "Karnataka", "Kerala", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Punjab", "Rajasthan", 
    "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"
]

indian_state_initials = [
    "AP", "AR", "AS", "BR", "CG", "GA", "GJ", "HR", "HP", "JH",
    "KA", "KL", "MP", "MH", "MN", "ML", "MZ", "NL", "OR", "PB",
    "RJ", "SK", "TN", "TS", "TR", "UP", "UK", "WB"
]

state_colors1 = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd",
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf",
    "#aec7e8", "#ffbb78", "#98df8a", "#ff9896", "#c5b0d5",
    "#c49c94", "#f7b6d2", "#c7c7c7", "#dbdb8d", "#9edae5",
    "#393b79", "#637939", "#8c6d31", "#843c39", "#7b4173",
    "#17becf", "#b5cf6b", "#e7ba52"
]

# Map state -> initials
state_to_initial = dict(zip(indian_states, indian_state_initials))

# Color mapping (unique & consistent across pages)
color_list = pc.qualitative.Alphabet + pc.qualitative.Dark24
state_colors = {state: color_list[i % len(color_list)] for i, state in enumerate(indian_states)}