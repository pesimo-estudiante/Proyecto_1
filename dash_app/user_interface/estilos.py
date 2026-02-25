COLORS = {
    "bg": "#efefef",
    "panel": "#f8f8f8",
    "border": "#222222",
    "text": "#111111",
    "primary": "#2c7fb8",
    "accent": "#d62728",
}

BASE_FONT = {"fontFamily": "Arial, sans-serif", "color": COLORS["text"]}

def box_style(width="100%", height=None, padding="16px", align="center"):
    style = {
        "border": f"2px solid {COLORS['border']}",
        "backgroundColor": COLORS["panel"],
        "padding": padding,
        "boxSizing": "border-box",
        "textAlign": align,
    }
    if width:
        style["width"] = width
    if height:
        style["height"] = height
    return style

def button_style():
    return {
        "border": f"2px solid {COLORS['border']}",
        "backgroundColor": "#ffffff",
        "padding": "20px 16px",
        "minHeight": "120px",
        "cursor": "pointer",
        "fontSize": "20px",
        "fontWeight": "500",
        "textAlign": "center",
        "display": "flex",
        "justifyContent": "center",
        "alignItems": "center",
        "whiteSpace": "normal",
    }

def small_button_style():
    return {
        "border": f"2px solid {COLORS['border']}",
        "backgroundColor": "#ffffff",
        "padding": "8px 12px",
        "cursor": "pointer",
        "fontSize": "14px",
        "marginRight": "8px",
    }