# flask is a python web framework. it allows us to send and receive user requests
# with a minimal number of lines of non-web3py code. flask is beyond the scope of
# this tutorial so the flask code won't be commented. that way we can focus on
# how we're working with our smart contract
from flask import Flask, request, render_template,url_for
from elena.emulators.network_emulator import app, add_routes
from threading import Thread
import time
from flask_assets import Environment, Bundle
import numpy as np
#run another contract
import os
from Inspect import QC_simulation
# solc is needed to compile our Solidity code
from solc import compile_source

# web3 is needed to interact with eth contracts
from web3 import Web3, HTTPProvider

# we'll use ConciseContract to interact with our specific instance of the contract
from web3.contract import ConciseContract

# multiprocess
from multiprocessing import Process,Pool

# initialize our flask app
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
app = Flask(__name__)

# Create the Flask-Assets's instance
assets_env = Environment(app)

# Flask-Assets's config
# Can not compress the CSS/JS on Dev environment.
app.config['ASSETS_DEBUG'] = True
app.config['AUTOPREFIXER_BIN'] = basedir + '/node_modules/postcss-cli/bin/postcss'
app.config['AUTOPREFIXER_BROWSERS'] = ['> 1%', 'last 2 versions', 'firefox 24', 'opera 12.1']

# Define the set for js and css file.
css = Bundle(
    'css/style.css',
    filters='autoprefixer6, cssmin',
    output='assets/css/common.css')

js = Bundle(
    'js/jquery.js',
    'js/jparticle.min.js',
    filters='jsmin',
    output='assets/js/common.js')

# register
assets_env.register('js', js)
assets_env.register('css', css)

# declare the candidates we're allowing people to vote for.
# note that each name is in bytes because our contract variable
# candidateList is type bytes32[]
DATA_RECORD = [b'Production time', b'Transport time',b'Inspection time',b'Address',b'Winners',b'State',b'Results']

# open a connection to the local ethereum node
http_provider = HTTPProvider('http://localhost:8545')
eth_provider = Web3(http_provider).eth

# we'll use one of our default accounts to deploy from. every write to the chain requires a
# payment of ethereum called "gas". if we were running an actual test ethereum node locally,
# then we'd have to go on the test net and get some free ethereum to play with. that is beyond
# the scope of this tutorial so we're using a mini local node that has unlimited ethereum and
# the only chain we're using is our own local one
default_account = eth_provider.accounts[0]
# every time we write to the chain it's considered a "transaction". every time a transaction
# is made we need to send with it at a minimum the info of the account that is paying for the gas
transaction_details = {
    'from': default_account,
}

# load our Solidity code into an object
with open('inspect.sol') as file:
    source_code = file.readlines()

# compile the contract
compiled_code = compile_source(''.join(source_code))

# store contract_name so we keep our code DRY
contract_name = 'Insepection'

# lets make the code a bit more readable by storing these values in variables
contract_bytecode = compiled_code[f'<stdin>:{contract_name}']['bin']
contract_abi = compiled_code[f'<stdin>:{contract_name}']['abi']
# the contract abi is important. it's a json representation of our smart contract. this
# allows other APIs like JavaScript to understand how to interact with our contract without
# reverse engineering our compiled code

# create a contract factory. the contract factory contains the information about the
# contract that we probably will not change later in the deployment script.
contract_factory = eth_provider.contract(
    abi=contract_abi,
    bytecode=contract_bytecode,
)

# here we pass in a list of smart contract constructor arguments. our contract constructor
# takes only one argument, a list of candidate names. the contract constructor contains
# information that we might want to change. below we pass in our list of voting candidates.
# the factory -> constructor design pattern gives us some flexibility when deploying contracts.
# if we wanted to deploy two contracts, each with different candidates, we could call the
# constructor() function twice, each time with different candidates.
contract_constructor = contract_factory.constructor(DATA_RECORD)

# here we deploy the smart contract. the bare minimum info we give about the deployment is which
# ethereum account is paying the gas to put the contract on the chain. the transact() function
# returns a transaction hash. this is like the id of the transaction on the chain
transaction_hash = contract_constructor.transact(transaction_details)

# if we want our frontend to use our deployed contract as it's backend, the frontend
# needs to know the address where the contract is located. we use the id of the transaction
# to get the full transaction details, then we get the contract address from there
transaction_receipt = eth_provider.getTransactionReceipt(transaction_hash)
contract_address = transaction_receipt['contractAddress']

contract_instance = eth_provider.contract(
    abi=contract_abi,
    address=contract_address,
    # when a contract instance is converted to python, we call the native solidity
    # functions like: contract_instance.call().someFunctionHere()
    # the .call() notation becomes repetitive so we can pass in ConciseContract as our
    # parent class, allowing us to make calls like: contract_instance.someFunctionHere()
    ContractFactoryClass=ConciseContract,
)

inspection_information = {}
product_information = {}
Product_ID = []
Inspector_ID= []
STATE = {}
output_information={'product_0':{'product_time':0,
        'transport_time':0,'Inspection time':0,'Address':0,'Winners':0,'State':0,'Results':'false'}}


@app.route('/', methods=['GET', 'POST'])
def index():

    alert = ''
    select_id = 0
    state = request.form.get('Score')
    if request.method == 'POST' and state:
        product_id = request.form.get('product_id')
        inspector_id = request.form.get('inspector_id')
        inspector_confidence = request.form.get('inspector_co')
        inspection_time = request.form.get('Inspection_time')
        product_id=int(product_id)
        inspector_id=int(inspector_id)
        inspector_confidence = float(inspector_confidence)
        inspection_time=int(inspection_time)
        state = int(state)
        if product_id not in Product_ID:
            Product_ID.append(product_id)
            contract_instance.initial(product_id)
            product_information.update({f'product_{product_id}':{}})
            print(inspector_confidence)
            STATE.update({f'product_{product_id}':{'inspector_confidence'
            :{f'state_{state}':inspector_confidence,'inspection_time':inspection_time,'inspector_id':inspector_id},'state':[state]}})
        if inspector_id not in Inspector_ID:
            Inspector_ID.append(inspector_id)
            inspection_information.update({f'inspector_{inspector_id}':{}})

        inspection_information[f'inspector_{inspector_id}'].update({f'product_{product_id}':{
            'product_id':product_id,
            'inspector_confidence':inspector_confidence,
            'inspection_time':inspection_time,
            'state':state
        }})

        if state not in STATE[f'product_{product_id}']['state']:
            STATE[f'product_{product_id}']['state'].append(state)
            STATE[f'product_{product_id}']['inspector_confidence'].update({f'state_{state}':inspector_confidence,
              'inspection_time':inspection_time,'inspector_id':inspector_id})

        elif state in STATE[f'product_{product_id}']['state'] and \
                inspector_id!=STATE[f'product_{product_id}']['inspector_confidence']['inspector_id']:
            new_c =  STATE[f'product_{product_id}']['inspector_confidence'][f'state_{state}']+inspector_confidence
            STATE[f'product_{product_id}']['inspector_confidence'].update({f'state_{state}':new_c})

        #check consensus

        for i in Product_ID:
            for j in STATE[f'product_{i}']['state']:
                s = int((STATE[f'product_{i}']['inspector_confidence'][f'state_{j}'])*10)
                print(s)
                it = int(STATE[f'product_{i}']['inspector_confidence']['inspection_time'])
                Ins_id = int(STATE[f'product_{i}']['inspector_confidence']['inspector_id'])
                contract_instance.consensus(i,j,it,s,Ins_id,transact=transaction_details)

            # contract_instance.checkProductnum(product_id,transact=transaction_details)
    transport_time = request.form.get('Transport_time')
    if request.method == 'POST' and transport_time:
        production_time = request.form.get('Production_time')
        product_id = request.form.get('product_id')
        production_time=int(production_time)
        transport_time=int(transport_time)
        product_id = int(product_id)
        print(product_id)
        contract_instance.setProduct(product_id, production_time, transport_time,
                                      transact=transaction_details)
    # the web3py wrapper will take the bytes32[] type returned by getCandidateList()
    # and convert it to a list of strings
    property_names = contract_instance.getList()
    propertylist = []
    for i in Product_ID:
        pt,tt,it,ad,wi,s,r=contract_instance.getinformation(i)
        output_information.update({f'product_{i}': {'product_time':pt,
        'transport_time':tt,'Inspection time':it,'Address':ad,'Winners':wi,'State':s,'Results':r}})
    print(output_information)
    # solidity doesn't yet understand how to return dict/mapping/hash like objects
    # so we have to loop through our names and fetch the current vote total for each one.
    select_id = request.form.get('select_option')
    if request.method == 'POST' and select_id:
        select_id = int(select_id)

    if select_id:
       valuelist=output_information[f'product_{select_id}'].values()
    else:
        valuelist = output_information[f'product_0'].values()
    print(valuelist)
    for property_names in property_names:

        candidate_name_string = property_names.decode().rstrip('\x00')
        propertylist.append(candidate_name_string)
    candidates = dict(zip(propertylist,valuelist))
    if len(Product_ID) > 0:
      Product_ID.sort()
      max = Product_ID[len(Product_ID) - 1]
      min = Product_ID[0]
    else:
        max=0
        min=0

    return render_template('index.html',candidates=candidates,max=max,min=min,alert=alert)
def run():
    app.run()
    time.sleep(1)
def inspect():
    os.system("python ./Inspect.py")
    time.sleep(1)
if __name__ == '__main__':
    # set debug=True for easy development and experimentation
    # set use_reloader=False. when this is set to True it initializes the flask app twice. usually
    # this isn't a problem, but since we deploy our contract during initialization it ends up getting
    # deployed twice. when use_reloader is set to False it deploys only once but reloading is disabled
    a = Thread(target=run)
    # b = Thread(target=inspect)
    a.start()
    # b.start()







