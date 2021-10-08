from pdf_bot import PdfBot
from utils import Utils
import traceback


class Driver:
    @staticmethod
    def run_automation(automation_map: dict):
        """
        Run a PDF scraping automation on a base URL.
        :automation_map: dict, map containing relevant properties
        :return: None
        """
        try:
            bot = PdfBot(automation_map["base_url"])
            bot.parse_html_for_pdfs()
            bot.download_pdfs(automation_map["pdf_download_dir"])
            for url, document in bot.extract_data_from_pdfs():
                matches, dates = bot.find_matches_in_pdf(
                    pdf=document,
                    process_map={
                        "regex": automation_map["pdf_data_regex"],
                        "pages": automation_map["pages"],
                    },
                ).values()
                for match in matches:
                    print(match)
                    match = Utils.replace_from_match(match_str=match, old_list=["$", "Costs and expenses:\n"])
                    match = Utils.replace_from_match(
                        match_str=match,
                        old_list=["European Commission fine\n"],
                        new="European Commission fines\n",
                    )
                    cols = Utils.map_list_to_cols(Utils.trim_and_split(match), automation_map["row_schema"])
                    for i, date in enumerate(dates):
                        cols[i].insert(0, date)
                    bot.write_to_excel(
                        data=cols,
                        file_path=automation_map["excel_file_path"],
                        header=automation_map["header"],
                        worksheet=automation_map["worksheet_name"],
                        col_wise=True,
                    )

            # write the row fields
            bot.write_to_excel(
                data=[automation_map["row_schema"].keys()],
                file_path=automation_map["excel_file_path"],
                header=automation_map["header"],
                worksheet=automation_map["worksheet_name"],
                col_wise=True,
                col_start=0,
                row_start=2,
            )
        except Exception as e:
            print(f"Error on {url}: {e}: {traceback.print_exc()}")


if __name__ == "__main__":
    tables = {
        "table1": {
            "base_url": "https://abc.xyz/investor/previous/",
            "pdf_name_regex": r"(10Q.pdf)",
            "pdf_download_dir": "output",
            "pdf_data_regex": [r"(?s)(Revenues\n.+?)(?:(?:\r*\n{2})|Basic net income per share)", r"(?s)\d{4}"],
            "pages": (5, 6),
            "excel_file_path": "./output/company_10Q.xlsx",
            "worksheet_name": "Alphabet Income Statement",
            "header": ["Alphabet 10Q - Consolidated Statements of Income"],
            "row_schema": {
                k: []
                for k in (
                    "Revenues",
                    "Cost of revenues",
                    "Research and development",
                    "Sales and marketing",
                    "General and administrative",
                    "European Commission fines",
                    "Total costs and expenses",
                    "Income from operations",
                    "Other income (expense), net",
                    "Income before income taxes",
                    "Provision for income taxes",
                    "Net income",
                )
            },
        },
        "table2": {
            "base_url": "https://investor.apple.com/investor-relations/default.aspx/",
            "pdf_name_regex": r"\(As-Filed\).pdf",
            "pdf_download_dir": "output",
            "pdf_data_regex": [r"(?s)(Products\n.+?)(?:(?:\r*\n{2})|Earnings per share:)", r"(?s)\d{4}"],
            "pages": (3, 4),
            "excel_file_path": "./output/company_10Q.xlsx",
            "worksheet_name": "Apple Operations Statement",
            "header": ["Apple 10Q - Consolidated Statements of Operations"],
            "row_schema": {
                k: []
                for k in (
                    "Products",
                    "Services",
                    "Total net sales",
                    "Sales and marketing",
                    "General and administrative",
                    "European Commission fines",
                    "Total costs and expenses",
                    "Income from operations",
                    "Other income (expense), net",
                    "Income before income taxes",
                    "Provision for income taxes",
                    "Net income",
                )
            },
        },
    }

    # run the automation for each table
    for automation_map in tables.values():
        Driver.run_automation(automation_map)
