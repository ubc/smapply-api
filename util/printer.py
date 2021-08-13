import collections

def print_odict(odict, depth=0, name=""):
    if type(odict) == str or type(odict) == int:
        print("{}{}".format("   " * depth, odict))
    elif type(odict) == list or type(odict) == tuple:
        for i in range(len(odict)):
            if type(odict[i]) == str or type(odict[i]) == int:
                print("{}{}[{}] = {}".format("   " * (depth), name, i, odict[i]))
            else:
                print("{}{}[{}]".format("   " * (depth), name, i))
                print_odict(odict[i], depth+1)
    elif type(odict) == collections.OrderedDict or type(odict) == dict:
        for key in odict.keys():
            if type(odict[key]) == list or type(odict[key]) == dict or type(odict[key]) == collections.OrderedDict:
                print("{}{}[{}]".format("   " * depth, name, key))
                print_odict(odict[key], depth+1)
            else:
                print("{}{}[{}] = {}".format("   " * depth, name, key, odict[key]))

def list_responses(response):
    if type(response) is list:
        print("response is list of length [{}]".format(len(response)))
        print("1) print first")
        print("2) print all")
        confirm = input("? ")
        if confirm == "1":
            print_odict(response[0])
        elif confirm == "2":
            print_odict(response)
        else:
            print("Bad input.")
    else:
        print_odict(response)
    
