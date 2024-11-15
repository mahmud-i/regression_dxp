import json as j
import os

css_content = """
        body { 
            font-family: Arial, sans-serif; 
            background-color: #f4f4f9; 
            color: #333; 
        }

        #report-container {
            width: 90%;
            margin: auto;
    	}

        h1 { 
            text-align: center; 
            color: #444; 
        }

        .acc, .acc-alt { 
            cursor: pointer;
            color: black; 
            padding: 10px; 
            border: 1px solid #ddd; 
            width: 100%; 
            text-align: left; 
            font-size: 14px; 
            font-weight: bold;
            transition: background-color 0.3s; 
            display: flex;
            justify-content: space-between;
        }

        .acc { background-color: #D0D0D0; }
        .acc-alt { background-color: #EDEDED; }

        .active, .acc:hover, .acc-alt:hover { 
            color: white;
            background-color: #0056b3; 
        }
        
        
        .acc_Pass {
            cursor: pointer;
            padding: 3px;
            margin-top: 5px;
            border: o.5px solid #f4f4f4; 
            width: 80%; 
            text-align: left; 
            font-size: 14px; 
            transition: background-color 0.3s; 
            display: flex;
            justify-content: space-between;
            color: green;
            font-weight: bold;
        } 
        
        .acc_Fail { 
            cursor: pointer;
            padding: 3px;
            margin-top: 5px;
            border: o.5px solid #f4f4f4; 
            width: 80%; 
            text-align: left; 
            font-size: 14px; 
            transition: background-color 0.3s; 
            display: flex;
            justify-content: space-between;
            color: red;
            font-weight: bold;
        } 
        
        .active_Fail  { 
            border: 1px solid #ddd; 
            border-bottom: none;
            color: white;
            background-color: red; 
        }
        
        .acc_Fail:hover { 
            border: 1px solid #ddd; 
            color: white;
            background-color: red;
        }
        
        .active_Pass  { 
            border: 1px solid #ddd; 
            border-bottom: none;
            color: white;
            background-color: green; 
        }
        
        .acc_Pass:hover { 
            border: 1px solid #ddd; 
            color: white;
            background-color: green;
        }
        
        .toggle-sign {
            font-size: 16px;
            font-weight: bold;
            text-align: right;
            padding-right: 8px;
        }
        
        .panel { 
            padding: 10px; 
            display: None; 
            width: 100%; 
            background-color: white; 
            overflow: hidden; 
            border: 1px solid #ddd; 
            border-top: none;
            font-size: 14px;  
        }

        ul, ol { 
            margin: 0 0 10px 20px; 
        }

        li { 
            margin-bottom: 5px; 
        }

        strong { 
            color: #555; 
        }

        """

def create_css_file(report_dir):
    """Create a CSS file for styling the HTML report if it doesn't already exist."""
    css_path = os.path.join(report_dir, "style.css")
    if not os.path.exists(css_path):
        css = css_content
        with open(css_path, 'w', encoding='utf-8') as f:
            f.write(css)

def json_to_html(json_data, indent=0):
    """Convert JSON data to HTML format recursively with accordions."""
    html_content = ""

    if isinstance(json_data, dict):
        html_content += "<ul>\n"
        for key, value in json_data.items():
            if key == "Passed_Result":
                html_content += f"""
                <li><div id ="accordion" class = "acc_Pass" onclick="togglePass(this)">
                    <span>{key}</span>
                    <span class="toggle-sign">+</span>
                </div>
                <div class="panel">
                    {json_to_html(value, indent + 1)}
                </div></li>
                """
            elif key == "Failed_Result":
                html_content += f"""
                <li><div id ="accordion" class = "acc_Fail" onclick="toggleFail(this)">
                    <span>{key}</span>
                    <span class="toggle-sign">+</span>
                </div>
                <div class="panel">
                    {json_to_html(value, indent + 1)}
                </div></li>
                """
            else:
                html_content += f"<li><strong>{key}</strong>: {json_to_html(value, indent + 1)}</li>\n"
        html_content += "</ul>\n"

    elif isinstance(json_data, list):
        html_content += "<ol>\n"
        for item in json_data:
            html_content += f"<li>{json_to_html(item, indent + 1)}</li>\n"
        html_content += "</ol>\n"

    else:
        html_content += f"{str(json_data)}"

    return html_content


def generate_html_report(json_file_path):
    """Generate an HTML report from a JSON file with accordions, saving it in a new 'html_report' folder."""
    # Load the JSON data
    with open(json_file_path, 'r', encoding='utf-8') as f:
        data = j.load(f)

    # Create the 'html_report' folder in the same directory as the JSON file
    json_dir = os.path.dirname(json_file_path)
    json_filename = os.path.splitext(os.path.basename(json_file_path))[0]
    report_dir = os.path.join(json_dir, f'{json_filename}_html_report')
    os.makedirs(report_dir, exist_ok=True)

    # Create the CSS file if it doesn't already exist
    #create_css_file(report_dir)

    # Set the HTML report file name based on the JSON file name
    output_html_path = os.path.join(report_dir, f"{json_filename}.html")

    # HTML structure with accordions
    html_content = f"""
    <html>
    <head>
        <title>{json_filename}</title>
        <style>
            {css_content}
        </style>
    </head>
    <body>
        <div id="report-container">
        <h1>{json_filename}</h1>
    """

    for i, (section_key, section_value) in enumerate(data.items(), start=1):
        row_class = "acc-alt" if i % 2 == 0 else "acc"
        html_content += f"""
        <div class={row_class} id ="accordion" onclick="toggleAccordion(this)">
                <span class="row-data">{i}. {section_key}</span>
                <span class="toggle-sign">+</span>
        </div>
        <div class="panel">
            {json_to_html(section_value)}
        </div>
        """

    html_content += """
        <script>
            function toggleAccordion(element) {
                // Toggle the active class on the clicked accordion
                element.classList.toggle("active");
            
                // Get the associated panel, which is the next sibling element
                var panel = element.nextElementSibling;
            
                // Check if the panel is currently displayed
                if (panel.style.display === "block") {
                    panel.style.display = "none"; // Hide the panel
                    element.querySelector(".toggle-sign").textContent = "+"; // Set toggle sign to +
                } else {
                    panel.style.display = "block"; // Show the panel
                    element.querySelector(".toggle-sign").textContent = "-"; // Set toggle sign to -
                }
            }
            
            function togglePass(element) {
                // Toggle the active class on the clicked accordion
                element.classList.toggle("active_Pass");
            
                // Get the associated panel, which is the next sibling element
                var panel = element.nextElementSibling;
            
                // Check if the panel is currently displayed
                if (panel.style.display === "block") {
                    panel.style.display = "none"; // Hide the panel
                    element.querySelector(".toggle-sign").textContent = "+"; // Set toggle sign to +
                } else {
                    panel.style.display = "block"; // Show the panel
                    element.querySelector(".toggle-sign").textContent = "-"; // Set toggle sign to -
                }
            }
            
            function toggleFail(element) {
                // Toggle the active class on the clicked accordion
                element.classList.toggle("active_Fail");
            
                // Get the associated panel, which is the next sibling element
                var panel = element.nextElementSibling;
            
                // Check if the panel is currently displayed
                if (panel.style.display === "block") {
                    panel.style.display = "none"; // Hide the panel
                    element.querySelector(".toggle-sign").textContent = "+"; // Set toggle sign to +
                } else {
                    panel.style.display = "block"; // Show the panel
                    element.querySelector(".toggle-sign").textContent = "-"; // Set toggle sign to -
                }
            }
            
            // Automatically set up all accordions on page load
            document.addEventListener("DOMContentLoaded", function() {
                var accordions = document.querySelectorAll("#accordion");
                accordions.forEach(function(accordion) {
                    // Initially set all panels to hidden
                    var panel = accordion.nextElementSibling;
                    if (panel) panel.style.display = "none";
                });
            });
            
        </script>
    </div>
    </body>
    </html>
    """

    # Write the HTML content to the output file
    with open(output_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"HTML report generated at {output_html_path}")
