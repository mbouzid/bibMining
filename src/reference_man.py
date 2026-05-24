class ParseTEI:
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    biblStruc = ".//tei:biblStruct"


class Reference:
    def __init__(self, authors, title, journal, year, doi, xml_id):
        self._authors = authors
        self._title = title
        self._journal = journal
        self._year = year
        self._doi = doi
        self._xml_id = xml_id


    def get_authors(self):
        return self._authors

    def get_title(self):
        return self._title

    def get_journal(self):
        return self._journal

    def get_year(self):
        return self._year

    def get_doi(self):
        return self._doi

    def get_xml_id(self):
        return self._xml_id

    @staticmethod
    def from_xml_element(bibl):
        ns = ParseTEI.ns

        # --- Title ---
        title = None
        journal = None
        xml_id = bibl.get("{http://www.w3.org/XML/1998/namespace}id")



        # Case 1: analytic
        title_el = bibl.find(".//tei:analytic/tei:title", ns)
        if title_el is not None:
            title = title_el.text
            if title is not None:
                title = title.strip()
            journal_el = bibl.find(".//tei:monogr/tei:title[@level='j']", ns)
            if journal_el is not None:
                journal = journal_el.text

        # Case 2: monogr-only (title level="m")
        else:
            monogr_title = bibl.find(".//tei:monogr/tei:title[@level='m']", ns)
            if monogr_title is not None:
                raw = monogr_title.text.strip()
                # heuristic: if last sentence looks like journal abbrev, split
                if "." in raw:
                    parts = raw.rsplit(".", 1)
                    if len(parts) == 2 and len(parts[1].strip().split()) <= 3:
                        title, journal = parts[0].strip(), parts[1].strip()
                    else:
                        title = raw
                else:
                    title = raw

        analytic_title = bibl.find(".//tei:analytic/tei:title[@type='main']", ns)
        monogr_title = bibl.find(".//tei:monogr/tei:title[@level='m']", ns)

        chapter_title = analytic_title.text if analytic_title is not None else None
        book_title = monogr_title.text if monogr_title is not None else None

        parts = []
        if chapter_title:
            parts.append(chapter_title.strip())
        if book_title:
            parts.append(book_title.strip())

        title = ". ".join(parts) if parts else None

        # --- Authors ---
        authors = []
        for path in [".//tei:analytic/tei:author", ".//tei:monogr/tei:author"]:
            for author in bibl.findall(path, ns):
                forename = author.find(".//tei:forename", ns)
                surname = author.find(".//tei:surname", ns)
                authors.append((
                    forename.text if forename is not None else None,
                    surname.text if surname is not None else None
                ))
            if authors:  # stop if we found some
                break

        # --- Date ---
        date = None
        date_el = bibl.find(".//tei:monogr/tei:imprint/tei:date", ns)
        if date_el is not None:
            date = date_el.text

        # --- DOI ---
        doi = None
        doi_el = bibl.find(".//tei:analytic/tei:idno[@type='DOI']", ns)
        if doi_el is not None:
            doi = doi_el.text

        return Reference(authors, title, journal, date, doi, xml_id)

#%%
import xml.etree.ElementTree as ET

class ParseTEI:
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}
    biblStruc = ".//tei:biblStruct"

class Publication:

    def __init__(self, title, references):
        self._title = title
        self._references = references

    def get_title(self):
        return self._title

    def get_references(self):
        return self._references

    @staticmethod
    def from_xlsx(xlsx_row):
        xmlfile = "../data/refs_table/" + xlsx_row['TeiFile'] + '.xml'

        tree = ET.parse(xmlfile)
        root = tree.getroot()

        references = []

        for bibl in root.findall(ParseTEI.biblStruc, ParseTEI.ns):
            references.append(Reference.from_xml_element(bibl))

        return Publication(xlsx_row['Title'], references)
