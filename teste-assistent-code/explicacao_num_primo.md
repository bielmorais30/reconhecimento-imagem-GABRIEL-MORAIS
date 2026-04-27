# Explicação detalhada — `num_primos.py`

Este documento descreve a versão refatorada de `num_primos.py`, que implementa
uma verificação de primalidade usando trial division otimizada (padrão 6k±1).

Visão geral da função `is_prime(n: int) -> bool`

- Propósito: Determinar se um inteiro `n` é primo retornando `True` ou `False`.
- Validação de entrada: Se `n` não for um `int`, a função retorna `False` (não coercitiva).
- Casos base: `n < 2` → `False`; `2` e `3` → `True`.
- Eliminação rápida: testa divisibilidade por `2` e `3`.
- Algoritmo principal: testa candidatos da forma `6k - 1` e `6k + 1` até `isqrt(n)`.

Por que 6k±1?

Todos os primos maiores que 3 estão na forma `6k±1`. Em vez de testar todos os ímpares,
testar apenas esses candidatos reduz ~2× o número de divisões, tornando o loop
mais eficiente sem complicar muito o código.

Complexidade

- Tempo: O algoritmo faz divisões até a raiz quadrada de `n`, então O(√n) no pior caso,
  com fator constante menor que um teste por todos os ímpares.
- Espaço: O(1) memória adicional.

Bloco principal (CLI)

- O script expõe uma pequena interface via `argparse`.
- Se nenhum número for passado na linha de comando, uma lista de exemplos é usada.
- Exemplo de uso:

```bash
python3 teste-assistent-code/num_primos.py 17 18 19
```

Observações e próximos passos

- Para aplicações que exigem checagem de primalidade em números muito grandes
(por exemplo, > 10^12 ou 64 bits), considere implementar um teste probabilístico
Miller–Rabin com bases determinísticas conhecidas para intervalos específicos.
- A função atual é intencionalmente simples e legível — adequada para ensino,
scripts e uso em que desempenho não seja crítico.
