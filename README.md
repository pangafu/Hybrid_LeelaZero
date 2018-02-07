
# 1. Hybrid_LeelaZero
Idea come from the leela zero issue #814 https://github.com/gcp/leela-zero/issues/814

This program will auto hybrid 2 or more weight file by HybridParameter, and auto test to find the strongest hybrid weight

# 2. How to run
# 2.1 requirment
Python 3.5 or higher  (https://www.python.org/) 

Leela Zero  (https://github.com/gcp/leela-zero)

GoGUI  (https://sourceforge.net/projects/gogui/)

# 2.2 Download the Parent weights
Download leela zero weights you loved from 
  
  http://zero.sjeng.org/
 
  http://zero.sjeng.org/networks/

And put the xxxxxxxx.gz file into parents\ fold
 
Just look like

    parents\
 
       0c5522ba97ddafb9b854889451a651ef0fce19fb0e10dd6b0ba9ca1af476b793.gz

       9efb2c7a8b03f134b7f0436d6dc8aa991fe9eddea7293c7782167d0788a78964.gz
 
       27af5a26c264cc90ad9949b5cfccf3d03f44827e5b19b5373c181037e029e52c.gz
 
       ... ...

# 2.3 Modify the config file
Please open config.py, modify parameters:


    LEELAZERO_CMD   :  LeelaZero Command (no blank in dir)
 
    GOGUI_TWOGTP_CMD  :  GOGUI gogui-twogtp  Command (no blank in dir)
    
    MATCH_PER_GAMES  :  Match when generated N game in child
    
    MATCH_PLAYOUT  :  Match Playout to test which weight is strong
  
    MATCH_TIMES  :  Math times Count to test which weight is strong,

    HYBRID  :  Hybrid Parameter
  
         HybridParameter: Max 5 weight to Hybrid , if wanner more, please modify hybrid.py->gen_children
  
         RandomInherit: percent to random inherited from one parent, for Mutation porpose
  
It's very easy to understand, if not know , please see the program commet.

# 2.4 run
In windows or linux, use 

     python main.py

It will do something like

     a. Generate hybrid child with Hybrid Parameter and parent weights
     
     b. Test to find the best child when generated child count > MATCH_PER_GAMES
  
     c. Move the best child into best\ direction
  
     d. Repeat STEP b and c to generate 1 best child in MATCH_PER_GAMES games
  
     e. At last, find the best weight in best\ direction
    

All the result you can see from the console output and matchlog\match.log, just like below:


    ----------------------------------------------------------------
    -- START ROUND TO FIND THE BEST OF CHILD --
    0c5-27a_1-1.txt vs 0c5-54b_1-1.txt :10(100.0%) : 0(0.0%)
    0c5-27a_1-1.txt vs 0c5-9ef_1-1.txt :5(50.0%) : 5(50.0%)
    0c5-27a_1-1.txt vs 27a-54b_1-1.txt :5(50.0%) : 5(50.0%)
    ----------------------------------------------------------------
    -- MATCH WITH PARENT AND OTHER BEST WEIGHT --
    0c5-27a_1-1.txt vs 0c5522ba97ddafb9b854889451a651ef0fce19fb0e10dd6b0ba9ca1af476b793.txt :10(100.0%) : 0(0.0%)
    0c5-27a_1-1.txt vs 27af5a26c264cc90ad9949b5cfccf3d03f44827e5b19b5373c181037e029e52c.txt :5(50.0%) : 5(50.0%)
    0c5-27a_1-1.txt vs 54bfb7b8324539c486cf191214abeb9d10dce667ba7469ac12e34069718f219a.txt :5(50.0%) : 5(50.0%)
    0c5-27a_1-1.txt vs 9efb2c7a8b03f134b7f0436d6dc8aa991fe9eddea7293c7782167d0788a78964.txt :5(50.0%) : 5(50.0%)
    ----------------------------------------------------------------
    This ROUND Hybrid Child KING is 0c5-27a_1-1.txt
    ----------------------------------------------------------------
 
  
