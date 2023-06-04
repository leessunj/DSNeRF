# Depth-supervised NeRF: Fewer Views and Faster Training for Free

[**Project**](https://www.cs.cmu.edu/~dsnerf/) | [**Paper**](https://arxiv.org/abs/2107.02791) | [**YouTube**](https://youtu.be/84LFxCo7ogk)

Original work from [Depth-supervised NeRF: Fewer Views and Faster Training for Free](https://www.cs.cmu.edu/~dsnerf/) CVPR, 2022

<details>
<summary>Original description</summary>
<div markdown="1">
We propose DS-NeRF (Depth-supervised Neural Radiance Fields), a model for learning neural radiance fields that takes advantage of depth supervised by 3D point clouds. Current NeRF methods require many images with known camera parameters -- typically produced by running structure-from-motion (SFM) to estimate poses and a sparse 3D point cloud. Most, if not all, NeRF pipelines make use of the former but ignore the latter. Our key insight is that such sparse 3D input can be used as an additional free signal during training.

<p align="center">
  <img src="figure_teaser.png"  width="800" />
</p>
</div>
</details>

---
## Quick Start

### Dependencies

Install requirements: 이게 정석
```
pip install -r requirements.txt
```
```commandline
conda env create --file dsnerf.yaml
conda activate dsnerf
```
conda init이 안된다면.. (which conda해서 anaconda3이 어딨는지 찾고 자신에게 맞도록 바꾼다.)
```commandline
source /opt/conda/etc/profile.d/conda.sh 
```
libGL import error면.. 
```commandline
apt-get update 
apt-get -y install libgl1-mesa-glx
apt-get install libglib2.0-0
```
Access Tensorboard: 애초에 docker를 *docker run -it -p 6006:6006 ~~~* 이렇게 만들었어야 한다
```
tensorboard --logdir=log/test --port=6006 --host=0.0.0.0
```

### How to Run?

#### Generate camera poses and sparse depth information using COLMAP (optional)

This step is necessary only when you want to run on your data.

First, place your scene directory somewhere. See the following directory structure for an example:
```
├── data
│   ├── fern_2v
│   ├── ├── images
│   ├── ├── ├── image001.png
│   ├── ├── ├── image002.png
```

To generate the poses and sparse point cloud:
```
python imgs2poses.py <your_scenedir>
```

Note: if you use this data format, make sure your `dataset_type` in the config file is set as `llff`.


#### Testing

Once you have the experiment directory (downloaded or trained on your own) in `./logs`, 

- to render a video:
```
python run_nerf.py --config configs/fern_dsnerf.txt --render_only
```

The video would be stored in the experiment directory.

<!-- - to only compute the evaluation metrics:
```
python run_nerf.py --config configs/fern_dsnerf.txt --eval
``` -->


#### Training

To train a DS-NeRF on the example `fern` dataset:
```
python run_nerf.py --config configs/fern_dsnerf.txt
```

It will create an experiment directory in `./logs`, and store the checkpoints and rendering examples there.

You can create your own experiment configuration to try other datasets.

