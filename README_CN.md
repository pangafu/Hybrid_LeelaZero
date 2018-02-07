# 1. Hybrid_LeelaZero
这个项目的想法是来自于 leela zero 问题 #814 https://github.com/gcp/leela-zero/issues/814

这个项目会将两个或者更多的权重进行混血，然后自动比赛，找出最好的混血权重。

# 2. 怎么运行
# 2.1 运行前准备 （windows环境和linux都测试过）
Python 3.5 or higher  (https://www.python.org/) 

Leela Zero  (https://github.com/gcp/leela-zero)

GoGUI  (https://sourceforge.net/projects/gogui/)

# 2.2 下载一代权重文件
从以下网址下载你喜欢的第一代权重文件 
  
  http://zero.sjeng.org/
 
  http://zero.sjeng.org/networks/

然后将 xxxxxxxx.gz 文件放到 parents\ 目录下
 
最后的文件结构就像这样

    parents\
 
       0c5522ba97ddafb9b854889451a651ef0fce19fb0e10dd6b0ba9ca1af476b793.gz

       9efb2c7a8b03f134b7f0436d6dc8aa991fe9eddea7293c7782167d0788a78964.gz
 
       27af5a26c264cc90ad9949b5cfccf3d03f44827e5b19b5373c181037e029e52c.gz
 
       ... ...

# 2.3 编写配置文件
请打开 config.py, 修改以下配置文件:


    LEELAZERO_CMD   :  LeelaZero 的命令行 (整个命令行中最好不要有空格)
    GOGUI_TWOGTP_CMD  :  GOGUI gogui-twogtp 的命令行 (整个命令行中最好不要有空格)
    MATCH_PER_GAMES  :  当产生了多少个混血权重后，开始一轮新的比赛
    MATCH_PLAYOUT  :  比赛参数Playout，建议至少>60，越大越好
    MATCH_TIMES  :  每两个权重的比赛次数，建议至少>20次，越大越好
    HYBRID  :  混血参数
        HybridParameter: 目前最多支持5个权重同时混血，如果你需要支持更多，请修改hybrid.py->gen_children
        RandomInherit: (0-1)随机继承参数，如果开启这个参数，混血权重的某个网络参数将以一定比例从父权重中继承，主要用于 突变目的
  
如果还是不太明白的话，请参考程序注释。

# 2.4 运行
在windows或者linux下，请用以下方法进行运行
 
 
     python main.py

运行的过程大概如下


    a. 首先根据父权重和混血参数，生成混血子权重
    b. 当生成的混血子权重数量 > MATCH_PER_GAMES，开始一轮比赛，找出这批子权重中最强的权重
    c. 将最强的子权重移动到 best\ 目录中
    d. 重复 b 和 c 步骤，每一批混血权重找出一个最强混血子权重
    e. 最后，测试所有在 best\ 目录下的权重，找出最后的混血权重之王
    

所有的比赛信息都可以在 matchlog\match.log 中看到，就像以下这个样子:


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
 
