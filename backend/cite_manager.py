from dataclasses import dataclass


@dataclass
class Cite:
    """
    Represents a citation with a URL and a source.
    """
    url: str
    source: str



class CiteManager:
    def __init__(self):
        self.url2id: dict[str, int] = {}
        self.id2cite: dict[int, Cite] = {}

    def register_cite(self, url: str, source: str) -> int:
        """
        Registers a citation in the cite manager.
        """
        if url in self.url2id:
            return self.url2id[url]

        cite_id = len(self.url2id)
        self.url2id[url] = cite_id
        self.id2cite[cite_id] = Cite(url=url, source=source)
        return cite_id

    def get_cite_url(self, cite_id: int) -> str:
        """
        Returns the URL of a citation.
        """
        return self.id2cite[cite_id]

    def format_markdown(self, cite_id: int) -> str:
        """
        Returns the markdown format of a citation.
        """
        cite = self.id2cite.get(int(cite_id))
        if cite is None:
            return f"[INVALID CITE]()"
        return f"[{cite.source}]({cite.url})"

    def format_html(self, cite_id: int) -> str:
        """
        Returns the markdown format of a citation.
        """
        cite = self.id2cite.get(int(cite_id))
        if cite is None:
            return f"[INVALID CITE]()"
        return f'<a href="{cite.url}" target="_blank">{cite.source}</a>'
