"""RF data -> integration-script template converter.

Pulls the rows belonging to one site out of a circle's Ericsson SSIS / CCR
workbooks and writes them into the RF_Data_Scripting_Template_4G_5G shape that
LTE_Integration_Scripting_Automtion consumes.

Deliberately free of Django imports so `views.py` can call `convert_site()`
directly when the tool is folded into LTE_Integration_Scripting_Automtion.
"""
from .convert import convert_site, ConversionResult

__all__ = ["convert_site", "ConversionResult"]
