torchrun --standalone --nnodes 1 --nproc-per-node 8 vla-scripts/generate_llavadata.py \
  --pretrained_checkpoint /data/jcy/ckpt/openvla-7b-prismatic/checkpoints/step-295000-epoch-40-loss=0.2200.pt \
  --vla.type prism-siglip-224px+mx-jcy \
  --data_mix diversity \
  --data_root_dir /data/jcy/data/openx_part/convered \
  --llavadata_root_dir /data/jcy/data/openx_part/llava \
  --image_aug False \
