import os
import shutil
import subprocess
import argparse
import sys

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
        out_dir_to_save = os.path.join(out_dir_to_save, os.path.basename(f_name).split(".")[0])
        if not os.path.exists(out_dir_to_save):
            os.makedirs(out_dir_to_save)
        if fps == None :    
            cmd = f"ffmpeg -i {f_name} {out_dir_to_save}/frame_%05d.jpg"
        else :
            cmd = f"ffmpeg -i {f_name} -vf fps={fps} {out_dir_to_save}/frame_%05d.jpg"
        subprocess.run(cmd, shell=True, check=True)
    
    def process_dirs(self,dirs_to_consider, out_dir_to_save=None, fps=None,) :
        
        all_files = []
        for each_dir in dirs_to_consider :
            file_list = [os.path.join(each_dir,x) for x in os.listdir(each_dir)]
            all_files.extend(file_list)
            
        processes = []
        for f_name in all_files :
            p = Process(target=self.extract_frames, args=(f_name, out_dir_to_save, fps))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()

        
    def extract_all_frames(self, test_ids=TEST_IDS, fps_list=FPS_LIST) :
        test_dirs = [os.path.join(self.root_dir,x) for x in os.listdir(self.root_dir) if x in test_ids and \
            os.path.isdir(os.path.join(self.root_dir,x))]
        train_dirs = [os.path.join(self.root_dir,x) for x in os.listdir(self.root_dir) if x not in test_ids and \
            os.path.isdir(os.path.join(self.root_dir,x))]
        
        
        # generating train and test frames
        self.process_dirs(train_dirs,os.path.join(self.out_dir,"train"))
        self.process_dirs(test_dirs, os.path.join(self.out_dir,"test"))
        
        for fps in fps_list :
            self.process_dirs(test_dirs,os.path.join(self.out_dir,F"test_{fps}fps"), fps)


def generate_annotations(root_dir_name, ann_file_name) :
    all_dirs = [ os.path.join(root_dir_name,x) for x in os.listdir(root_dir_name)]
    annotations = []
    for dir_name in all_dirs :
        annotations.append(F"{os.path.basename(dir_name)} {len(os.listdir(dir_name))} {os.path.basename(dir_name).split('A')[-1][:2]}\n")
    
    with open(ann_file_name,'w') as fw:
        fw.writelines(annotations)
    
    print(F"annotations are saved to {ann_file_name}")


def get_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir",type=str,required=True)
    parser.add_argument("--out_dir",type=str, required=True)
    return parser.parse_args()

if __name__ == "__main__" :
    args = get_args()
    # fe = FrameExtractor(args)
    # fe.extract_all_frames()
    
    for each_dir in os.listdir(args.root_dir) :
        each_dir = os.path.join(args.root_dir,each_dir)
        if os.path.isdir(each_dir) : 
            generate_annotations(each_dir, os.path.join(args.out_dir,F"{os.path.basename(each_dir)}_annotations.txt"))