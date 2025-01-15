import hidmsr.commands as cmds
import hidmsr.convert as conv
import utils

m = cmds.MSRDevice()
m.set_hico()
m.set_bpi(210, 75, 210)

# out = m.read_raw()
out = m.read()

data = conv.decode_msr_data(out)
parsedData = utils.extract_id(data)

print(data)
print(parsedData)

# print(conv.extract_data(out))
