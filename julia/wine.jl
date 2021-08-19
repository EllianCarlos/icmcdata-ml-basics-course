using CSV, DataFrames, ScikitLearn, StatsBase

df = CSV.read("../vinho.csv", DataFrame)

shape = size(df)

target = "is_good"
features = df.columns.to_list()
features.remove(target)
X_train, X_val, y_train, y_val = train_test_split(df[features], df[target], test_size=0.2, random_state=0)
