import random, string, io

print("=== Zander's Batch Obfuscator ===")
print("(c) Chef Zander - 2022")
print("-> included in Zander's Toolbox")
print()

# config
# -> Transformers
tra_charvar_rename = True
tra_uselesscode_troll = True

# -> Character-Variable Renamer Settings
obf_charset = string.ascii_letters # complicated, just leave it unless you know what you are doing
obf_varmin = 69 # min 50 or it might have duplicates
obf_varmax = 420 # max 1000 or it might crash

# -> Useless Code Adder Settings
obf_add_cmdc = True
obf_add_cmdc_chance = 100 # in %
obf_add_cmdc_cmd = "cmd /c echo Nope"

obf_add_echonul = True
obf_add_echonul_chance = 100 # in %
obf_add_echonul_cmd = "echo>nul Nop"

# utility
def random_string_generator(min, max):
    return ''.join(random.choice(obf_charset) for x in range(random.randrange(min, max)))
def log(str):
    print("-> " + str)

# files
infile = "in.cmd"
outfile = "asfd.cmd"
log(f"In File: {infile}")
log(f"Out File: {outfile}")

# lines
lines_raw = []
lines_pre = []
lines_obf = []
lines_final = []

headers = []
mappings = {}

# read src
log("Reading InFile")
lines_raw = open(infile).readlines()
log("Cleaning")
for line in lines_raw:
    lines_pre.append(line.strip())

# generate headers and mappings
log(f"Generating Mappings ({str(len(obf_charset))} items)")
for char in obf_charset:
    mp = random_string_generator(obf_varmin, obf_varmax)
    mappings[char] = mp
    headers.append(f"set {mp}={char}")
log("Done!")

# use headers on code
log("Obfuscating Code using mappings")
ignore = [' ', '.', '=', '%', '/', '>']
def obfuscate(line):
    obfl = ""
    for char in line:
        if(not char in ignore):
            obfl = obfl + f"%{mappings[char]}%"
        else:
            obfl = obfl + char
    return obfl

for line in lines_pre:
    if(line.startswith("rem ")): continue
    if(tra_charvar_rename):
        lines_obf.append(obfuscate(line))
    if(tra_uselesscode_troll):
        if(obf_add_cmdc):
            num = random.randrange(0, 100)
            if(num < obf_add_cmdc_chance):
                lines_obf.append(obfuscate(obf_add_cmdc_cmd))
        if(obf_add_echonul):
            num = random.randrange(0, 100)
            if(num < obf_add_echonul_chance):
                lines_obf.append(obfuscate(obf_add_echonul_cmd))


log(f"Obfuscated {str(len(lines_pre))} Lines")

# combine in final
mark = [
    "rem 🛡 Zander Obfuscation",
    "rem You Wont Reverse This KEKW",
    "@echo off"
]
lines_final = mark + headers + lines_obf

# write
log(f"Writing to {outfile}")
with io.open(outfile, "w", encoding="utf-8") as f:
    for line in lines_final:
        f.write(line + "\n")
print()
log("Finished!")