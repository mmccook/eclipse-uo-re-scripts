## How to use:
- Download the repo and extract into a Eclipse folder in RazorEnhanced/Scripts folder.

- For Mining you need at least 2 rune books, one for just the bank and the other(s)
- Get the Serial for the Bank one and update the `static_runebooks_serial` in `Resources.py`
  
Example `static_runebooks_serial` object

```python
static_runebooks_serial = {
    'bank': {
        "YOUR_CHARACTER_NAME_HERE": YOUR_BANK_RUNEBOOK_SERIAL_FROM_INSPECTOR
    }
}
```

- Get the serials for the runebooks with all your mining locations in them and update `runebooks` in `scripts/mining_recall.py`

Example: `runebooks` array
```python
runebooks=[SERIAL_FOR_RUNEBOOK_HERE,ANOTHER_RUNEBOOK_SERIAL_HERE]
```

