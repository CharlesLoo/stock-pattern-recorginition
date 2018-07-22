#!/bin/bash

# Configure the resources required
#SBATCH -p gpu                                                  # partition (this is the queue your job will be added to)
#SBATCH -n 1              	                                # number of tasks (sequential job starts 1 task) (check this if your job unexpectedly uses 2 nodes)
#SBATCH -c 1              	                                # number of cores (sequential job calls a multi-thread program that uses 8 cores)
#SBATCH --time=00:20:00                                         # time allocation, which has the format (D-HH:MM), here set to 1 hour
#SBATCH --gres=gpu:1                                            # generic resource required (here requires 2 GPUs)
#SBATCH --mem=16GB                                              # specify memory required per node (here set to 16 GB)

# Configure notifications 
#SBATCH --mail-type=END                                         # Type of email notifications will be sent (here set to END, which means an email will be sent when the job is done)
#SBATCH --mail-type=FAIL                                        # Type of email notifications will be sent (here set to FAIL, which means an email will be sent when the job is fail to complete)
#SBATCH --mail-user=a1699138@student.adelaide.edu.au                    # Email to which notification will be sent

#module load tensorflow/1.0.1-cuda-foss-2016b

module load Python/3.6.1-foss-2016b
source /fast/users/a1699138/virtualenvs/project_py3/bin/activate		# load virtual environemt 

# Execute your script (due to sequential nature, please select proper compiler as your script corresponds to)


export PYTHONPATH=$PYTHONPATH:/fast/users/a1699138/pattern_recognition/train_model/models-master/research:/fast/users/a1699138/pattern_recognition/train_model/models-master/research/slim

cd /fast/users/a1699138/pattern_recognition/train_model/run 

python ../models-master/research/object_detection/eval.py --logtostderr --pipeline_config_path=frcnn_resnet_50.config  --checkpoint_dir=train/ --eval_dir=test


deactivate							#deactivate virtual environment
