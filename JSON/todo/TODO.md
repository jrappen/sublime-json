# TODO

- check extensions against <https://www.schemastore.org/api/json/catalog.json>
- check "optional" variables for validity
- fix trailing comma (move to JSONC)
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
