import array
from flask import Flask, render_template, request

app = Flask(__name__)
# import config
from web3 import Web3


url = "HTTP://127.0.0.1:7545"
w3 = Web3(Web3.HTTPProvider(url))
print(w3.isConnected())
from solcx import compile_standard, install_solc

install_solc("0.8.3")

with open("./test.sol", "r") as file:
    TodolistFile = file.read()


Sol_compiled = compile_standard(
    {
        "language": "Solidity",
        "sources": {"test.sol": {"content": TodolistFile}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.3",
)
w3.eth.defaultAccount = w3.eth.accounts[0]
abi = Sol_compiled["contracts"]["test.sol"]["TodoList"]["abi"]
bytecode = Sol_compiled["contracts"]["test.sol"]["TodoList"]["evm"]["bytecode"][
    "object"
]

# Todo = w3.eth.contract(abi=abi, bytecode=bytecode)
# tx_hash = Todo.constructor().transact()
# tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
# cont = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
address = "0x1E5641980a21d9214B418cc72cE39D8a8F3Ef782"
cont = w3.eth.contract(address=address, abi=abi)


@app.route("/")
@app.route("/home")
def home():

    return render_template("home.html")


@app.route("/hometest", methods=["POST", "GET"])
def hometest():
    return render_template("test.html")


@app.route("/extra", methods=["POST", "GET"])
def extra():
    result = request.form.to_dict()
    Action = str(result["Acy"])
    Day = int(result["Day"])
    May = int(result["May"])
    Yay = int(result["Yay"])
    add = cont.functions.addtolist(Action, Day, May, Yay).transact()
    w3.eth.waitForTransactionReceipt(add)

    say = cont.functions.getlast().call()
    print(say)
    return render_template("test.html", say=say)


@app.route("/dest")
def Getfromlist():
    tot = int(cont.functions.getamnt().call())
    return render_template("dest.html", tot=tot)


@app.route("/deste", methods=["POST", "GET"])
def Getfromlist2():
    tot = int(cont.functions.getamnt().call())
    get = request.form.to_dict()
    index = int(get["list"])

    got = cont.functions.getfromlist(index).call()
    # notgot = cont.functions.notintod(index).call()

    return render_template("dest.html", got=got, index=index, tot=tot)


@app.route("/rem")
def rem():
    tot = int(cont.functions.getamnt().call())
    return render_template("rem.html", tot=tot)


@app.route("/exrem", methods=["POST", "GET"])
def exrem():

    edit = request.form.to_dict()
    index = int(edit["Inde"])
    cont.functions.getamnt().call()
    remove = cont.functions.remfromtodo(index).transact()
    dalo = w3.eth.waitForTransactionReceipt(remove)
    tot = cont.functions.getamnt().call()
    return render_template("rem.html", index=index, tot=tot, remd=dalo)


@app.route("/edit")
def Edit():
    return render_template("editpage.html")


@app.route("/alls")
def Allsaved():
    return "Allsaved Page1"


@app.route("/allt")
def Allthings():
    tor = cont.functions.getamnt().call()
    bat = cont.functions.allTod().call()
    return render_template("allt.html", bat=bat)


@app.route("/editac")
def Editac():
    tor = int(cont.functions.getamnt().call())
    return render_template("editac.html", tor=tor)


@app.route("/reditac", methods=["POST", "GET"])
def Editacs():
    tor = int(cont.functions.getamnt().call())
    ed = request.form.to_dict()
    index = int(ed["index"])
    action = str(ed["action"])
    editac = cont.functions.editaction(index, action).transact()
    w3.eth.waitForTransactionReceipt(editac)
    get = cont.functions.getfromlist(index).call()
    shy = cont.functions.showaction(index).call()
    return render_template("editac.html", get=get, tor=tor, index=index, sha=shy)


@app.route("/editdaye", methods=["POST", "GET"])
def EditDays():
    tor = int(cont.functions.getamnt().call())
    eds = request.form.to_dict()
    index = int(eds["Inde"])
    day = int(eds["Day"])
    rday = cont.functions.editDay(index, day).transact()
    w3.eth.waitForTransactionReceipt(rday)
    get = cont.functions.getfromlist(index).call()
    shy = cont.functions.showday(index).call()
    return render_template("editda.html", get=get, tor=tor, index=index, shd=shy)


@app.route("/editday")
def Editday():
    tor = int(cont.functions.getamnt().call())

    return render_template("editda.html", tor=tor)


@app.route("/editmo")
def Editmo():
    tor = int(cont.functions.getamnt().call())
    return render_template("editmo.html")


@app.route("/editmone", methods=["POST", "GET"])
def EditMons():
    tor = int(cont.functions.getamnt().call())
    eds = request.form.to_dict()
    index = int(eds["index"])
    mon = int(eds["Mon"])
    rmon = cont.functions.editMonth(index, mon).transact()
    w3.eth.waitForTransactionReceipt(rmon)
    get = cont.functions.getfromlist(index).call()
    shy = cont.functions.showmonth(index).call()
    return render_template("editmo.html", get=get, tor=tor, index=index, shm=shy)


@app.route("/editye")
def Edityear():
    tor = int(cont.functions.getamnt().call())
    return render_template("editye.html")


@app.route("/edityes", methods=["POST", "GET"])
def Edityears():
    tor = int(cont.functions.getamnt().call())
    eds = request.form.to_dict()
    index = int(eds["index"])
    yer = int(eds["Yer"])
    ryer = cont.functions.editYear(index, yer).transact()
    w3.eth.waitForTransactionReceipt(ryer)
    get = cont.functions.getfromlist(index).call()
    shy = cont.functions.showyear(index).call()

    return render_template("editye.html", get=get, tor=tor, shy=shy, index=index)


@app.route("/editwho")
def EditWholeList():
    tor = int(cont.functions.getamnt().call())

    return render_template("editlist.html", tor=tor)


@app.route("/editwhole", methods=["POST", "GET"])
def EditWholeLists():
    result = request.form.to_dict()
    index = int(result["index"])
    Action = str(result["Action"])
    Day = int(result["Day"])
    May = int(result["Month"])
    Yay = int(result["Year"])
    edt = cont.functions.editwholeindex(index, Action, Day, May, Yay).transact()
    w3.eth.waitForTransactionReceipt(edt)
    tor = int(cont.functions.getamnt().call())
    get = cont.functions.getfromlist(index).call()
    return render_template("editlist.html", tor=tor, get=get, index=index)
