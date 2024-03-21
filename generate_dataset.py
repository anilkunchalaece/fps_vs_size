import os
import shutil
import subprocess
import argparse
import sys

from multiprocessing import Process


FPS_LIST=[20,15,10,7,5,3,1]
RESOLUTION_LIST=["640:480","320:240","160:120","128:96"]

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
        self.dataset = args.dataset
        
        if self.dataset == 'mcad' :
            self.TEST_IDS = ['ID0004', 'ID0012', 'ID0015', 'ID0019', 'ID0032']
        else :
            self.TEST_IDS = [17, 18, 19, 20]

    def extract_frames(self,f_name,out_dir_to_save, fps, resolution=None) :
        if self.dataset == 'mcad' :
            out_dir_to_save = os.path.join(out_dir_to_save, os.path.basename(f_name).split(".")[0])
        else :
            f_split = f_name.split(os.sep) 
            out_dir_to_save = os.path.join(out_dir_to_save,F"{f_split[-5]}_{f_split[-4]}_{f_split[-3]}_{f_split[-2]}_{f_split[-1].split('.')[0]}")
        if not os.path.exists(out_dir_to_save):
            os.makedirs(out_dir_to_save)
        if fps == None :    
            cmd = f"ffmpeg -i {f_name} {out_dir_to_save}/img_%05d.jpg"
        elif resolution == None :
            cmd = f"ffmpeg -i {f_name} -vf fps={fps} {out_dir_to_save}/img_%05d.jpg"
        else :
            cmd = f'ffmpeg -i {f_name} -vf "fps={fps},scale={resolution}" {out_dir_to_save}/img_%05d.jpg'
        subprocess.run(cmd, shell=True, check=True)
    
    def process_dirs(self,all_files, out_dir_to_save=None, fps=None,resolution=None) :
            
        processes = []
        for f_name in all_files :
            p = Process(target=self.extract_frames, args=(f_name, out_dir_to_save, fps, resolution))
            p.start()
            processes.append(p)

        for p in processes:
            p.join()
    
    def extract_all_frames_at_resolutions(self, fps=10, resolutions=RESOLUTION_LIST) :
        test_dirs = [os.path.join(self.root_dir,x) for x in os.listdir(self.root_dir) if x in self.TEST_IDS and \
            os.path.isdir(os.path.join(self.root_dir,x))]

        for resolution in resolutions :
            self.process_dirs(test_dirs,os.path.join(self.out_dir,F"test_{fps}fps_{resolution.replace(':','x')}"), fps, resolution)

        
    def extract_all_frames(self, fps_list=FPS_LIST) :
        
        if self.dataset == 'mcad' :
            test_dirs = [os.path.join(self.root_dir,x) for x in os.listdir(self.root_dir) if x in self.TEST_IDS and \
                os.path.isdir(os.path.join(self.root_dir,x))]
            train_dirs = [os.path.join(self.root_dir,x) for x in os.listdir(self.root_dir) if x not in self.TEST_IDS and \
                os.path.isdir(os.path.join(self.root_dir,x))]

            train_files = []
            test_files = []
            
            for idx, each_dir in enumerate([train_dirs, test_dirs]) :
                file_list = [os.path.join(each_dir,x) for x in os.listdir(each_dir)]
                if idx == 0 :
                    train_files.extend(file_list)
                else :
                    test_files.extend(file_list)
                        
        elif self.dataset == 'mmact' : 
            
            all_subject_dirs = os.listdir(self.root_dir)
            test_files = []
            train_files = []
            
            for each_subject_dir in all_subject_dirs :
                cam_dirs = os.listdir(os.path.join(self.root_dir,each_subject_dir))
                for each_cam_dir in cam_dirs :
                    scene_dirs = os.listdir(os.path.join(self.root_dir,each_subject_dir,each_cam_dir))
                    for each_scene_dir in scene_dirs :
                        all_sessions = os.listdir(os.path.join(self.root_dir,each_subject_dir, each_cam_dir, each_scene_dir))
                        for each_session in all_sessions :
                            all_videos = os.listdir(os.path.join(self.root_dir,each_subject_dir, each_cam_dir, each_scene_dir,each_session))
                            for each_video in all_videos :
                                video_full_name = os.path.join(self.root_dir,each_subject_dir, each_cam_dir, each_scene_dir,each_session, each_video)
                                if int(each_subject_dir.replace('subject','')) in self.TEST_IDS :
                                    test_files.append(video_full_name)
                                else :
                                    train_files.append(video_full_name)
        
        # generating train and test frames
        self.process_dirs(train_files,os.path.join(self.out_dir,"train"))
        self.process_dirs(test_files, os.path.join(self.out_dir,"test"))
                
        for fps in fps_list :
            self.process_dirs(test_files,os.path.join(self.out_dir,F"test_{fps}fps"), fps)


def generate_annotations(root_dir_name, ann_file_name, dataset_type) :
    mmact_classes = ['carrying', 'carrying_heavy', 'carrying_light','checking_time', 
                     'closing', 'crouching', 'entering', 'exiting', 'fall', 'jumping', 
                     'kicking', 'loitering', 'looking_around', 'opening', 'picking_up', 
                     'pointing', 'pulling', 'pushing', 'running', 'setting_down', 'standing', 
                     'talking', 'talking_on_phone', 'throwing', 'transferring_object', 'using_phone',
                     'walking', 'waving_hand', 'drinking', 'pocket_in', 'pocket_out', 'sitting',
                     'sitting_down', 'standing_up', 'talking_on_phone_desk', 'using_pc',
                     'using_phone_desk'] # total 37
    all_dirs = [ os.path.join(root_dir_name,x) for x in os.listdir(root_dir_name)]
    annotations = []
    
    
    for dir_name in all_dirs :
        if dataset_type == 'mcad' :
            annotations.append(F"{os.path.basename(dir_name)} {len(os.listdir(dir_name))} {int(os.path.basename(dir_name).split('A')[-1][:2])-1}\n")
        else :
            base_dir = os.path.basename(dir_name).split('_')
            if len(base_dir) == 5 :
                class_name = base_dir[-1]
            else :
                class_name = "_".join(base_dir[4:])
            class_name = class_name.lower()
            annotations.append(F"{os.path.basename(dir_name)} {len(os.listdir(dir_name))} {mmact_classes.index(class_name)}\n")
    
    with open(ann_file_name,'w') as fw:
        fw.writelines(annotations)
    
    print(F"annotations are saved to {ann_file_name}")


def get_args() :
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir",type=str,required=True)
    parser.add_argument("--out_dir",type=str, required=True)
    parser.add_argument("--act", type=str,required=True)
    parser.add_argument("--dataset", type=str, default='mcad')
    return parser.parse_args()

if __name__ == "__main__" :
    args = get_args()
    
    if args.act == "extract" :
        fe = FrameExtractor(args)
        fe.extract_all_frames()
        # fe.extract_all_frames_at_resolutions(fps=10)
    else :
        for each_dir in os.listdir(args.root_dir) :
            each_dir = os.path.join(args.root_dir,each_dir)
            if os.path.isdir(each_dir) : 
                generate_annotations(each_dir, os.path.join(args.out_dir,F"{os.path.basename(each_dir)}_annotations.txt"), args.dataset)
