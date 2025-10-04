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

# Map state -> initials
state_to_initial = dict(zip(indian_states, indian_state_initials))

# Color mapping (unique & consistent across pages)
color_list = pc.qualitative.Alphabet + pc.qualitative.Dark24
state_colors = {state: color_list[i % len(color_list)] for i, state in enumerate(indian_states)}