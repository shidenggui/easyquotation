import easyquotation
quotation = easyquotation.use("timekline")
data = quotation.market_snapshot(prefix=True) 
print(data)
