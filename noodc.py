import os
import sys

# Some global variables
_GLOBALS = {
"keywords": ["if", "elif", "else", "then", "end", "startnoodling", "noodleuntil"],
"commands": {"nop", "set", "push", "pop", "get", "add", "sub", "out",},
"filename": None,
"argv": [],
"args":[],
"vars": {},
"stack": [],
"sc": 0,
"ip": 0,
}

def run_command(cmd : str):
    def _nop():
        pass

    def _set():
        args = _GLOBALS["args"]
        pass

    def _get():
        args = _GLOBALS["args"]
        pass

    def _push():
        args = _GLOBALS["args"]
        pass

    def _pop():
        args = _GLOBALS["args"]
        pass

    def _add():
        result = 0
        while _GLOBALS["sc"] > 0:
                result += _GLOBALS["stack"][::-1].pop(0)
                _GLOBALS["sc"] -= 1
        return

    def _sub():
        result = 0
        while _GLOBALS["sc"] > 0:
            result -= _GLOBALS["stack"][::-1].pop(0)
            _GLOBALS["sc"] -= 1
        return

    def _out():
        while _GLOBALS["sc"] > 0:
            arg = _GLOBALS["stack"][::-1].pop(0)
            print(arg)
            _GLOBALS["sc"] -= 1

    command_list = {
        "nop": _nop, "set": _set, "get": _get, "push": _push, "pop": _pop, "add": _add,
        "sub": _sub, "out": _out,
    }
    
    command_list[cmd]()
    return

def usage() -> None:
    #print("Usage: noodc.py <file>")
    sys.exit()

def tokenize(contents: list) -> None:
    tokens = []
    for i in range(len(contents)):
        # Loop over lines and split each on spaces
        #print(f'\n--------\nProcessing line {i}\n--------')
        line = contents[i]
        temp = line.split(" ")
        #print(f'temp: {temp}')
        appended = False
        for val in temp:
            if "," in val:
                #print("Comma!")
                if len(val) > 1:
                    # Separate , from whatever it is on
                    index = 0
                    #print(f'Inner val: {val[index]}')
                    while index <= len(val) and val[index] != ",":
                        tokens.append(val[index])
                        index += 1
                appended = True
            if ";" in val:
                #print("Semicolon!")
                if len(val) > 1:
                    # Separate ; from whatever it is on
                    if val[:-1] in _GLOBALS["commands"]:
                        tokens.append(val[:-1])
                        tokens.append(val[-1])
                    else:
                        for inner_val in val:
                            if '\n' not in inner_val:
                                tokens.append(inner_val)
                else:
                    # By itself, just append
                    tokens.append(';')
                appended = True
            if val != "" and not appended:
                tokens.append(val)
            #print(f'Tokens so far: {tokens}')
    #print(f'Tokens after processing: {tokens}')
    for item in tokens:
        if item in _GLOBALS["keywords"]:
            i = _GLOBALS["keywords"].index(item)
            #print(f'Encountered keyword "{_GLOBALS["keywords"][i]}". Parsed keyword: {item}')
    print(f'Final tokens: {tokens}')
    return tokens

def execute(tokens : list) -> None:
    #print(f'Length of tokens: {len(tokens)}')
    while _GLOBALS["ip"] < len(tokens):
        #action = _GLOBALS["commands"]["nop"]
        token = tokens[_GLOBALS["ip"]]
        #print(f'IP: {_GLOBALS["ip"]}')
        if token in _GLOBALS["commands"]:
            # Processing a command
            # Get the function to run
            #action = _GLOBALS["commands"][token]
            #print(f'>> Setting action to "{token}"')
            # Build up the arguments
            if token in ["out"]:
                #print(">> Out command")
                # These commands only take 1 arg
                inital_sc = _GLOBALS["sc"]
                _GLOBALS["sc"] = 0
                _GLOBALS["ip"] += 1
                temp = tokens[_GLOBALS["ip"]]
                print(f'>> Initial temp: {temp}')
                if not temp.isdigit():
                    if temp in _GLOBALS["vars"]:
                        temp = _GLOBALS["vars"][temp]
                    else:
                        raise RuntimeError(f'Variable {temp} does not exist!')
                else:
                    # Some digit
                    temp = int(temp)
                print(f'>> Final temp: {temp}')
                _GLOBALS["stack"].append(temp)
                _GLOBALS["sc"] += 1
                run_command("out")
                _GLOBALS["sc"] = inital_sc
            elif token in ["set", "add", "sub"]:
                if token == "set":
                    #print(">> Set command")
                    _GLOBALS["ip"] += 1
                    var = tokens[_GLOBALS["ip"]]
                    _GLOBALS["ip"] += 1
                    val = tokens[_GLOBALS["ip"]]
                    if val.isdigit():
                        val = int(val)
                    else:
                        val = _GLOBALS["vars"][val]
                    _GLOBALS["vars"][var] = val
                    #print(f'>> Var {var} set to {val}. {var} = {_GLOBALS["vars"][var]}')
                else:
                    #print(">> Add command")
                    # Add command puts result on top of stack
                    # These commands take 2 args
                    inital_sc = _GLOBALS["sc"]
                    _GLOBALS["sc"] = 0
                    # IP points to add token, have to inc at start of loop
                    # Next two tokens will be variable names, digits, or a combo
                    _GLOBALS["ip"] += 1
                    val1 = tokens[_GLOBALS["ip"]]
                    if val1.isdigit():
                        val1 = int(val1)
                        name1 = str(val1)
                    else:
                        name1 = val1
                        if val1 in _GLOBALS["vars"]:
                            val1 = _GLOBALS["vars"][val1]
                        else:
                            raise RuntimeError(f'Variable {name1} does not exist!')
                    _GLOBALS["ip"] += 1
                    val2 = tokens[_GLOBALS["ip"]]
                    if val2.isdigit():
                        val2 = int(val2)
                        name2 = str(val2)
                    else:
                        name2 = val2
                        if val2 in _GLOBALS["vars"]:
                            val2 = _GLOBALS["vars"][val2]
                        else:
                            raise RuntimeError(f'Variable {name2} does not exist!')
                    #print(f'>> Adding {name1} and {name2} to get {val1 + val2}')
                    #result = val1 + val2
                    #_GLOBALS["stack"].append(result)
                    _GLOBALS["stack"].append(val2)
                    _GLOBALS["sc"] += 1
                    _GLOBALS["stack"].append(val1)
                    _GLOBALS["sc"] += 1
                    #print(f'>> Stack changed. Added {result}')
                    run_command("add")
                    _GLOBALS["sc"] = inital_sc
        else:
            _GLOBALS["ip"] += 1
        """elif token in [";"]:
            # Hit a semicolon, execute command
            args = []
            #print(f'>> Stack (Raw): {_GLOBALS["stack"]}')
            #print(f'>> Stack: {_GLOBALS["stack"][::-1]}')
            while _GLOBALS["sc"] > 0 and len(_GLOBALS["stack"]) > 0:
                args.append(_GLOBALS["stack"][::-1].pop(0))
                _GLOBALS["sc"] -= 1
            if action is not _GLOBALS["commands"]["nop"]:
                #print(f'>> Action: {tokens[_GLOBALS["ip"] - 1]}')
                #print(f'>> Args: {args}')
                action(args)
                #print(f'>> End action {token}')
            _GLOBALS["ip"] += 1
        
        else:
            _GLOBALS["ip"] += 1
        """


def main() -> None:
    if len(sys.argv[1:]) < 1:
        usage()
    else:
        _GLOBALS["argv"] = sys.argv
        _GLOBALS["filename"] = _GLOBALS["argv"][1]
        #print(_GLOBALS["filename"])

    try:
        filehandle = open(_GLOBALS["filename"], 'r')
    except FileNotFoundError:
        raise Exception("File not found!")
    file_contents = filehandle.readlines()
    #print(file_contents)
    tokens = tokenize(file_contents)
    execute(tokens)


if __name__ == '__main__':
    main()