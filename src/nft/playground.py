from ZapMedia import ZapMedia

params = ["signer", '31337']

zap_media = ZapMedia(*params)
num = 1
floaty = 1.0

print(zap_media.chainId)
print(zap_media.address)
print(zap_media.w3)
# print(zap_media.connect_to_contract())
print(dir(zap_media.contract.functions))
print(zap_media.contract.functions.getOwner().call())