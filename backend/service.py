from llm import get_report

def generate_report(data: dict) -> str:
    country = data.get("country")
    selected_topics = data.get("selected_topics")
    urls = data.get("urls")
    if not country or not selected_topics:
        raise ValueError("Country and selected topics must be provided.")
    
    report = get_report(country, selected_topics, urls)
    print(report)
    return report
