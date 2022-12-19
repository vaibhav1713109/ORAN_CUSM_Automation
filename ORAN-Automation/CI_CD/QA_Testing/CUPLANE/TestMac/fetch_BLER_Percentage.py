def fetch_BLER_Percentage_list(filename):
    file = open(filename,'r+')
    lines = file.readlines()

    li = []
    i = 0
    while i < len(lines):
        if "kbps           UL BLER      Num CB" in lines[i]:
                li.append(lines[i+2])
                i+=2
        i+=1

        
    import re
    bler_values = []
    for val in li:
        bler_column = val.split("|")
        #  print(bler_column)
        values = re.split(r'\s{2,}',bler_column[4])
        bler_values.append(values[3])
    return bler_values


if __name__ == "__main__":
     filename = '/home/sebu.mathew/QA_CICD/QA_Testing/shegna/16AugConig_execute_TestMac/ul_qpsk1_ch1.txt'
     bler_val = fetch_BLER_Percentage_list(filename)
     print(bler_val)
     pass
