import os
import shutil
import subprocess
import argparse

from multiprocessing import Process


TEST_IDS = ['ID0004', 'ID0012', 'ID0015', 'ID0019', 'ID0032']
FPS_LIST=[20,10,5]

"""
list of dirs to extract the images 
this is used to specify either test or train
"""

class FrameExtractor :
    def __init__(self, args):
        """
        fps_list -> list of fps to extract the test set
        """
        self.root_dir = args.root_dir
        self.out_dir = args.out_dir

    def extract_frames(self,f_name,out_dir_to_save, fps) :
        if not os.path.exists(out_dir_to_save):
            os.makedirs(out_dir_to_save)
    
        cmd = f"ffmpeg -i {f_name} -vf fps={fps} {out_dir_to_save}/frame_%05d.jpg"
        subprocess.run(cmd, shell=True, check=True)
    
    def process_dirs(self,dirs_to_consider, fps=None, out_dir_to_save=None) :
        
        for each_dir in dirs_to_consider :
            file_list = [os.path.join(each_dir,x) for x in os.listdir(each_dir)]
        
        processes = []
        for f_name in file_list :
            p = Process(target=self.extract_frames, args=(f_name, out_dir_to_save, fps))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        
    def extract_all_frames(self, test_ids=TEST_IDS, fps_list=FPS_LIST) :
        test_dirs = [os.path.join(self.root_dir,x) for x in os.listdir(self.root_dir) if x in test_ids]
        train_dirs = [os.path.join(self.root_dir,x) for x in os.listdir(self.root_dir) if x not in test_ids]
        
        # generating train and test frames
        self.process_dirs(train_dirs,os.path.join(self.root_dir,"train"))
        self.process_dirs(test_dirs, os.path.join(self.root_dir,"test"))
        
        for fps in fps_list :
            self.process_dirs(test_dirs, fps, os.path.join(self.root_dir,F"test_{fps}fps"))

def get_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir",type=str,required=True)
    parser.add_argument("--out_dir",type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__" :
    args = get_args()
    fe = FrameExtractor(args)
    fe.extract_all_frames()