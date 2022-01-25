import os
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)




class ClassGenerator():
    def __init__(self, contract_name:str, path_to_put_file:str = os.path.dirname(os.path.realpath(__file__))):
        self.contract_name = contract_name
        self.path_to_put_file = path_to_put_file
        self.get_ABI(contract_name)      
        pass

    def get_ABI(self, contract_name:str):
            with open(f'src/artifacts/{contract_name.lower()}.json', 'r') as f:
                artifact = json.load(f)
            self.abi = artifact['abi']
            
            # self.address = artifact[self.chainId]['address']
            # self.contract = self.w3.eth.contract(address=self.address, abi=self.abi)

    def create_file(self):
        filename = f"{self.contract_name.lower()}.py"
        where_to_create = self.path_to_put_file
        # Creating a file at specified location
        with open(os.path.join(where_to_create, filename), 'w') as new_file:
            pass
            new_file.write(self.generate_head())

    def generate_head(self):
        head = f"""from base_contract import BaseContract

class {self.contract_name}(BaseContract):

    def __init__(self, chainId):
        super().__init__(chainId) 
        try:
            self.connect_to_contract("ZapMedia")            
        except Exception as e:
            print(e)
        """
        return head
    

gen = ClassGenerator("ZapMedia")
gen.create_file()  

    
        
# params = ["zapmedia", "./test_zap_media.py"]
# zap_media = ClassGenerator(*params)

# # print(zap_media)
# # print(zap_media.abi)
# functions = {}
# abi = zap_media.abi
# for obj in abi:
#     # pp.pprint(obj)
#     if obj['type'] == 'function':
#         functions[obj['name']] = {}
#         functions[obj['name']]['input'] = obj['inputs']
#         # print(obj['name'])

# pp.pprint(functions)



