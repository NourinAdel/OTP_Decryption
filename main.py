# word guesser function
def guesser(index, position, sentence):
    for i, ch in enumerate(sentence):
        guesses.append((index, position + i, ch))

# turn ciphertexts from hexadecimal to byte format
c1 = bytes.fromhex("68AF0BEF7F39982DA975B5E6D06947E61C22748C94A2155CFCCC464DEAFB6F4844DB2D7312ED192B6B7251580C61D5A296964E824A16648B16B9")
c2 = bytes.fromhex("70A20FBD7E209324A979BFE2997A46E61B22749692EB1655FA995D46A9FA654F43C93F2114A21E3E227714580A6790B88BD74F9E09107D8B0EAC")
c3 = bytes.fromhex("6FA20DBA622CDD28EC68F0F0C16D41A7023778C29EB8455EFC894B46EDA96C46459E2D2A1CEF1239707F571604618CEB9DD85E955013628B0DAE")
c4 = bytes.fromhex("6FA20DBA6220893AA970A4B5CD664CE609286D8799B80010F68A0F56FAE868405BD72A2A51E118386E7214520E6994AC9D964E824A16648B16B9")
c5 = bytes.fromhex("71A80AAA6227DD20FB68A0E1D6695BA71C3864C285AE1445F09E4A50A9EA6B5B52D82B3F51E3192922645D5100769ABE8B965C89480F6F910BB3")
c6 = bytes.fromhex("7DA30ABD753A8E63FB70BEF1D66340BC0D24748D99EB065FEC804B03F9FB6F5F52D02A731CE31B24617F5B431C2496AA94DA1D865D17778109B3")
c7 = bytes.fromhex("75B34EA66369932CFD31A0E7D86D5DAF0F3171C283A44542FC805603FAE6664C5BC77E3C1FA204346F7B51421D6D96EB9DD85E955013628B0DAE")
c8 = bytes.fromhex("75E71DA771259163E774A6F0CB2E5BA3192378C283A30010EA8D4246A9F96B5A44C9312115A21823227B415A1B6D85A79D965C844A0C638C16B3")
c_array = [c1, c2, c3, c4, c5, c6, c7, c8] # list storing ciphertexts in byte form
c_xor_array = [] # list to store xor result of each pair of ciphertexts
THRESHOLD = 5

spaces_array = []
for c in c_array:
    spaces_array.append([0]*len(c)) # to keep track of spaces

# xor each pair of ciphertexts
for i in range(len(c_array)-1):
    for j in range(i+1, len(c_array)):
        ci = c_array[i]
        cj = c_array[j]
        xor_pair = [] # store bytes of a single pair per loop
        for k in range(len(c_array[i])):
            c_xor = ci[k] ^ cj[k] # xor each byte
            xor_pair.append(c_xor)

            # if output in range of characters a-z or A-Z, then there was probably a space
            if (0x61 <= c_xor <= 0x7A) or (0x41 <= c_xor <= 0x5A):
                spaces_array[i][k] += 1  # ith ciphertext may have space here
                spaces_array[j][k] += 1  # jth ciphertext may have space here
        c_xor_array.append(xor_pair) # add final result to main array

spaces = []
for i in range(len(spaces_array)): # ciphertexts
    for j in range(len(spaces_array[i])): # bytes
        if spaces_array[i][j] >= THRESHOLD:
            spaces.append((i,j)) # mark as a space

key_array = [None]*len(c_array[0])

for i,j in spaces:
    key_byte = c_array[i][j]^0x20 # get key byte by xoring with space
    if key_array[j] is None:
        key_array[j] = key_byte
    elif key_array[j] != key_byte:
        continue

# use key_array to decrypt
plaintexts = []
for c in c_array:
    plaintext = []
    for i in range(len(c)):
        if key_array[i] is not None:
            plaintext.append(chr(c[i]^key_array[i]))
        else:
            plaintext.append('_')
    plaintexts.append(plaintext)

for p in plaintexts:
    print(f"{''.join(p)}") # print initial values before guessing
print("\n")

guesses = []
guesser(0,0,'The open design principle increases confidence in security')
guesser(1, 0, 'Learning how to write secure software is a necessary skill')
guesser(2, 0, 'Secure key exchange is needed for symmetric key encryption')
guesser(3, 0, 'Security at the expense of usability could damage security')
guesser(4, 0, 'Modern cryptography requires careful and rigorous analysis')
guesser(5, 0, 'Address randomization could prevent malicious call attacks')
guesser(6, 0, 'It is not practical to rely solely on symmetric encryption')
guesser(7, 0, 'I shall never reuse the same password on multiple accounts')

# update key array
for (index, position, char) in guesses:
    key_byte = c_array[index][position] ^ord(char)
    if key_array[position] is None:
        key_array[position] = key_byte
    elif key_array[position] != key_byte:
        continue

plaintexts = []
for c in c_array:
    plaintext = []
    for i in range(len(c)):
        if key_array[i] is not None:
            plaintext.append(chr(c[i]^key_array[i]))
        else:
            plaintext.append('_')
    plaintexts.append(plaintext)

# display found plaintexts
for p in plaintexts:
    print(f"{''.join(p)}")
