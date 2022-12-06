import pandas as pd
import numpy as np

def preprocess(df,df_region):
    df=df[df["Season"] == "Summer"]
    d=df.merge(df_region, on="NOC", how="left")
    d.rename(columns={"region":"Region","notes":"Notes"},inplace=True)
    d.drop_duplicates()
    d=pd.concat([d,pd.get_dummies(d["Medal"])], axis=1)
    return d