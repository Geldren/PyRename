class ArgumentException(Exception):
    def __init__(self, message):
        self.message = message

class Argument:
    TYPE_DEFAULT = 'def'

    def __init__(self, aliases, argtype=TYPE_DEFAULT, parameters=0, functions=[], givenParams=[], name="", argNames=[], desc=[]):
        self._argtype = argtype
        self._parameters = parameters
        self._functions = functions
        self._aliases = aliases
        self._givenParams = givenParams

        #Generate help menu entry for this argument
        self._helpStr = ""
        if len(name) > 0:
            self._helpStr = name + ": "
        for a in aliases:
            self._helpStr = self._helpStr + ' ' + a
        self._helpStr = self._helpStr

        i = 0
        while i < parameters:
            self._helpStr = self._helpStr + ' ' + argNames[i] if len(argNames)>i else "arg"+str(i)
            i+=1
        self._helpStr = "{0:.<50}".format(self._helpStr)

        i = 1
        if len(desc) > 0:
            self._helpStr = self._helpStr + desc[0]
            while i < len(desc):
                self._helpStr = self._helpStr + "\n" + "{0:50}".format("") + desc[i]
                i+=1
        

    def matchAlias(self, arg): return arg in self._aliases
    def defaultAlias(self): return self._aliases[0]
    def argType(self): return self._argtype
    def paramCount(self): return self._parameters
    def givenParams(self): return self._givenParams
    def functions(self): return self._functions
    def aliases(self): return self._aliases

    def trigger(self, paramlist=[]):
        allparams = self._givenParams + paramlist
        allResults = []
        for f in self._functions: allResults.append(f(allparams))
        return allResults

    def __str__(self):
        return "Argument " + self._aliases[0] + "; type " + str(self._argtype) + "; " + str(self._parameters) + " parameters"

    def helpStr(self):
        return self._helpStr

class ArgumentParser:
    def __init__(self):
        self._argDictionary = {}
        self._parsedDictionary = {}
        self._aliasList = []

    def addArgument(self, arg):
        if isinstance(arg, Argument) == False:
            raise ArgumentException("Non-Argument passed to ArgumentParser")
            return

        if arg.argType() not in self._argDictionary:
            self._argDictionary[arg.argType()] = []
        self._argDictionary[arg.argType()].append(arg)

    def parseArgs(self, arglist):
        a = 1

        #Check all args
        while a < len(arglist):
            matched = False
            #Check each dictionary arg type
            for d in self._argDictionary:
                if matched: break
                #Check each arg of the type
                for q in self._argDictionary[d]:
                    if matched: break
                    #if it matches, get data for it and add to _parsedDictionary
                    if q.matchAlias(arglist[a]):
                        if q.argType() not in self._parsedDictionary:
                            self._parsedDictionary[q.argType()] = []
                        givenParams = []
                        for z in range(q.paramCount()):
                            a+=1
                            givenParams.append(arglist[a])
                        self._parsedDictionary[q.argType()].append(Argument(q.aliases(), q.argType(), q.paramCount(), q.functions(), givenParams))
                        self._aliasList.append(q.defaultAlias())

                        matched = True
            if matched == False:
                t = Argument.TYPE_DEFAULT
                if t not in self._parsedDictionary:
                    self._parsedDictionary[t] = []
                self._parsedDictionary[t].append(arglist[a])
            a+=1

    def getArgType(self, t):
        if t in self._parsedDictionary:
            return self._parsedDictionary[t]
        return []

    def getAliasList(self):
        return self._aliasList

    def generateHelp(self):
        helpstr = ""
        for d in self._argDictionary:
            for a in self._argDictionary[d]:
                helpstr = helpstr + a.helpStr() + "\n"
        return helpstr