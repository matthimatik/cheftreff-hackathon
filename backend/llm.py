from typing import List
from urllib import response

from aggregate_pandas import aggregate_dataframe
from crawl.arbitrary_source import url_encode_model
from cite_manager import CiteManager
from settings import DATA_DIR

import requests
from crawl.reliefweb import get_reliefweb_data
import re
import pandas as pd


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

BACKSLASH = "\n"



def stream_data(iterator):
    buffer = ""
    for chunk in iterator:
        buffer += chunk.text
        print(chunk.text, end="")
    return buffer


def get_report(country: str, selected_topics: List[str], urls: List[str]) -> str:
    cite_manager = CiteManager()

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
    Relate statistics and numbers to claims you make. Use the data provided in the <AVAILABLE DATA> section to support your claims.
    """

    relief_data = get_reliefweb_data(226, 2024, 12)  # syria, year, month

    template_pdfs = [
        Part.from_bytes(
            data=(DATA_DIR / "syria-template-1.pdf").read_bytes(),
            mime_type="application/pdf",
        ),
        Part.from_bytes(
            data=(DATA_DIR / "example_templates/syria.html").read_bytes(),
            mime_type="text/html",
        ),
        Part.from_bytes(
            data=(DATA_DIR / "example_templates/yemen.html").read_bytes(),
            mime_type="text/html",
        ),
        Part.from_bytes(
            data=(DATA_DIR / "example_templates/afghanistan.html").read_bytes(),
            mime_type="text/html",
        ),
    ]

    data_urls = urls

    data_pdfs = [
        Part.from_bytes(
        data=(DATA_DIR / "syria-data-1.pdf").read_bytes(),
        mime_type="application/pdf",
    ),
    ]

    data_csvs = []
    for file in sorted((DATA_DIR /"syria-csv/").glob("*.csv")):
        if file.stat().st_size > 100 * 1024:  # Check if file size is greater than 100KB
            df = pd.read_csv(file, encoding="utf-8")
            aggregated_data = aggregate_dataframe(df)
            data_csvs.append(
            f"<CSV-AGG><ID>{cite_manager.register_cite(file.name, 'CSV-AGG (DATAVIZ)')}</ID><DATA>{aggregated_data}</DATA></CSV-AGG>"
            )
        else:
            csv_data = file.read_text()
            data_csvs.append(
            f"<CSV><ID>{cite_manager.register_cite(file.name, 'CSV (DATAVIZ)')}</ID><DATA>{csv_data}</DATA></CSV>"
            )

    contents = []
    contents.append(
    f"""<MISSION>
    Create a detailed monthly report for:
    <COUNTRY>SYRIA</COUNTRY>
    <DATE>2024-12</DATE>
    <AUTHOR>TEAM Chäffchen<cheftreff@weboverflow.de></AUTHOR> Do not refer to other authors for questions.
    Cite where you got information from. The source data denotes this in <ID>id here</ID> for each input you use in your report. Style: `<SRC>id here</SRC>`. Maximum 3 citations per claim.
    <SECTION>Add the following sections to your report: {', '.join(selected_topics)}</SECTION>
    </MISSION>""")

    contents.append("<TEMPLATES>\nUse the following templates as a reference for your report. Follow the structure and style of the templates.")
    contents += template_pdfs
    contents.append("</TEMPLATES>")

    contents.append("""<AVAILABLE DATA>""")
    contents.append(
    f"""<WEBSITES>
    {BACKSLASH.join([url_encode_model(x, cite_manager) for x in data_urls])}
    </WEBSITES>
    """)
    contents.append("<ARTICLES>")
    contents += [x.encode_model(cite_manager) for x in relief_data]
    contents.append("</ARTICLES>")
    contents.append("<CSV>")
    contents += data_csvs
    contents.append("</CSV>")
    contents.append("""</AVAILABLE DATA>""")

    agent_response = stream_data(client.models.generate_content_stream(
        model=MODEL_ID,
        contents=contents,
        config=GenerateContentConfig(
            tools=[
                # TODO: function to read details of reliefweb data
            ],
            system_instruction=system_instruction,
            thinking_config=ThinkingConfig(
            thinking_budget=THINKING_BUDGET,
            ),
        ),
    ))
    output = re.sub(r"<SRC>(\d+)</SRC>", lambda match: cite_manager.format_html(match.group(1)), agent_response, flags=re.IGNORECASE)
    return output

if __name__ == "__main__":
    print(get_report("Syria", ["HIGHLIGHTS", "economic_updates"]))
