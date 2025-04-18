fineimport os
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

def train(args, logger):
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
    else:
        print('No pretrained model provided')
    
    # Optimizer and scheduler
    optimizer = torch.optim.Adam(model.parameters(),
        lr=args.lr,
        weight_decay=args.weight_decay,
    )
        
    # Training loop
    logger.info('Start training...')
    try:
        for it in range(1, args.max_iters+1):
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
            wandb.log({
                "train/loss" : loss, 
                "train/lr" : optimizer.param_groups[0]['lr'],
                "train/grad_norm" : orig_grad_norm
            })
            if it % args.val_freq == 0 or it == args.max_iters:
                all_clean = []
                all_denoised = []
                for i, data in enumerate(tqdm(val_dset, desc='Validate')):
                    model.eval()
                    pcl_noisy = data['pcl_noisy'].to(args.device)
                    pcl_clean = data['pcl_clean'].to(args.device)
                    pcl_denoised = patch_based_denoise(model, pcl_noisy, ld_step_size=args.ld_step_size)
                    all_clean.append(pcl_clean.unsqueeze(0))
                    all_denoised.append(pcl_denoised.unsqueeze(0))
                all_clean = torch.cat(all_clean, dim=0)
                all_denoised = torch.cat(all_denoised, dim=0)
                avg_chamfer = chamfer_distance_unit_sphere(all_denoised, all_clean, batch_reduction='mean')[0].item()
                wandb.log({
                    'val/loss': avg_chamfer,
                })
        return avg_chamfer
    except KeyboardInterrupt:
        logger.info('Terminating...')
    
    

############################################################################################################################
#####################################################  MAIN METHOD #########################################################
############################################################################################################################

def main():
    # Arguments
    parser = argparse.ArgumentParser()
    ## Dataset and loader
    parser.add_argument('--dataset_root', type=str, default='./data')
    parser.add_argument('--dataset', type=str, default='SYNTHNet')
    parser.add_argument('--patch_size', type=int, default=1000)
    parser.add_argument('--resolutions', type=str_list, default=['10000', '30000', '50000'])
    parser.add_argument('--noise_min', type=float, default=0.005)
    parser.add_argument('--noise_max', type=float, default=0.020)
    parser.add_argument('--train_batch_size', type=int, default=8)
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
    parser.add_argument('--ckpt', type=str, default='')
    parser.add_argument('--seed', type=int, default=2020)
    parser.add_argument('--logging', type=eval, default=True, choices=[True, False])
    parser.add_argument('--log_root', type=str, default='./logs')
    parser.add_argument('--device', type=str, default='cuda')
    parser.add_argument('--max_iters', type=int, default=100000)
    parser.add_argument('--val_freq', type=int, default=2000)
    parser.add_argument('--val_upsample_rate', type=int, default=4)
    parser.add_argument('--val_num_visualize', type=int, default=4)
    parser.add_argument('--val_noise', type=float, default=0.015)
    parser.add_argument('--ld_step_size', type=float, default=0.2)
    parser.add_argument('--tag', type=str, default=None)
    args = parser.parse_args()
    seed_all(args.seed)

    # start a new wandb run to track this script
    wandb.init(
        # set the wandb project where this run will be logged
        project="narvis-denoise-finetune",
    )
    # Update hyperparameters
    args.lr = wandb.config['lr']
    args.ld_step_size = wandb.config['ld_step_size']
    args.patch_size = wandb.config['patch_size']
    # args.score_net_hidden_dim = wandb.config['score_net_hidden_dim']
    # args.score_net_num_blocks = wandb.config['score_net_num_blocks']
    
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

    # Kaolin Checkpoint Visualization every 5 iterations
    #timelapse = kaolin.visualize.Timelapse('./kaolin_ckpts')
    
    cd_score = train(args, logger)
    wandb.log({'avg_chamfer_distance': cd_score})
    wandb.finish()

if __name__ == "__main__":
    sweep_configuration = {
        'method' : 'random',
        'metric' : {'goal': 'minimize', 'name': 'avg_chamfer_distance'},
        'parameters' : {
            'lr' : {'max': 1e-3, 'min': 1e-4},
            'ld_step_size' : { 'max': 0.3, 'min': 0.2},
            'patch_size' : {'max': 1500, 'min': 1000},
            'score_net_hidden_dim' : {'max': 150, 'min':100},
            'score_net_num_blocks' : {'max': 5, 'min':3},
        }
    }
    sweep_id = wandb.sweep(
        sweep=sweep_configuration, 
        project='narvis-denoise-finetune'
    )
    wandb.agent(sweep_id, function=main, count=100)
    
