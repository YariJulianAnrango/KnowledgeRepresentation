def generate_output(trues,falses, filename):
    outfile = "p cnf 999 729\n" + " 0\n".join([str(trueval) for trueval in trues]) +" 0\n"+ " 0\n".join(["-" + str(falseval) for falseval in falses])
    outtitle = filename + '.out'
    with open(outtitle, 'w') as f:
        f.write(outfile)

