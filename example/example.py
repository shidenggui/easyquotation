def test_timekline():
    import easyquotation
    quotation = easyquotation.use("timekline")
    data = quotation.market_snapshot(prefix=True) 
    print(data)

def test_daykline():
    import easyquotation
    quotation  = easyquotation.use("daykline")
    data = quotation.get_stock_data(stock_list=['hk00001','hk00700'])
    # data = quotation.get_stock_data(stock_list=['hk00700'])
    print(data)

if __name__ == "__main__":
    test_daykline()

