
import os
import time
import subprocess
import shutil
from config import *

def run_cmd(cmd):
    output = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, universal_newlines=True)
    return output.stdout

def write_log(logstr):
    print(logstr)
    with open(FILE_MATCHLOG, "a") as matchlogfile:
        matchlogfile.write(logstr + "\n")

#Get all weight file in DIR_PARENTS
def get_all_weight(weight_dir):
    files = os.listdir(weight_dir)
    all_weight = []
    for file in files:
        if file.endswith(".txt"):
            all_weight.append(file)
    return all_weight
    

#silent delete file
def silent_remove(filename):
    try:
        os.remove(filename)
    except OSError as e: # this would be "except OSError, e:" before Python 2.6
        if e.errno != errno.ENOENT: # errno.ENOENT = no such file or directory
            raise # re-raise exception if a different error occurred
            

def remove_temp_files():
    files = os.listdir(DIR_WORK)
    for file in files:
       if file == "leelazero.dat" or file == "leelazero.lock" or file == "leelazero.html" or file == "leelazero.summary.dat" or file.endswith(".sgf"):
           silent_remove(file)

#match 2 weight
def match_weight(weight1, weight2):
    
    while os.path.isfile("leelazero.dat") or os.path.isfile("leelazero.lock"):
        time.sleep(1)
        remove_temp_files()
    
    
    matchcmd = MATCH_CMD.format(GOGUI_TWOGTP_CMD, LEELAZERO_CMD, MATCH_PLAYOUT, weight1, weight2, MATCH_TIMES)
    print(matchcmd)
    match_result = run_cmd(matchcmd)
    print(match_result)
    
    if not os.path.isfile("leelazero.dat"):
       #maybe weight file is error
       return [MATCH_TIMES,1,1,1,1,1,1,1,1]
    
    while not os.path.isfile("leelazero.summary.dat"):
        time.sleep(1)
        analyzecmd = MATCH_ANALYZE_CMD.format(GOGUI_TWOGTP_CMD)
        print(analyzecmd)
        analyze_result = run_cmd(analyzecmd)
        print(analyze_result)
    
    with open("leelazero.summary.dat", "rt") as matchresultfile:
        matchresultfile.readline()
        matchresult = matchresultfile.readline().split()
        return matchresult
    

def log_matchresult(match_result, weightb, weightw):
    print("%s vs %s :" %(weightb, weightw))
    print("    %s" % match_result)
    gamecount = int(match_result[0])
    bwinrate = float(match_result[6])
    bwincount = round(gamecount*bwinrate)
    wwinrate = 1-bwinrate
    wwincount = gamecount - bwincount
    print("    %s(%.2f) : %s(%.2f)" %(bwincount, bwinrate*100, wwincount, wwinrate*100))
    write_log("{0} vs {1} :{2}({3}%) : {4}({5}%)".format(weightb, weightw, bwincount, bwinrate*100, wwincount, wwinrate*100))
    

def child_match_dir(child_dir, child_dir_weight, match_dir):
    
     #match best weight with parent
     match_dir_weights = get_all_weight(match_dir)
     
     for match_dir_weight in match_dir_weights:
         match_result = match_weight(os.path.join(child_dir, child_dir_weight), os.path.join(match_dir, match_dir_weight))
         log_matchresult(match_result, child_dir_weight, match_dir_weight)
        

def findbest(child_dir):
    write_log(" ")
    write_log("----------------------------------------------------------------")
    write_log("-- START ROUND TO FIND THE BEST OF CHILD --")
    #get child
    child_weights = get_all_weight(child_dir)
    print("All Child Weight: %s"%  child_weights)
    
    #change to work direction
    if not os.path.exists(DIR_WORK):
        os.makedirs(DIR_WORK)
    
    os.chdir(DIR_WORK)
    
    # match child weight
    if (len(child_weights)>1):
        #find best weight
        best_weight = ""
        for child_weight in child_weights:
            if best_weight == "":
                print("King change to %s" % child_weight)
                best_weight = child_weight
            else:
                match_result = match_weight(os.path.join(child_dir, best_weight), os.path.join(child_dir, child_weight))
                log_matchresult(match_result, best_weight, child_weight)
                if float(match_result[6]) < 0.5:
                    print("King change to %s" % child_weight)
                    best_weight = child_weight
        
        
        write_log("----------------------------------------------------------------")
        write_log("-- MATCH WITH PARENT AND OTHER BEST WEIGHT --")
        
        if child_dir == DIR_CHILDREN:
            child_match_dir(child_dir, best_weight, DIR_BEST)
        child_match_dir(child_dir, best_weight, DIR_PARENTS)
        
        write_log("----------------------------------------------------------------")
        write_log("This ROUND Hybrid Child KING is {0}".format(best_weight))
        write_log("----------------------------------------------------------------")
        write_log(" ")
        return best_weight
    elif len(child_weights) == 1:
        print("Only One Child! ")
        return child_weights[0]
    else:
        print("Child weight's count < 1, Exit!")
        return ""


def findbestchild():
    best_child = findbest(DIR_CHILDREN)
    
    if (best_child != "") :
        write_log("Move %s to best direction!" % best_child)
        shutil.copyfile(os.path.join(DIR_CHILDREN, best_child), os.path.join(DIR_BEST, best_child) )
    
    files = os.listdir(DIR_CHILDREN)
    for file in files:
       if file.endswith(".txt"):
           silent_remove(os.path.join(DIR_CHILDREN, file))


# find best child weight
def findbestbest():
    write_log("  ")
    write_log("  ")
    write_log("----------------------------------------------------------------")
    write_log("-- START TO FIND THE BEST OF BEST --")
    
    best_best = findbest(DIR_BEST)
    
    write_log("----------------------------------------------------------------")
    write_log("The LAST Hybrid Child KING is {0}".format(best_best))
    write_log("----------------------------------------------------------------")
        

if __name__ == '__main__':
    findbestbest()