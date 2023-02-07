def streamlit_theme_alt():
    font = "Helvetica"
    primary_color = "#bf0838" # #F63366 Bright pink
    font_color = "#262730"  # dark grey
    grey_color = "#f0f2f6"
    lightgrey_color = "#f6f2f6"
    black= '#201e1f'
    darkGray= '#a6a6a6'
    gray= '#eaeaea'
    lightGray= '#f0f0f0'
    white= '#ffffff'
    green= '#64CB29'
    blue= '#2d9ee0'
    rose= '#f45b69'
    cerise= '#f00faa'
    red= '#ed6a5a'
    orange= '#edae49'
    yellow= '#e4ce44'
    lightRed= '#cc998d'
    darkPurple= '#303965'
    base_size = 14
    lg_font = base_size * 1.15
    sm_font = base_size * 0.8  # st.table size
    xl_font = base_size * 1.5

    config = {
        "config": {
            "view": {"fill": lightGray},
            "arc": {"fill": primary_color},
            "area": {"fill": primary_color},
            "circle": {"fill": primary_color, "stroke": font_color, "strokeWidth": 0.5},
            "line": {"stroke": primary_color},
            "path": {"stroke": primary_color},
            "point": {"stroke": primary_color},
            "rect": {"fill": primary_color},
            "shape": {"stroke": primary_color},
            "symbol": {"fill": primary_color},
            "title": {
                "font": font,
                "color": font_color,
                "fontSize": lg_font,
                "anchor": "start",
            },
            "axis": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
                "grid": True,
                "gridColor": "#fff",
                "gridOpacity": 1,
                "domain": True, # False
                "domainColor": lightGray,
                "tickColor": font_color,
            },
            "header": {
                "labelFont": font,
                "titleFont": font,
                "labelFontSize": base_size,
                "titleFontSize": base_size,
            },
            "legend": {
                "titleFont": font,
                "titleColor": font_color,
                "titleFontSize": sm_font,
                "labelFont": font,
                "labelColor": font_color,
                "labelFontSize": sm_font,
            },
            "range": {
                #"category": ["#f63366", "#fffd80", "#0068c9", "#ff2b2b", "#09ab3b"],
                "category": [ "#f63366", "#0068c9", "#fffd80", "#7c61b0", "#ffd37b", "#ae5897", "#ffa774","#d44a7e", "#fd756d",'#f00faa'], # =category_large
                "diverging": [
                    "#850018",
                    "#cd1549",
                    "#f6618d",
                    "#fbafc4",
                    "#f5f5f5",
                    "#93c5fe",
                    "#5091e6",
                    "#1d5ebd",
                    "#002f84",
                ],
                "heatmap": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ramp": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
                "ordinal": [
                    "#ffb5d4",
                    "#ff97b8",
                    "#ff7499",
                    "#fc4c78",
                    "#ec245f",
                    "#d2004b",
                    "#b10034",
                    "#91001f",
                    "#720008",
                ],
            },
        }
    }
    return config

    
