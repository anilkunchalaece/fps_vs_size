## Testing the performance of FPS and Image Size on the Action Classification

### Overview
I'm using MCAD dataset
ref - https://ieeexplore.ieee.org/document/7926611
dataset - https://zenodo.org/records/884592

All person id's -> ['0001', '0003', '0004', '0005', '0007', '0008', '0012', '0013', '0014', '0015', '0016', '0017', '0018', '0019', '0020', '0023', '0026', '0027', '0030', '0032']

test_ids = ['0004', '0012', '0015', '0019', '0032']

all other id's are train ids


### Steps to follow
1. Extract the frames using the fixed frame rate for Training
2. Extract the testing frames with various frame rates
    - [org/30, 20, 10, 5]
3. Train the action recognition model using Train data
4. Evalauate the model with test data across different frame rates



