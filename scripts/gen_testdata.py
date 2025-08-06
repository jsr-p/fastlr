import fastlr

X, y = fastlr.generate_data(N=50, k=2, seed=42)

print("X = [")
for row in X:
    print("[", ", ".join(f"{x:.2f}" for x in row), "],")
print("]")

print("y = [")
for value in y:
    print(f"{value:.2f},")
print("]")
