from molmass import Formula

user_input = input("Enter molecules to calc. mol mass of: (as list sep with ,):\n")

mols = user_input.split(",") 
mols = [mol.strip() for mol in mols]
print(f"Molecule:        Mass:\n")
for mol in mols:
    f = Formula(mol)
    if f.formula:
        mass = f.mass 
        print(f"\n{mol:<15} {f.mass:.2f}")
    else: 
        print(f"Invalid input for {mol}")

print("\n-----------------")
print("*", "DONE".center(13), "*")
print("-----------------")
