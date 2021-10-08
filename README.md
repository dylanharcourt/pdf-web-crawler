# PDF Web Crawler

## Features

PDF web crawler that supports downloading PDFs on any webpage.
- Crawl HTML text and find PDFs matching search criteria
- Download PDFs to local file directory
- Extract and transform PDF tabular data and write it to an Excel workbook

## Example

Here is an image of what you can with PDF table data

![PDF Web Crawler applied to PDF table scraping](https://codebrew.ai/static/08ebc2327d9f6a165581f52e10ea6466/7d769/example_pdf_table_scrape_column.png)

## Installation
```bash
git clone https://github.com/dylanharcourt/pdf-web-crawler.git
```

## General Usage

General usage is for downloading PDFs from a supplied base URL. All automations are meant to exist in `driver.py` and be invoked by running the file at the command line.
You will need to create a new automation function in the `Driver class` and add logic to invoke it like this:
```python
class Driver:
  @staticmethod
  def run_download_automation(automation_map: dict) -> None:
    bot = PdfBot(automation_map["base_url"])
    bot.parse_html_for_pdfs()
    bot.download_pdfs(automation_map["pdf_download_dir"])
    
if __name__ == "__main__":
  automations = {
    "automation1": {
      "base_url": [YOUR_BASE_URL],
      "pdf_download_dir": [NAME_OF_OUTPUT_DIRECTORY],
    }
  }
  
  # run the automation for each URL
  for automation_map in automations.values():
    Driver.run_download_automation(automation_map)
    
```

This will download all PDFs from base URL. Add a key in the automation map called `pdf_name_regex` and pass it as an arg to `bot.parse_html_for_pdfs()` if you want to match certain PDFs by regex.

The full list of properties for argument `automation_map`:
| Key                     | Type           | Description                                                                                                    |
| ----------------------- | ---------------| -----------------------------------------                                                                      |
| `"base_url"`            | `str`          | The base URL to scrape from                                                                                    |
| `"pdf_name_regex"`      | `regex`        | The regex to filter matches on PDFs                                                                            |
| `"pdf_download_dir"`    | `str`          | The directory you want to write output to                                                                      |
| `"pdf_data_regex"`      | `List[regex]`  | List of regex expressions to match pdf content against                                                         |
| `"pages"`               | `Tuple`        | Range of pages to scrape from in the PDF. Needs to be a valid Python range (i.e. (start=int, step=0, end=int)) |
| `"excel_file_path"`     | `str`          | File path to save Excel workbook to (i.e. ./output/file_name.xlsx)                                             |
| `"worksheet_name"`      | `str`          | Name of the worksheet in the workbook to create and write to                                                   |
| `"header"`              | `List[str]`    | List of column fields for the worksheet's header                                                               |
| `"row_schema"`          | dict           | Row schema; must be key: field name, val: []; (this field is optional if you do not have a row schema)         |


## Usage (table data extraction feature)
1. Define an `automation_map` dictionary in the `driver.py` file. This will contain all of the automations you want to run. The current impl in `run_automation` is developed for
scraping Alphabet's 10Q statements and writing them to Excel. You will need to define your own automation logic for your use case

## Upcoming
- CLI
- More features soon!
