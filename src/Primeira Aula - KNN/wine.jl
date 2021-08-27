using CSV, DataFrames, StatsBase, MLJ

df = CSV.read("vinho.csv", DataFrame)

shape = size(df)

target = "is good"
target_column = copy(df[!, "is good"])
features = copy(df)
delete!(features, findfirst( isequal(target), names(features)))
X_train, X_val, y_train, y_val = train_test_split(features, df, test_size=0.2, random_state=42)
train, valid, test = partition(eachindex(y), 0.7, 0.2, shuffle=true, rng=1234)
#teste = train_test_split(features, target_column, test_size=0.2, random_state=42)

println(typeof(features))
println(typeof(target_column))
