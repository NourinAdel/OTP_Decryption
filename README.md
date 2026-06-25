# Many-Time Pad Decryption Program

A cryptographic analysis tool that exploits key reuse in stream ciphers (Many-Time Pad attack) to recover multiple plaintexts and reconstruct the original encryption key.

## Overview

The objective of this project is to break some hexadecimal ciphertexts that were insecurely encrypted using the same One-Time Pad (OTP) key. By exploiting the algebraic properties of XOR operation and predictable ASCII patterns, it eliminates the secret key, extracts information about the plaintext, and decrypts the messages.

---

## Decryption Method

### 1. Eliminate Key using XOR
When two ciphertexts that are encrypted with the same key ($K$) are XORed together, the key cancels out and leaves the XOR of the two plaintexts.
$$C_1 \oplus C_2 = (P_1 \oplus K) \oplus (P_2 \oplus K) = P_1 \oplus P_2$$

### 2. Space Detection
In ASCII, any alphabetical character ($[a-z, A-Z]$) XORed with a space character (`0x20`) outputs another alphabetical character with an inverted case. XORing two characters usually outputs non-alphabetic or special characters. 
The program makes use of this by:
* Comparing all ciphertexts byte-by-byte.
* Incrementing the frequency of a certain byte when an alphabetic character is output, i.e. it was likely a space character.
* If frequency goes over the specified `THRESHOLD` (which is equal to `5`), flag that position as a space.

### 3. Partial Key Recovery
Once a position is locked in as a space in ciphertext $A$ at index $i$, the key byte in that position can be found using:
$$K_i = C_{A,i} \oplus 0x20$$

The partial key $K$ decodes a large portion of the text, and leaves unknown characters as `_`. Using this information, the `guesser()` function guesses these gaps in the plaintext and completes the missing key indexes.

---

## Execution and Results

### Dependencies
This project uses standard Python 3 built-in data types and requires no external libraries.

### Running the Project
Execute the script using your terminal or preferred IDE:
```bash
python main.py
```

### Outputs

Before guessing:
```text
_he _pen desig_ _____ipl_ incr___es co__i_en_e i__s_c_____
_ear_ing how t_ _____ se_ure s___ware __ _ n_ces__r_ _____
_ecu_e key exc_a_____s n_eded ___ symm__r_c _ey __c_y_____
_ecu_ity at th_ _____se _f usa___ity c__l_ d_mag__s_c_____
_ode_n cryptog_a_____equ_res c___ful a__ _ig_rou__a_a_____
_ddr_ss random_z_____ co_ld pr___nt ma__c_ou_ ca__ _t_____
_t i_ not prac_i_____o r_ly so___y on __m_et_ic __c_y_____
_ sh_ll never _e_____he _ame p___word __ _ul_ipl__a_c_____
```

After guessing:
```text
The open design principle increases confidence in security
Learning how to write secure software is a necessary skill
Secure key exchange is needed for symmetric key encryption
Security at the expense of usability could damage security
Modern cryptography requires careful and rigorous analysis
Address randomization could prevent malicious call attacks
It is not practical to rely solely on symmetric encryption
I shall never reuse the same password on multiple accounts
```