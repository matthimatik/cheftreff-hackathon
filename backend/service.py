def generate_report(data: dict) -> str:
    report_content = f"Report Data: {str(data)}"
    return report_content

def generate_report_for_country(data: dict) -> str:
    country = data.get("country")
    selected_topics = data.get("selected_topics")
    if not country or not selected_topics:
        raise ValueError("Country and selected topics must be provided.")
    
    # create html report content
    report_content = f"<h1>Report for {country}</h1>"
    report_content += "<ul>"
    for topic in selected_topics:
        report_content += f"<li>{topic}</li>"
    report_content += "</ul>"
    return report_content
