import os
import argparse
import torch
import torch.utils.tensorboard
from torch.utils.data import DataLoader
from torch.nn.utils import clip_grad_norm_
from tqdm.auto import tqdm

from datasets import *
from utils.misc import *
from utils.transforms import *
from utils.denoise import *
from models.denoise import *
from models.utils import chamfer_distance_unit_sphere
import kaolin 
import wandb

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument('--kaolin_interval', type=int, default=5000)
parser.add_argument('--kaolin_ckpts_dir', type=str, default=None)
parser.add_argument('--wandb_samples', type=int, default=8)
## Dataset and loader
parser.add_argument('--dataset_root', type=str, default='./data')
parser.add_argument('--dataset', type=str, default='SYNTHNet')
parser.add_argument('--patch_size', type=int, default=1000)
parser.add_argument('--resolutions', type=str_list, default=['10000', '30000', '50000'])
parser.add_argument('--noise_min', type=float, default=0.001)
parser.add_argument('--noise_max', type=float, default=0.017)
parser.add_argument('--train_batch_size', type=int, default=16)
parser.add_argument('--val_batch_size', type=int, default=8)
parser.add_argument('--num_workers', type=int, default=4)
parser.add_argument('--aug_rotate', type=eval, default=True, choices=[True, False])
## Model architecture
parser.add_argument('--supervised', type=eval, default=True, choices=[True, False])
parser.add_argument('--frame_knn', type=int, default=32)
parser.add_argument('--num_train_points', type=int, default=128)
parser.add_argument('--num_clean_nbs', type=int, default=4, help='For supervised training.')
parser.add_argument('--num_selfsup_nbs', type=int, default=8, help='For self-supervised training.')
parser.add_argument('--dsm_sigma', type=float, default=0.01)
parser.add_argument('--score_net_hidden_dim', type=int, default=128)
parser.add_argument('--score_net_num_blocks', type=int, default=4)
## Optimizer and scheduler
parser.add_argument('--lr', type=float, default=1e-4)
parser.add_argument('--weight_decay', type=float, default=0)
parser.add_argument('--max_grad_norm', type=float, default=float("inf"))
## Training
parser.add_argument('--seed', type=int, default=2020)
parser.add_argument('--logging', type=eval, default=True, choices=[True, False])
parser.add_argument('--log_root', type=str, default='./logs')
parser.add_argument('--device', type=str, default='cuda')
parser.add_argument('--ckpt', type=str, default='./pretrained/ckpt.pt')

# parser.add_argument('--max_iters', type=int, default=1*MILLION)
parser.add_argument('--max_iters', type=int, default=100000)
parser.add_argument('--val_freq', type=int, default=2000)
parser.add_argument('--val_upsample_rate', type=int, default=4)
parser.add_argument('--val_num_visualize', type=int, default=3)
parser.add_argument('--val_noise', type=float, default=0.017)
parser.add_argument('--ld_step_size', type=float, default=0.2)
parser.add_argument('--tag', type=str, default=None)
args = parser.parse_args()
seed_all(args.seed)

# args.lr =  0.06974908884223924
# args.ld_step_size = 0.2
# args.patch_size = 1315
# args.score_net_hidden_dim = 128
# args.score_net_num_blocks = 4

# Logging
if args.logging:
    log_dir = get_new_log_dir(args.log_root, prefix='D%s_' % (args.dataset), postfix='_' + args.tag if args.tag is not None else '')
    logger = get_logger('train', log_dir)
    writer = torch.utils.tensorboard.SummaryWriter(log_dir)
    ckpt_mgr = CheckpointManager(log_dir)
    log_hyperparams(writer, log_dir, args)
else:
    logger = get_logger('train', None)
    writer = BlackHole()
    ckpt_mgr = BlackHole()
logger.info(args)

# start a new wandb run to track this script
wandb.init(
    # set the wandb project where this run will be logged
    project="narvis-denoise-final",
    
    # track hyperparameters and run metadata
    config={
    "learning_rate": args.lr,
    "ld_step_size" : args.ld_step_size,
    "patch_size": args.patch_size,
    "hidden_size": args.score_net_hidden_dim,
    "num_blocks": args.score_net_num_blocks,
    "dataset": args.dataset,
    "pretrained": "yes" if args.ckpt != '' else "no",
    "epochs": args.max_iters,
    }
)

# Register Kaolin checkpoints directory
timelapse = kaolin.visualize.Timelapse(args.kaolin_ckpts_dir)

# Datasets and loaders
logger.info('Loading datasets')
train_dset = PairedPatchDataset(
    datasets=[
        IsaacSimDataset(
            root=args.dataset_root,
            dataset=args.dataset,
            split='train',
            resolution=resl,
            transform=standard_train_transforms(noise_std_max=args.noise_max, noise_std_min=args.noise_min, rotate=args.aug_rotate)
        ) for resl in args.resolutions
    ],
    patch_size=args.patch_size,
    patch_ratio=1.2,
    on_the_fly=True  
)
val_dset = IsaacSimDataset(
        root=args.dataset_root,
        dataset=args.dataset,
        split='test',
        resolution=args.resolutions[0],
        transform=standard_train_transforms(noise_std_max=args.val_noise, noise_std_min=args.val_noise, rotate=False, scale_d=0),
    )
train_iter = get_data_iterator(DataLoader(train_dset, batch_size=args.train_batch_size, num_workers=args.num_workers, shuffle=True))

# Model
logger.info('Building model...')
model = DenoiseNet(args).to(args.device)
logger.info(repr(model))

# Loading Pretrained weights if provided 
if args.ckpt != '':
    ckpt = torch.load(args.ckpt, map_location=args.device)
    model.load_state_dict(ckpt['state_dict'])
    print("Loaded Pretrained model")


# Optimizer and scheduler
optimizer = torch.optim.Adam(model.parameters(),
    lr=args.lr,
    weight_decay=args.weight_decay,
)

# Train, validate and test
def train(it):
    # Load data
    batch = next(train_iter)
    pcl_noisy = batch['pcl_noisy'].to(args.device)
    pcl_clean = batch['pcl_clean'].to(args.device)

    # Reset grad and model state
    optimizer.zero_grad()
    model.train()

    # Forward
    if args.supervised:
        loss = model.get_supervised_loss(pcl_noisy=pcl_noisy, pcl_clean=pcl_clean)
    else:
        loss = model.get_selfsupervised_loss(pcl_noisy=pcl_noisy)

    # Backward and optimize
    loss.backward()
    orig_grad_norm = clip_grad_norm_(model.parameters(), args.max_grad_norm)
    optimizer.step()

    # Logging
    logger.info('[Train] Iter %04d | Loss %.6f | Grad %.6f' % (
        it, loss.item(), orig_grad_norm,
    ))
    writer.add_scalar('train/loss', loss, it)
    writer.add_scalar('train/lr', optimizer.param_groups[0]['lr'], it)
    writer.add_scalar('train/grad_norm', orig_grad_norm, it)
    writer.flush()
    wandb.log({
        "train/loss" : loss, 
        "train/lr" : optimizer.param_groups[0]['lr'],
        "train/grad_norm" : orig_grad_norm
    })

def validate(it):
    all_clean = []
    all_denoised = []
    gt_samples = []
    out_samples = []
    for i, data in enumerate(tqdm(val_dset, desc='Validate')):
        pcl_noisy = data['pcl_noisy'].to(args.device)
        pcl_clean = data['pcl_clean'].to(args.device)
        pcl_denoised = patch_based_denoise(model, pcl_noisy, ld_step_size=args.ld_step_size)
        all_clean.append(pcl_clean.unsqueeze(0))
        all_denoised.append(pcl_denoised.unsqueeze(0))
        if i < args.wandb_samples:
            gt_samples.append(wandb.Object3D({
                "type" : "lidar/beta",
                "points" : pcl_clean.cpu().numpy()
            }))

            out_samples.append(wandb.Object3D({
                "type" : "lidar/beta",
                "points" : pcl_denoised.cpu().numpy()
            }))
    all_clean = torch.cat(all_clean, dim=0)
    all_denoised = torch.cat(all_denoised, dim=0)
    # Register Kaolin checkpoint
    if it % args.kaolin_interval == 0:
        timelapse.add_pointcloud_batch(category='groundtruth',
                                    iteration=it,
                                pointcloud_list=all_clean)
        timelapse.add_pointcloud_batch(category='output',
                                    iteration=it,
                                pointcloud_list=all_denoised)
    
    avg_chamfer = chamfer_distance_unit_sphere(all_denoised, all_clean, batch_reduction='mean')[0].item()

    logger.info('[Val] Iter %04d | CD %.6f  ' % (it, avg_chamfer))
    writer.add_scalar('val/chamfer', avg_chamfer, it)
    writer.add_mesh('val/pcl', all_denoised[:args.val_num_visualize], global_step=it)
    writer.flush()
    wandb.log({
        'val/loss': avg_chamfer,
        "groundtruth" : gt_samples,
        "denoised" : out_samples
    })
    # scheduler.step(avg_chamfer)
    return avg_chamfer

# Main loop
logger.info('Start training...')
try:
    for it in range(1, args.max_iters+1):
        train(it)
        if it % args.val_freq == 0 or it == args.max_iters:
            cd_loss = validate(it)
            opt_states = {
                'optimizer': optimizer.state_dict(),
                # 'scheduler': scheduler.state_dict(),
            }
            ckpt_mgr.save(model, args, cd_loss, opt_states, step=it)
            # ckpt_mgr.save(model, args, 0, opt_states, step=it)

except KeyboardInterrupt:
    logger.info('Terminating...')
