# A helper app to manage investments

## Features
- Add new investment
- Add subscription to existing investment
- Add redemption to existing investment
- Add dividend to existing investment
- Update the price of existing investment
- Generate reports of investments to a spreadsheet.

## Supported UI Language
- Currently, supports Chinese only.
- Update language.py to add more languages.

## Dependencies
- The .toml in the project lists required dependencies.
- [PySimpleGUI](https://pysimplegui.com/) for GUI. 
Developer key is required. Read its website for details.
- [OpenPyXL](https://openpyxl.readthedocs.io/en/stable/)
for spreadsheet generation.
- [SciPy](https://scipy.org/) for financial calculation.

## Licenses
InvestHelper is released under 
[GPLv2](https://www.gnu.org/licenses/old-licenses/gpl-2.0.html).

| Package       | License                                                                                                                                |
|---------------|----------------------------------------------------------------------------------------------------------------------------------------|
| OpenPyXL      | MIT                                                                                                                                    |
| SciPy         | BSD                                                                                                                                    |
| PySimpleGUI | This product includes PySimpleGUI (https://PySimpleGUI.com).<br/>PySimpleGUI is Copyright (c) PySimpleSoft, Inc. and/or its licensors.<br/>Use of PySimpleGUI is subject to the license terms available at https://PySimpleGUI.com/eula |
