using CSV, DataFrames

df = CSV.read("data.csv", DataFrame)

shape = size(df)

print(names(df))

select!(df, Not("Column1"))


