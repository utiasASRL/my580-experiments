all: merged-target merged

merged:
	ps2pdf someCustom.ps
	ps2pdf someStandard.ps
	pdftk A=someCustom.pdf B=someStandard.pdf shuffle A B output merged.pdf
	-open evince merged.pdf

merged-target:
	ps2pdf someCustomTarget.ps
	ps2pdf someStandardTarget.ps
	pdftk A=someCustomTarget.pdf B=someStandardTarget.pdf shuffle A B output merged-target.pdf
	-open evince merged-target.pdf
