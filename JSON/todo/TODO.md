# TODO

- add jsonl syntax? https://jsonlines.org/examples
- add ldj syntax? https://webocreation.com/blog/linedelimited-json-ldj-protocol/

## Indentation Pattern

### increaseIndentPattern

#### vscode

```regex
(
  {+
  (?=
    (
      [^\"]*
      \"
      [^\"]*
      \"
    )*
    [^\"}]*
    $
  )
)|
(
  \\[+
  (?=
    (
      [^\"]*
      \"
      [^\"]*
      \"
    )*
    [^\"\\]]*
    $
  )
)
```

#### atom

```regex
^.*(\\{[^}]*|\\[[^\\]]*)$
```
