# Explicação do `debug.py` — identificação, causa e correção

Resumo rápido

- Arquivo analisado: [teste-assistent-code/debug.py](teste-assistent-code/debug.py)
- Objetivo: identificar erros, explicar a causa e apresentar uma correção funcional.

1) Erros identificados

- SyntaxError na linha que define `item1`: o prompt não está entre aspas (input(Preço do item 1? )).
- `desconto_cupom` é lido como string (uso de `input`) mas depois usado em cálculo aritmético; falta conversão para número, causando `TypeError` ou comportamento incorreto.
- Uma das linhas de `print` usa chaves de formatação sem `f`-string: print(" Item 2:        R$ {total_item2:.2f}") — isso imprime as chaves literais em vez do valor.
- Erro de indentação: o `print` dentro do `if desconto_cupom > 0:` não está indentado, resultando em `IndentationError`.

2) Causa

- Falta de aspas no argumento de `input` faz com que o Python tente interpretar um identificador não definido/um token inválido, gerando `SyntaxError` na importação/execução.
- `input()` sempre retorna `str`. Usar esse retorno diretamente em operações numéricas (divisão/multiplicação) sem conversão causa `TypeError` ou resultados errados. O código original também testa `if desconto_cupom > 0` sobre uma string.
- Esquecer o prefixo `f` antes da string faz com que a expressão entre chaves não seja avaliada.
- Impressões e blocos condicionais sem a indentação correta violam a sintaxe do Python e interrompem a execução.

3) Correção proposta

- Colocar as mensagens de `input()` entre aspas.
- Converter entradas numéricas imediatamente para `int`/`float` conforme esperado.
- Usar `f`-strings ao formatar valores com casas decimais.
- Indentar corretamente o corpo do `if`.

4) Código corrigido (substitua o conteúdo do arquivo original por este bloco ou aplique as mudanças mostradas abaixo):

```python
# ENTRADA DE DADOS
cliente = input("Qual é seu nome? ")

qtd1 = int(input("Quantidade do item 1: "))
item1 = float(input("Preço do item 1? "))

qtd2 = int(input("Quantidade do item 2: "))
item2 = float(input("Preço do item 2? "))

qtd3 = int(input("Quantidade do item 3: "))
item3 = float(input("Preço do item 3? "))

# CÁLCULOS DOS ITENS
total_item1 = qtd1 * item1
total_item2 = qtd2 * item2
total_item3 = qtd3 * item3

subtotal = total_item1 + total_item2 + total_item3
imposto = subtotal * 0.10

# DESCONTO
# converter o valor do cupom para float (percentual)
desconto_cupom = float(input("Você tem um cupom de desconto? (Digite o percentual ou 0): "))
desconto = subtotal * (desconto_cupom / 100)

# TOTAL FINAL
total = subtotal + imposto - desconto

# EXIBIÇÃO
linha = "=" * 31
separador = "-" * 31

print(linha)
print(f" Cliente: {cliente}")
print(linha)
print(f" Item 1:        R$ {total_item1:.2f}")
print(f" Item 2:        R$ {total_item2:.2f}")
print(f" Item 3:        R$ {total_item3:.2f}")
print(separador)
print(f" Subtotal:      R$ {subtotal:.2f}")
print(f" Imposto (10%): R$ {imposto:.2f}")

if desconto_cupom > 0:
    print(f" Desconto ({desconto_cupom:.0f}%): -R$ {desconto:.2f}")

print(linha)
print(f" TOTAL:         R$ {total:.2f}")
print(linha)
```

5) Observações e melhorias opcionais

- Validação: adicionar checagens para entradas negativas ou valores não numéricos com try/except e mensagens amigáveis.
- Localização/formatos: ao mostrar valores monetários, considerar `locale` para separar milhares e usar vírgula/ ponto conforme região.
- Testes: criar um conjunto de testes automatizados (por exemplo, adicionar uma função que calcula o total e testar várias combinações).

6) Como aplicar a correção

- Opção rápida: substituir o conteúdo do arquivo [teste-assistent-code/debug.py](teste-assistent-code/debug.py) pelo bloco de código corrigido acima.
- Se quiser, posso aplicar a correção automaticamente no arquivo `debug.py` e executar um teste; basta confirmar.

Fim da explicação
