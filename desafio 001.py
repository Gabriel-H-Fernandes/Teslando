ni = 0
I = 0
nf = 0
passo = 1

while passo <= 3:
    try:
        if passo == 1:
            ni = int(input("Digite um número inicial: "))
            passo = 2

        elif passo == 2:
            I = int(input("Digite um incremento: "))
            if I > 0:
                passo = 3
            else:
                print("Erro: O incremento deve ser maior que zero!")

        elif passo == 3:
            nf = int(input("Digite um número final: "))
            if nf >= ni:
                passo = 4 
            else:
                print(f"Erro: O número final deve ser maior ou igual a {ni}!")
                
    except ValueError:
        print("Erro: Digite apenas números inteiros!")


print("\nResultado:")
for i in range(ni, nf + 1, I):
    print(i)
