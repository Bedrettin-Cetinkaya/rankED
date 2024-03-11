_base_ = [
    '../_base_/models/upernet_swin.py', '../_base_/datasets/nyud_hha.py',
    '../_base_/default_runtime.py', '../_base_/schedules/schedule_160k.py'
]

norm_cfg = dict(type='BN', requires_grad=True)

model = dict(
    backbone=dict(
        embed_dim=128,
        depths=[2, 2, 18, 2],
        num_heads=[4, 8, 16, 32],
        window_size=12,
        ape=False,
        drop_path_rate=0.3,
        patch_norm=True,
        use_checkpoint=False
    ),
    decode_head=dict(
        in_channels=[128, 256, 512, 1024],
        num_classes=1
    ),
auxiliary_head=[dict(
        type='FCNHead',
        in_channels=128,
        in_index=0,
        channels=64,
        num_convs=1,
        concat_input=False,
        dropout_ratio=0.1,
        num_classes=1,
        norm_cfg=norm_cfg,
        align_corners=False,
        loss_decode=dict(
            type='HEDLoss', use_sigmoid=True, loss_weight=0.4)),
        dict(
        type='FCNHead',
        in_channels=256,
        in_index=1,
        channels=128,
        num_convs=1,
        concat_input=False,
        dropout_ratio=0.1,
        num_classes=1,
        norm_cfg=norm_cfg,
        align_corners=False,
        loss_decode=dict(
            type='HEDLoss', use_sigmoid=True, loss_weight=0.4)),
        dict(
        type='FCNHead',
        in_channels=512,
        in_index=2,
        channels=256,
        num_convs=1,
        concat_input=False,
        dropout_ratio=0.1,
        num_classes=1,
        norm_cfg=norm_cfg,
        align_corners=False,
        loss_decode=dict(
            type='HEDLoss', use_sigmoid=True, loss_weight=0.4))
            
         ])

# AdamW optimizer, no weight decay for position embedding & layer norm in backbone
optimizer = dict(_delete_=True, type='AdamW', lr=0.00006, betas=(0.9, 0.999), weight_decay=0.01,
                 paramwise_cfg=dict(custom_keys={'absolute_pos_embed': dict(decay_mult=0.),
                                                 'relative_position_bias_table': dict(decay_mult=0.),
                                                 'norm': dict(decay_mult=0.)}))

lr_config = dict(_delete_=True, policy='poly',
                 warmup='linear',
                 warmup_iters=1500,
                 warmup_ratio=1e-6,
                 power=1.0, min_lr=0.0, by_epoch=False)

# By default, models are trained on 8 GPUs with 2 images per GPU
#data=dict(samples_per_gpu=2)
test_cfg = dict(mode='slide', crop_size=(320, 320), stride=(280, 280))
find_unused_parameters = True
data = dict(samples_per_gpu=4)

