levels = [
    [["CuCuCuCu"], ["CuCuCuCu"], [0, 0, 0, 0, 0, 0, 0, 0]],  # 1
    [["CuCuRuRu"], ["RuRuCuCu"], [1, 1, 0, 0, 0, 0, 0, 0]],  # 2
    [["--CuRu--", "--RuCu--"], ["Ru----Cu", "Cu----Ru"], [1, 1, 1, 0, 0, 0, 0, 0]],  # 3
    [["RuRuRuRu"], ["--RuRu--", "Ru----Ru"], [1, 1, 1, 1, 1, 0, 0, 0]],  # 4
    [["SbSbSbSb"], ["Sb------", "Sb------", "Sb------", "Sb------"], [1, 1, 1, 1, 1, 0, 0, 0]],  # 5
    [["WyWy----", "CcCc----"], ["WyCcWyCc"], [1, 1, 1, 1, 1, 1, 0, 0]],  # 6
    [["CbCcCbCc"], ["CbCbCcCc"], [1, 1, 1, 1, 1, 1, 0, 0]],  # 7
    [["RrCgRrCg"], ["Rr------:Cg------", "Cg------:Rr------"], [1, 1, 1, 1, 1, 1, 0, 0]],  # 8
    [["RuCuRuCu", "r"], ["CuCrRuRr"], [1, 1, 1, 1, 1, 1, 1, 0]],  # 9
    [["WuWuWuWu", "c", "y"], ["WuWcWuWy"], [1, 1, 1, 1, 1, 1, 1, 0]],  # 10
    [["CuRuCuRu", "r", "RuCuRuCu"], ["RrCuRrCu:CuRrCuRr"], [1, 1, 1, 1, 1, 1, 1, 0]],  # 11
    [["r", "g", "y", "b"], ["y", "w"], [0, 0, 0, 0, 0, 0, 0, 1]],  # 12
    [["CuCuCuCu", "r", "g", "b"], ["CuCrCyCw"], [1, 1, 1, 1, 1, 1, 1, 0]],  # 13
    [["r", "CuCuCuCu", "g", "RuRuRuRu", "b"], ["RbRuRbRu:CyCyCuCu"], [1, 1, 1, 1, 1, 1, 1, 1]],  # 14
    [["r", "b", "WuWgWuWu", "r", "b", "CuSuCuRu"], ["CrWbRmWw:SbWrWuCm"], [1, 1, 1, 1, 1, 1, 1, 1]],  # 15
    [["RuWuRuWu", "y", "c", "r", "b", "SuSuSuSu"], ["WySr----:--ScRc--", "----ScSb:--RbWw--"], [1, 1, 1, 1, 1, 1, 1, 1]]  # 16
]

# Per level a different setup is used: Different outputs,
# different inputs and only the functions that are allowed to be used
# Setup: [[Outputs], [Inputs], [Functions that are allowed]]
