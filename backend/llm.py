from typing import List
from settings import DATA_DIR

import requests

from google import genai
from google.genai.types import (
    FunctionDeclaration,
    GenerateContentConfig,
    GoogleSearch,
    HarmBlockThreshold,
    HarmCategory,
    Part,
    SafetySetting,
    ThinkingConfig,
    Tool,
    ToolCodeExecution,
    Content
)


def get_report(country: str, selected_topics: List[str], urls: List[str]) -> str:

    def stream_data(iterator):
        buffer = ""
        for chunk in iterator:
            buffer += chunk.text
        return buffer

    
    client = genai.Client(api_key="AIzaSyDKiNNII-XOFMkQdJ3VQD61j8KgZEN-4xg")
    MODEL_ID = "gemini-2.5-flash-preview-04-17"

    # When unset -> dynamic thinking (default)
    # When set to 0 -> thinking is disabled.
    # When set to [1-32768] -> model uses the allocated thinking budget
    THINKING_BUDGET = 1024


    system_instruction = """
    You are a data specialist at the NGO "World Food Programme".
    Your mission is to write a detailed monthly report, following the structure of the previous monthly reports. Output format is HTML. ONLY HTML, no text before or after the HTML.

    Your highest priority is accuracy and a truthful report.
    """


    def crawl_website_data(href: str) -> str:
        """
        Call this method to retrieve the document from the website, if it interests you.

        Args:
            href: The href attribute from the link of the HTML
        """
        print(f"href: {href}")

        request = requests.get(href)
        if request.status_code == 200:
            return request.text

        raise Exception(f"Error: {request.status_code}")



    template_pdfs = [
        Part.from_bytes(
            data=(DATA_DIR / "syria-template-1.pdf").read_bytes(),
            mime_type="application/pdf",
        ),
        Part.from_bytes(
            data=(DATA_DIR / "example_templates/syria.html").read_bytes(),
            mime_type="text/html",
        ),
    ]

    data_urls = [
        "https://reliefweb.int/updates?list=Syrian%20Arab%20Republic%20%28Syria%29%20Updates&advanced-search=%28PC226%29",
        # "https://www.bbc.com/news/topics/cx1m7zg0w5zt",
    ]
    data_urls += urls

    data_pdfs = [
        Part.from_bytes(
        data=(DATA_DIR / "syria-data-1.pdf").read_bytes(),
        mime_type="application/pdf",
    ),
    ]

    data_csvs = [
    "<Syrian Arab Republic Energy.csv>",
    Part.from_bytes(
        data=(DATA_DIR / "Syrian Arab Republic_energy.csv").read_bytes(),
        mime_type="text/csv",
    ),
    "</Syrian Arab Republic Energy.csv>",
    ]

    contents = []
    contents.append(
    f"""<MISSION>
    Create a detailed monthly report for:
    <COUNTRY>{country}</COUNTRY>
    <DATE>2024-12</DATE>
    </MISSION>""")
    contents.append("<TEMPLATES>\nUse the following templates as a reference for your report. Follow the structure and style of the templates.")
    contents += template_pdfs
    contents.append("</TEMPLATES>")
    contents.append(f"Add the following sections to your report: {', '.join(selected_topics)}")
    contents.append("""<AVAILABLE DATA>""")
    contents.append(
    f"""<WEBSITE HREF>
    Use the following web pages. You must crawl links using the provided tool to retrieve more data
    {[f"<WEBSITE><URL>{x}</URL><HTML>{crawl_website_data(x)}</HTML></WEBSITE>" for x in data_urls]}
    </WEBSITE HREF>
    """)
    contents.append("<PDF FILES>\nUse the following PDF files as data sources for your report.")
    contents += data_pdfs
    contents.append("</PDF FILES>")

    contents.append("<CSV>\nUse the following CSV files as data sources for your report.")
    contents += data_csvs
    contents.append("</CSV")

    contents.append("""</AVAILABLE DATA>""")

    return stream_data(client.models.generate_content_stream(
        model=MODEL_ID,
        contents=contents,
        config=GenerateContentConfig(
            tools=[
                crawl_website_data,
            ],
            system_instruction=system_instruction,
            thinking_config=ThinkingConfig(
            thinking_budget=THINKING_BUDGET,
            ),
        ),
    ))

if __name__ == "__main__":
    print(get_report("Syria", ["HIGHLIGHTS", "economic_updates"]))
