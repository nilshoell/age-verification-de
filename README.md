# ID-Based Age Verification

A small python script that implements the algorithm/checksums behind the german ID (Personalausweis) to verify someones age.

## Usage

### Verify Age

To verify a given ID, use

```python
python ./ageverify.py --verify ID BD ED CS
```

where `ID` is the "Personalausweis-ID", `BD` and `ED` the birth and expiry dates in `yymmdd` plus checksum, and `CS` the single-digit checksum.  
Check below to see where each parameter is located on the back of the ID card


### Generate Test Data

To generate a full set of data and valid checksums use

```python
python ./ageverify.py --generate
```

## Background

I wanted to understand how exactly the age verification process implemented on some websites (e.g. the ZDF/ARD Mediathek) based on data of the federal ID works. Since there is not much information only, I had to dig through a lot of government docs including laws to get the full picture.  
The verification process is completely offline, so no validation against a central server is performed. All that can be checked is whether the entered information is syntactically correct and if the checksums arevalid.

All required data is on the back of the ID card, in the bottom three lines:

```
IDD<<[ID]<<<<<<<<<<<<<<<<
[BD]<[ED]D<<<<<<<<<<<[CS]
[NAME]<<<<<<<<<<<<<<<<<<<
```

### Checksums

Every piece of data (the actual ID, the birth date, and the expiry date) is followed by a single-digit checksum. Finally, the last checksum is calculated over all three data points concatenated.  
Before the calculation, all characters are converted to a number, starting with `A` = `10` counting up. However, each letter converted into a number is still treated as a single item, despite having two digits.

For each item, we then determine the next step by calculating the `mod 3` of its position - that means we are rotating through three different calculations while going through the list:

* Opt 1: multiply the number by 7 and store it's mod 10
* Opt 2: multiply the number by 3 and store it's mod 10
* Opt 3: multiply the number by 1 and store it's mod 10

Finally, add up all the results and calculate it's `mod 10` to get the checksum.

### Allowed Characters

Allowed characters are all digits, as well as a set of (most) uppercase latin letters, excluding some potentially ambiguous ones such as O or I. The full list is in the `ALLOWED_CHARS` array.  
There is also a subset of letters that is allowed for the first character of the ID, where different letters have special meaning (some are reserved for temporary IDs, for example), but this is beyond the scope of this overview.