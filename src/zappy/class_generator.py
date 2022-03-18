import os
import json
import pprint
pp = pprint.PrettyPrinter(indent=4)




class ClassGenerator():
    def __init__(self, contract_name:str, path_to_file:str = os.path.dirname(os.path.realpath(__file__))):
        self.contract_name = contract_name
        self.path_to_file = path_to_file
        self.get_ABI(contract_name)      
        pass

    def get_ABI(self, contract_name:str):
            with open(f'src/nft/artifacts/{contract_name.lower()}.json', 'r') as f:
                artifact = json.load(f)
            self.abi = artifact['abi']
            
            # self.address = artifact[self.chainId]['address']
            # self.contract = self.w3.eth.contract(address=self.address, abi=self.abi)

    def create_file(self):
        filename = f"{self.contract_name.lower()}.py"
        where_to_create = self.path_to_file
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
            self.connect_to_contract({self.contract_name}.__name__)
        except Exception as e:
            print(e)
        """
        return head

    def generate_functions(self):
        filename = f"{self.contract_name.lower()}.py"
        path_to_file = self.path_to_file
        with open(os.path.join(path_to_file, filename), 'a') as new_file:
            # pass
            for obj in self.abi:
                if obj['type'] == 'function':
                    func_name = obj['name']
                    func_inputs = ClassGenerator.get_params(obj['inputs'])
                    stateMutability = obj['stateMutability']
                    # params = func_inputs[0:]
                    temp = ClassGenerator.generate_function_str(func_name, func_inputs, stateMutability)
                    
                    # print(temp)

                    new_file.write(temp)
            # pass
    
    @staticmethod
    def get_params(inputs):
        params = []
        for input in inputs:
            if input['name'] in ["from", "to"]:
                params.append("_"+input['name'])
            else:
                params.append(input['name'])
        params = (", ").join(params)
        return params
    
    @staticmethod
    def generate_function_str(function_name, function_params, stateMutability):
     return f"""
    def {function_name}(self, {function_params}):
        return self.contract.functions.{function_name}({function_params})
            """

# zap_media = ClassGenerator("ZapMedia")
# zap_media.create_file()  
# zap_media.generate_functions()

# zap_market = ClassGenerator("ZapMarket")
# zap_market.create_file()  
# zap_market.generate_functions()

# auction_house = ClassGenerator("AuctionHouse")
# auction_house.create_file()  
# auction_house.generate_functions()

# mf = ClassGenerator("MediaFactory")
# mf.create_file()  
# mf.generate_functions()

zap_token = ClassGenerator("ZapTokenBSC")
zap_token.create_file()
zap_token.generate_functions()