# Refactor log

## 07.16.2026

### Baseline setup

- Dependencies:
  - set up `.venv` and create `requirements.txt`
- Separate metadata from code
  - Move `rooms`, `items`, and `knowings` to `/data`
- Code-splitting:
  - Move `help`, `load`, `save` logic to `/utils`
  - Add `current_room` and `inventory` to `save_game()` params

### rooms

- Change `description` into `string[]`
- Consolidate implicitly concatenated strings to improve readability

## MainGame

- Flatten `getDesc()` and `print_split_text()` to reduce obfuscation
  - Fighting urge to introduce `GameState` class object to replace `current_room: int` and `inventory: string[]`
    - `GameState` would include `getter` (`current_room = rooms[current_room]`)

##

- f
