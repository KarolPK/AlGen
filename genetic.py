
class genetic:
    """
    To nie jest ani trochę działający kod, tylko szkic koncepcji

    Ma tworzyć obiekt, który zawiera populację i ją przetwarza.
    Kolejno wpisane są metody, które razem stworzą całą iterację programu.
    Podział na takie metody jest dla czytelności.
    Genotyp będzie zmieniony, do niego trzeba dopasować osrateczny kształt operatorów mutacji, krzyżowania itd

    """
    genotyp = [False *x]
    read(genotyp populacja)
    fit
    normalize fit: (this fit ) /(max fit - min fit) + 0.5
    def select:
        for i in range(populacja):
            los = random( ) *sum(normalize fit)
            j = 0
            while populacja['podsuma'][ j +1 ]< =los:
                ++j
            nowa_populacja.append(populacja.loc[j])

    def cross(paren1, parent2):
        if rand(1 ) <p_cross:
            cis = rand(len(parent))
            ch1 = parent1[0:cis ] +parent2[cis:len(parent)]
            ch2 = parent2[0:cis ] +parent1[cis:len(parent)]
            else:
            ch1 = parent1
            ch2 = parent2
    return (ch1, ch2)

def mutate(genotyp):
    for i, bit in enumerate(genotyp):
        if rand(1) < p_mutate:
            genotyp[i] = ~bit
    return genotyp
