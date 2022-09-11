def index_chart(data):
    # df = data[ref].copy()
    df = data.copy()
    df.dropna(axis=0, inplace=True)
    columns = [x for x in df.columns]
    for x in columns:
        df[x] = (df[x]/df.iloc[0,columns.index(x)])
    return df
