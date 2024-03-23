# PDF utils

A CLI tool for simple PDF operations

## Installation

```sh
git clone git@github.com:teshanshanuka/pdfutils.git
cd pdfutils
pip install .
```

## Usage

```
usage: pdfutils [-h] {imgs2pdf,insert,rotate,search,join,remove,scale,pick} ...

subcommands:
    imgs2pdf            Convert images to PDF
    join                Join multiple PDFs into one
    pick                Pick specific pages from a PDF
    remove              Remove specific pages from a PDF
    insert              Insert a PDF into another PDF
    scale               Scale specific pages in a PDF
    rotate              Rotate specific pages in a PDF
    search              Search for text in a PDF

options:
  -h, --help            show this help message and exit
```

To get usage of any subcommand, use `pdfutils <subcommand> -h`
