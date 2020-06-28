# TexToEnglish.py is a program meant to take in a single string a latex code in the form of an equation
# and output that same string translated into spoken English.
#
# To run this program ensure the following line is added to the top of the file calling the command:
#   import TexToEnglish
#
# Then use the command (LatexString being a string of latex code):
#   TexToEnglish.getEnglish(LatexString)
#
# The above command will return a string containing the English interpretation of the latex code in the
# LatexString variable

def getEnglish(inString):
    global specialChar
    global g_letters
    global var_g_letters
    global intToWord
    global compCommandToKey
    global specialCharToWord
    global int_flag
    global frac_flag

    setUp()

    # First we start by splitting the input string at all points that contain "\"
    inString.strip()
    stringArr = inString.split("\\")

    Eng_String = ""

    for i in range(0, len(stringArr)):
        letterIndex = 0
        startingIndex = 0
        for j in range(0, len(stringArr[i])):
            print(Eng_String)
            letter = (stringArr[i])[j]

            if (j == len(stringArr[i])-1):
                if (letter in specialChar):
                    command = findCommand(stringArr[i], startingIndex, j)
                    Eng_String += str(command) + " "
                    sChar = (stringArr[i])[j:j+1]
                    Eng_String +=  specialCharToWord[sChar] + " "
                elif (letter == "}"):
                    command = findCommand(stringArr[i], startingIndex, j)
                    Eng_String += str(command) + " "
                    command = closeComplexCommand()
                    Eng_String += str(command) + " "
                elif (letter == "{"):
                    command = startComplexCommand(stringArr[i], startingIndex, j+1)
                    Eng_String += str(command) + " "
                else:
                    command = findCommand(stringArr[i], startingIndex, j+1)
                    Eng_String += str(command) + " "

                continue

            if (letter == " "):
                command = findCommand(stringArr[i], startingIndex, j)
                Eng_String += str(command) + " "
                startingIndex = j+1
                
            if (letter == "}"):
                if (j - startingIndex != 0):
                    command = findCommand(stringArr[i], startingIndex, j)
                    Eng_String += str(command) + " "
                command = closeComplexCommand()
                Eng_String += str(command) + " "
                startingIndex = j+1

            if (letter == "{"):
                command = startComplexCommand(stringArr[i], startingIndex, j+1)
                Eng_String += str(command) + " "
                startingIndex = j+1

            if (letter in specialChar):
                # Manual override for brackets
                if (letter == "(" or letter == ")"):
                    command = findCommand(stringArr[i], startingIndex, j)
                    Eng_String += str(command) + " "
                    command = startComplexCommand(letter, 0, 1)
                    Eng_String += str(command) + " "
                    startingIndex = j+1
                    continue

                nextLetter = (stringArr[i])[j+1]

                if (nextLetter == "{"):
                    if (j - startingIndex != 0):
                        command = findCommand(stringArr[i], startingIndex, j)
                        Eng_String += str(command) + " "
                        startingIndex = j
                    continue
                elif (nextLetter == "}"):
                    if (startingIndex - j == 0):
                        sChar = (stringArr[i])[j:j+1]
                        Eng_String +=  specialCharToWord[sChar] + " "
                        startingIndex = j+1
                    else:
                        command = findCommand(stringArr[i], startingIndex, j)
                        Eng_String += str(command)
                        sChar = (stringArr[i])[j:j+1]
                        Eng_String +=  specialCharToWord[sChar] + " "
                        startingIndex = j+1
                    continue
                else:
                    command = findCommand(stringArr[i], startingIndex, j)
                    Eng_String += str(command) + " "
                    sChar = (stringArr[i])[j:j+1]
                    Eng_String +=  specialCharToWord[sChar] + " "
                    startingIndex = j+1

    Eng_String = cleanString(Eng_String)
    return Eng_String

def findCommand(stringEntry, startIndex, endIndex):
    # This function is meant to translate individual simple commands (ie: greek letters, mathimatical symbols, etc...).
    # This takes, as input, a keyword parsed out from the latex code and returns the English interpretation of that one
    # key word.

    # Load in the necessary global variables.
    global g_letters
    global var_g_letters

    # Parse out the desired chunch of latex code
    commandString = stringEntry[startIndex:endIndex]
    commandString = commandString.strip()

    # If the command is just a greek letter, then no translation needs to be done
    if (commandString in g_letters):
        return commandString
    if (commandString in var_g_letters):
        return commandString[3, len(commandString)]

    # manual override to deal with brackets
    print(commandString)
    if (commandString == "left" or commandString == "right"):
        try:
            if (stringEntry[endIndex] == "(" or stringEntry[endIndex] == ")"):
                return ""
        except:
            pass

    # See if the given command is a command for a built in symbol
    try:
        symbolString = simpleCommands[commandString]
    except:
        # If we cannot find a given command, then the string is probably just a variable, and it is just returned
        return commandString

    # If the commandString does correspond to a Latex symbol
    return symbolString

def startComplexCommand(stringEntry, startIndex, endIndex):
    # Function that starts a complex command, ie: a command that will influence how later command are translated
    # When a complex command is started, it is added to the flagBuffer. As complex commands close, they are removed
    # from the buffer and a modifed string is translated out

    # Load in the necessary global variables.
    global flagBuffer
    global compCommandToKey
    global intToWord
    global int_flag
    global frac_flag
    global counters

    # Start by parsing off the desired string
    substring = stringEntry[startIndex:endIndex]
    substring = substring.strip()
    if (substring[len(substring)-1] == "{"):
        substring = substring[0:len(substring)-1]

    if (len(substring) == 0):
        if (frac_flag):
            key = "frac"
        else:
            return -1
    else:
        try:
            key = compCommandToKey[substring]
        except:
            return -1

    # bufferInsert is the string that gets inserted into the flagBuffer. This contains a key to denote what command
    # has been started, as well as a number to indicate nesting of that command
    bufferInsert = key + "_"
    outString = ""
    if (key == "exp"):
        counters["exp"] += 1
        bufferInsert += str(counters["exp"])
        outString = "to the"
    if (key == "frac"):
        if (frac_flag):
            bufferInsert += "denom_" + str(counters["frac"])
            outString = intToWord[counters["frac"]] + " denominator,"
        else:
            counters["frac"] += 1
            bufferInsert += "numer_" + str(counters["frac"])
            outString = intToWord[counters["frac"]] + " numerator,"
    if (key == "sub"):
        counters["sub"] += 1
        bufferInsert += str(counters["sub"])
        outString = "sub,"
    if (key == "sqrt"):
        counters["sqrt"] += 1
        bufferInsert += str(counters["sqrt"])
        outString = "square root of,"
    if (key == "vect"):
        outString = "vector"
        bufferInsert += "_0"
    if (key == "bracket_open"):
        counters["bracket"] += 1
        bufferInsert += str(counters["bracket"])
        outString = "bracket,"
    if (key == "bracket_close"):
        if ("bracket_open" not in flagBuffer[0]):
            return -1
        else:
            bracketNum = int((flagBuffer[0])[len(flagBuffer[0])-1])
            if (bracketNum != counters["bracket"]):
                return -1
            counters["bracket"] -= 1
            outString = ", end of " + intToWord[bracketNum] + " bracket,"
            temp_flagBuffer = flagBuffer
            flagBuffer = []
            for k in range(1, len(temp_flagBuffer)):
                flagBuffer.append(temp_flagBuffer[k])
            return outString

    # Add the new buffer string into the first space of the flagBuffer
    if (len(flagBuffer) == 0):
        flagBuffer.append(bufferInsert)
    else:
        temp_flagBuffer = flagBuffer
        flagBuffer = []
        flagBuffer.append(bufferInsert)
        for buf in range(0, len(temp_flagBuffer)):
            flagBuffer.append(temp_flagBuffer[buf])

    return outString

def closeComplexCommand():
    # Load in the necessary global variables.
    global flagBuffer
    global intToWord
    global int_flag
    global frac_flag
    global counters

    commandType = (flagBuffer[0])[0:len(flagBuffer[0])-2]
    firstFlagBuffer = flagBuffer[0]
    commandNum = int(firstFlagBuffer[len(firstFlagBuffer)-1])
    outString = ""

    if ("frac" in commandType):
        if ("denom" in commandType):
            outString = ", end of " + intToWord[commandNum] + " denominator,"
            counters["frac"] -= 1
            frac_flag = False
        elif ("numer" in commandType):
            outString = ", end of " + intToWord[commandNum] + " numerator,"
            frac_flag = True
    if ("exp" in commandType):
        counters["exp"] -= 1
        outString = ", end of " + intToWord[commandNum] + " exponant,"
    if ("sub" in commandType):
        counters["sub"] -= 1
        outString = ", end of " + intToWord[commandNum] + " subscript,"
        print(outString)
    if ("sqrt" in commandType):
        counters["sqrt"] -= 1
        outString = ", end of " + intToWord[commandNum] + " square root,"
    if ("vect" in commandType):
        outString = ""

    # Remove the command in the first place of the flagBuffer
    temp_flagBuffer = flagBuffer
    flagBuffer = []
    for k in range(1, len(temp_flagBuffer)):
        flagBuffer.append(temp_flagBuffer[k])

    return outString

def cleanString(inString):
    # Function meant to cut out the white space and clean up the formatting of the commas

    sArr = inString.split(" ")
    cleanedString = ""

    for i in range(0, len(sArr)):
        if (sArr[i] == ""):
            continue
        if (sArr[i] == ","):
            if (cleanedString[len(cleanedString)-1] == ","):
                continue
            cleanedString += str(sArr[i])
        else:
            cleanedString += " " + str(sArr[i])

    cleanedString.strip()
    return cleanedString

def setUp():
    # This function is called at the beginning of run time and will set up all of the required variable and dictionaries that will be
    # used later in the program.

    # Set up some special characters
    global specialChar
    specialChar = ["_", "^", "+", "-", "/", "*", ">", "<", "=", "(", ")"]
    # Set up some basic greek letters
    global g_letters
    g_letters = ["Alpha", "alpha", "Beta", "beta", "Gamma", "gamma", "Delta", "delta", "Epsilon", "epsilon", "Zeta", "zeta", "Eta", "eta", "Theta", "theta", "Iota", "iota", "Kappa", "kappa", "Lambda", "lambda", "Mu", "mu", "Nu", "nu", "Xi", "xi", "Omicron", "omicron", "Pi", "pi", "Rho", "rho", "Sigma", "sigma", "Tau", "tau", "Upsilon", "upsilon", "Phi", "phi", "Chi", "chi", "Psi", "psi", "Omega", "omega"]
    global var_g_letters
    var_g_letters = ["varepsilon", "vartheta", "varkappa", "varsigma", "varphi"]

    # Dictionary of integers to the corresponding number's word
    global intToWord
    intToWord = {1: "first", 2: "second", 3: "third", 4: "fourth", 5: "fifth", 6: "sixth", 7: "seventh", 8: "eighth", 9: "nineth"}

    # Initialize Flags and flag buffer
    global flagBuffer
    flagBuffer = []
    global int_flag
    int_flag = False
    global frac_flag
    frac_flag = False

    global counters
    counters = {
        "exp": 0,
        "frac": 0,
        "sub": 0,
        "bracket": 0,
        "sqrt": 0
    }

    # Initialize Dictionaries
    global compCommandToKey
    compCommandToKey = {
        "^": "exp",
        "_": "sub",
        "frac": "frac",
        "(": "bracket_open",
        ")": "bracket_close",
        "int": "int",
        "sqrt": "sqrt",
        "vect": "vect"
    }
    global specialCharToWord
    specialCharToWord = {
        "_": "sub",
        "^": "to the",
        "+": "plus",
        "-": "minus",
        "/": "divided by",
        "*": "times",
        ">": "greater than",
        "<": "less than",
        "=": "equals"
    }
    global simpleCommands
    simpleCommands = {
        "nless": "is not less than",
        "leq": "is less than or equal to",
        "leqslant": "is less than or equal to",
        "nleq": "is neither less than nor equal to",
        "nleqslant": "is neither less than nor equal to",
        "prec": "precedes",
        "nprec": "doesn't precede",
        "preceq": "precedes or equals",
        "npreceq": "neither precedes nor equals",
        "ll": "much smaller than",
        "subset": "is a proper subset of",
        "subseteq": "is a subset of",
        "nsubseteq": "	is not a subset of",
        "ngtr": "is greater than or equal to",
        "geqslant": "is greater than or equal to",
        "ngeq": "is neither greater than nor equal to",
        "ngeqslant": "is neither greater than nor equal to",
        "succ": "succeeds",
        "nsucc": "doesn't succeed",
        "succeq": "succeeds or equals",
        "nsucceq": "neither succeeds nor equals",
        "gg": "much greater than",
        "supset": "is a proper superset of",
        "supseteq": "is a superset of",
        "nsupseteq": "is not a superset of",
        "equiv": "is equivalent to",
        "approx": "is approximately",
        "cong": "is congruent to",
        "simeq": "is similar or equal to",
        "sim": "is similar to",
        "propto": "is proportional to",
        "neq": "is not equal to",
        "ne": "is not equal to",
        "parallel": "is parallel with",
        "asymp": "is asymptotic to",
        "in": "is member of",
        "models": "models",
        "perp": "is perpendicular with",
        "nparallel": "is not parallel with",
        "ni": "owns, has member",
        "notin": "is not member of",
        "mid": "divides",
        "pm": "plus or minus",
        "mp": "minus or plus",
        "times": "multiplied by",
        "div": "divided by",
        "ast": "asterisk",
        "exists": "there exists at least one",
        "nexists": "there is no",
        "forall": "for all",
        "neg": "logical not",
        "lor": "logical or",
        "land": "logical and",
        "Longrightarrow": "implies",
        "implies": "implies",
        "Rightarrow": "implies",
        "Longleftarrow": "is implied by",
        "Leftarrow": "is implied by",
        "iff": "if and only if",
        "Leftrightarrow": "if and only if",
        "partial": "partial",
        "hbar": "h bar",
        "nabla": "del",
        "infty": "infinity",
        "sin": "sine",
        "cos": "cosine",
        "tan": "tangent",
        "csc": "cosecant",
        "sec": "secant",
        "cot": "cotangent",
        "arcsin": "arc sine",
        "arccos": "arc cosine",
        "arctan": "arc tangent",
        "arccsc": "arc cosecant",
        "arcsec": "arc secant",
        "arccot": "arc cotangent",
        "sinh": "hyperbolic sine",
        "cosh": "hyperbolic cosine",
        "tanh": "hyperbolic tangent",
        "csch": "hyperbolic cosecant",
        "sech": "hyperbolic secant",
        "coth": "hyperbolic cotangent"
    }
