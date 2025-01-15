import hidmsr.commands as cmds
import hidmsr.convert as conv

m = cmds.MSRDevice()
m.set_hico()
m.set_bpi(210, 75, 210)

# out = m.read_raw()
out = m.read()

decoded_data = conv.decode_msr_data(out)

specific_part = decoded_data[17:25]
print(decoded_data)
print(specific_part)

# print(conv.extract_data(out))
