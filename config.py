import os

# - LeelaZero Command (no blank in dir)- 
#Windows
#LEELAZERO_CMD = "E:\go\leelazero\win64\leelaz.exe"
#Linux
LEELAZERO_CMD = "/home/wukong/leela-zero/src/leelaz"

# - GOGUI gogui-twogtp  Command (no blank in dir)-
#Windows
#GOGUI_TWOGTP_CMD = "E:\go\gogui\win64\gogui-twogtp.exe"
#Linux
GOGUI_TWOGTP_CMD = "/home/wukong/gogui/bin/gogui-twogtp"


# - math when N game in child -
MATCH_PER_GAMES = 100

# - match Playout to test which weight is strong -
MATCH_PLAYOUT = 200

# - math times Count to test which weight is strong -
MATCH_TIMES = 40



# - match command-
MATCH_CMD = '{0} -black "{1} -g -m 30 -p {2} --noponder -t 1 -q -d -r 1 -w {3}"  -white "{1} -g -m 30 -p {2} --noponder -t 1 -q -d -r 1 -w {4}" -games {5} -sgffile leelazero -size 19 -komi 7.5 -alternate -auto'
MATCH_ANALYZE_CMD = "{0} -analyze leelazero.dat"

# - Dir list -
DIR_RUN = os.path.abspath('.')
DIR_PARENTS = os.path.join(DIR_RUN, "parents")
DIR_CHILDREN = os.path.join(DIR_RUN, "children")
DIR_WORK = os.path.join(DIR_RUN, "work")
DIR_BEST = os.path.join(DIR_RUN, "best")
FILE_MATCHLOG  = os.path.join(DIR_RUN, "matchlog", "match.log")

# - Hybrid Parameter -
#HybridParameter: Max 7 weight to Hybrid , if wanner more, please modify hybrid.py->gen_children
#RandomInherit: percent to random inherited from one parent, for Mutation porpose

HYBRID = [{"HybridParameter":"1:1:1:1:1", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.8:0.8:0.8:0.8", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.5:0.5:0.5:0.5", "RandomInherit":"0"},
                 {"HybridParameter":"1:1:1:1:1:1", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.8:0.8:0.8:0.8:0.8", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.5:0.5:0.5:0.5:0.5", "RandomInherit":"0"}]

"""
HYBRID = [{"HybridParameter":"1:1", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.8", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.5", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.2", "RandomInherit":"0"},
                 {"HybridParameter":"1:1:1", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.8:0.8", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.5:0.5", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.2:0.2", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.7:0.3", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.9:0.7", "RandomInherit":"0"},
                 {"HybridParameter":"1:1:1:1", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.8:0.8:0.8", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.9:0.7:0.5", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.8:0.5:0.2", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.5:0.5:0.5", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.2:0.2:0.2", "RandomInherit":"0"},
                 {"HybridParameter":"1:1:1:1:1", "RandomInherit":"0"},
                 {"HybridParameter":"1:0.8:0.6:0.4:0.2", "RandomInherit":"0"}]
"""