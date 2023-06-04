import sys
import numpy as np
from scipy.spatial.transform import Rotation as Rot
import os

def read_images_txt(images_path):
    if not os.path.exists(images_path):
        raise Exception(f"No such file : {images_path}")
    with open(images_path, 'r') as f:
        lines = f.readlines()
    if len(lines) < 2:
        raise Exception(f"Invalid cameras.txt file : {images_path}")
    comments = lines[:4]
    contents = lines[4:]

    img_ids = []
    cam_ids = []
    img_names = []
    poses = []
    for img_idx, content in enumerate(contents[::2]):
        content_items = content.split(' ')
        img_id = content_items[0]
        q_xyzw = np.array(content_items[2:5] + content_items[1:2], dtype=np.float32) # colmap uses wxyz
        t_xyz = np.array(content_items[5:8], dtype=np.float32)
        cam_id = content_items[8]
        img_name = content_items[9]

        R = Rot.from_quat(q_xyzw).as_matrix()
        T = np.eye(4)
        T[:3, :3] = R
        T[:3, -1] = t_xyz
        img_ids.append(img_id)
        cam_ids.append(cam_id)
        img_names.append(img_name)
        poses.append(T)

    return img_ids, cam_ids, img_names, poses
def from_points(filepath):
    sys.stdin=open(f"{filepath}/points3D.txt",'r')
    n1 = input()

    n2 = input()#   POINT3D_ID, X, Y, Z, R, G, B, ERROR, TRACK[] as (IMAGE_ID, POINT2D_IDX)
    n3 = input()

    line=input()
    points={}
    pt3d, x, y, z, r, g, b, err, *track = map(float, line.split())
    points[pt3d]={'xyz':[x,y,z], 'rgb':[r,g,b], 'err':err}
    # for i in range(15079):
    #     line=input()
    # tracks={}
    while line:
        pt3d,x,y,z,_,_,_,err,*track=map(float,line.split())
        points[pt3d] = {'xyz': [x, y, z], 'rgb': [r, g, b], 'err': err, 'track':track}
        # tracks[pt3d]=list(map(int,track))
        try:
            line=input()
        except:
            break

    np.save(f'{filepath}/point3s.npy', points)


def from_images(filepath,img_num):
    sys.stdin = open(f"{filepath}/images.txt", 'r')
    n1 = input()
    n2 = input()
    n3 = input()
    n4 = input()
    #   IMAGE_ID, QW, QX, QY, QZ, TX, TY, TZ, CAMERA_ID, NAME #   POINTS2D[] as (X, Y, POINT3D_ID)
    points2d = {}
    for i in range(img_num):
        if i % 2 == 0:
            n = input()
            print(n)
        else:
            n = list(map(float, input().split()))
            new_list = []
            for j in range(0, len(n), 3):
                # if n[j+2]==-1:
                #     continue
                new_list.append(np.array(n[j:j + 3]))
            points2d[(i // 2) + 1] = np.array(new_list)
    # print(points2d)
    np.save(f'{filepath}/point2s.npy', points2d)

    print(len(points2d.keys()),len(points2d[2]),points2d[2])
    # print(points2d[4][616], points2d[5][2224], points2d[3][597], points2d[1][5411], points2d[2][4876],points2d[15][10351])
filepath="data/comb_d/"
# from_images("data/comb_d/",14)
# from_points("data/comb_d/")
read_images_txt(f'{filepath}images.txt')

pt2d=np.load(f'{filepath}/point2s.npy', allow_pickle=True).item()
pt3d=np.load(f'{filepath}/point3s.npy', allow_pickle=True).item()
cnt=0
# for i in range(2224):
#     if l.item()[5][i][2]==-1:
#         cnt+=1
# print(cnt)
# print(l.item()[4][616])
# print(l.item()[5][2224])
# print(l.item()[3][597])

# img_ids, cam_ids, img_names, poses=read_images_txt("images.txt")
# np.save('pose_c2w.npy',np.linalg.inv(poses) )
# l=np.load('pose_c2w.npy', allow_pickle=True)
# print(l)