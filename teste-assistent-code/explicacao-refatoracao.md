# Explicação da refatoração — `refatoracao.py`

Este documento descreve as mudanças aplicadas ao arquivo original `refatoracao.py`
para melhorar legibilidade, nomenclatura e robustez.

Resumo das mudanças

- Função renomeada: `c` → `calculate_statistics` — o novo nome é descritivo e
  comunica claramente a responsabilidade da função.
- Tipagem adicionada: uso de `typing.Sequence` e `typing.Tuple` para indicar os
  tipos de entrada e saída.
- Docstring: adicionado para explicar propósito, retorno e comportamento.
- Validação de entrada: lança `ValueError` quando a sequência está vazia, evitando
  divisões por zero e resultados inesperados.
- Uso de built-ins: substituição de loops manuais por `sum()`, `len()`, `max()` e
  `min()` para código mais claro e conciso.
- Estrutura de execução: uso do guard `if __name__ == "__main__"` e variáveis com
  nomes significativos (`sample`, `total`, `mean`, `maximum`, `minimum`).

Antes (problemas principais)

- Nomes pouco expressivos: função `c` e variáveis como `t`, `m`, `mx`, `mn`.
- Repetição de lógica manual (loops indexados) quando operações built-in são mais
  legíveis e eficientes.
- Falta de checagem para lista vazia; o código falharia com divisão por zero.

Depois (benefícios)

- Legibilidade: leitores entendem o que cada parte faz sem decifrar abreviações.
- Manutenção: código mais curto e com funções padrão facilita ajustes futuros.
- Robustez: tratamento explícito de entrada vazia e assinaturas de tipo ajudam
  detectarem usos incorretos em tempo de desenvolvimento.

Complexidade e desempenho

- A complexidade assintótica não mudou: operações como `sum`, `max` e `min`
  ainda percorrem a lista, resultando em O(n) tempo e O(1) espaço adicional.
- O código agora depende de implementações internas otimizadas do Python para
  somas e buscas, que costumam ser eficientes em C.

Exemplo de uso

```bash
python3 teste-assistent-code/refatoracao.py

# saída esperada
total: 346
media: 34.6
maior: 89
menor: 2
```

Sugestões futuras

- Adicionar testes unitários (`pytest`) cobrindo casos normais e de erro (lista
  vazia, valores com floats, etc.).
- Documentar a função em um `README` ou na documentação do projeto caso seja
  exportada para uso por outros módulos.
- Se precisão numérica for importante (por exemplo, somas de muitos floats),
  considerar uso de `math.fsum` para reduzir erros de arredondamento.
