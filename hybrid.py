
import gzip, binascii, os
import itertools
import random
from best import *
from config import *

childnum = 0

#Uncompress .gz file to other file
def uncompress_file(fn_in, fn_out):  
    print("uncompress %s -> %s" % (fn_in, fn_out))
    f_in = gzip.open(fn_in, 'rb')  
    f_out = open(fn_out, 'wb')  
    file_content = f_in.read()  
    f_out.write(file_content)  
    f_out.close()  
    f_in.close()  
    
#Uncompress all weight xxx.gz file to xxx.txt in DIR_PARENTS
def uncompress_parent():
    files = os.listdir(DIR_PARENTS)
    for file in files:
        if file.endswith(".gz"):
            file_pre = file[:-3]
            file_weight = file_pre + ".txt"
            
            if file_weight not in files:
                uncompress_file(os.path.join(DIR_PARENTS, file), os.path.join(DIR_PARENTS, file_weight))
                
#Get all parent weight file in DIR_PARENTS
def get_all_parent():
    files = os.listdir(DIR_PARENTS)
    all_weight = []
    for file in files:
        if file.endswith(".txt"):
            all_weight.append(file)
    return all_weight

#See if child has generate or not need generate
def check_genchild_paramter(had_generated_pair, weights_pair, hbparam):
    #not generate pair with same weight
    for weight in weights_pair:
        if weights_pair.count(weight)>1:
        	return False
        	
    #not generate pair had generated
    key_paramter = []
    for weight_param in zip(weights_pair, hbparam):
        key_paramter.append(weight_param[0] + ":" +  weight_param[1] + "&&")
    key_paramter.sort()
    
    key_index = "".join(str(x) for x in key_paramter)
    
    if key_index in had_generated_pair:
        return False
        
    had_generated_pair.append(key_index)
    return True

#Generate one child by one parameter
def gen_child(weights_pair, hbparam, randominherit):
    #weight file name
    weightname = "".join((x[:3] + "-") for x in weights_pair)
    weightname = weightname[:-1]
    weightname = weightname + "_"
    hbparamname = "".join((str(x)+ "-") for x in hbparam)
    hbparamname = hbparamname[:-1]
    weightname = weightname + hbparamname
    if (randominherit>0):
        weightname = weightname + "_" + str(randominherit)
    
    weightname = weightname + ".txt"
    print(weightname)
    
    #load all parent weight file
    parent_weights_files = []
    for filename in weights_pair:
        parent_weights_files.append(open(os.path.join(DIR_PARENTS,filename), "rt"))
    
    child_weight_file = open(os.path.join(DIR_CHILDREN,weightname), "wt")
    
    #write child weight file
    n = 0
    while n>=0:
        n = n + 1
        if n == 1:
            #write 1 in first line
            child_weight_file.write("1")
            for parent_weights_file in parent_weights_files:
                parent_weights_file.readline()
        else:
            #init 1 line array
            linearray_list = []
            for parent_weights_file in parent_weights_files:
                file_line = parent_weights_file.readline()
                if file_line:
                    line_array = [float(x) for x in file_line.split()]
                    linearray_list.append(line_array)
                else:
                    #read end , quit loop
                    n = -1
                    break
            
            if n == -1:
                break;
            child_weight_file.write('\n')
            #write child file
            if len(linearray_list[0])>0:
                for i in range(0, len(linearray_list[0])):
                    float_value = 0
                    hb_value = 0
                    for j in range(0, len(linearray_list)):
                        float_value = float_value + linearray_list[j][i]*float(hbparam[j])
                        hb_value = hb_value + float(hbparam[j])
                    float_value = float_value/hb_value
                    
                    #random inherited
                    if (randominherit>0):
                        percent = random.random()
                        if (percent<randominherit):
                            index = random.randint(0, len(linearray_list))
                            float_value = linearray_list[j][i]
                        
                    child_weight_file.write('%g ' % (float_value))
                
                
    child_weight_file.close()
    for file in parent_weights_files:
        file.close()

#Generate children by one parameter
def gen_children(all_parent_weight, parameter, randominherit):
    hbparam = parameter.split(":")
    
    des_parent_weights = []
    if len(hbparam) == 2:
        des_parent_weights = itertools.product(all_parent_weight, all_parent_weight)
    
    if len(hbparam) == 3:
        des_parent_weights = itertools.product(all_parent_weight, all_parent_weight, all_parent_weight)
    
    if len(hbparam) == 4:
        des_parent_weights = itertools.product(all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight)

    if len(hbparam) == 5:
        des_parent_weights = itertools.product(all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight)

    if len(hbparam) == 6:
        des_parent_weights = itertools.product(all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight)

    if len(hbparam) == 7:
        des_parent_weights = itertools.product(all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight, all_parent_weight)

    had_generated_pair = []
    for weights_pair in des_parent_weights:
        #check if weight need generate
        need_gen = check_genchild_paramter(had_generated_pair, weights_pair, hbparam)
        if need_gen :
            global childnum
            childnum = childnum + 1
            gen_child(weights_pair, hbparam, randominherit)
            
            #match after MATCH_PER_GAMES
            if childnum>=MATCH_PER_GAMES:
                findbestchild()
                childnum = 0

#Main function
def hybrid():
    print("-- STEP 1: Uncompress All parent weight file --")
    uncompress_parent()
    print("")
    print("-- STEP 2: Generate Hybrid Weight --")
    all_parent_weight = get_all_parent()
    print("All Parent weight File: %s" % all_parent_weight)
    
    for hybrid_pattern in HYBRID:
        print(">>Generate Hybrid Children with %s" % hybrid_pattern )
        gen_children(all_parent_weight, hybrid_pattern["HybridParameter"], float(hybrid_pattern["RandomInherit"]))
    
    findbestchild()

if __name__ == '__main__':
    hybrid()