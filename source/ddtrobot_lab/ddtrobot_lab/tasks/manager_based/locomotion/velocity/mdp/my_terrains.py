import numpy as np
import noise
from isaaclab.terrains.height_field.utils import height_field_to_mesh
from isaaclab.utils import configclass
from isaaclab.terrains.height_field.hf_terrains_cfg import HfTerrainBaseCfg


@height_field_to_mesh
def fractal_perlin_terrain(difficulty: float, cfg: "HfFractalPerlinTerrainCfg") -> np.ndarray:
    
    if cfg.border_width * 2 >= cfg.size[0] or cfg.border_width * 2 >= cfg.size[1]:
        raise ValueError(f"border_width={cfg.border_width} too big over the size:{cfg.size}")

    total_w_px = int(cfg.size[0] / cfg.horizontal_scale)
    total_l_px = int(cfg.size[1] / cfg.horizontal_scale)

    inner_w_m = cfg.size[0] - 2 * cfg.border_width
    inner_l_m = cfg.size[1] - 2 * cfg.border_width
    inner_w_px = int(inner_w_m / cfg.horizontal_scale)
    inner_l_px = int(inner_l_m / cfg.horizontal_scale)

    octaves      = int(np.clip(cfg.octaves + difficulty * 3, 1, 10))
    persistence  = cfg.persistence + difficulty * 0.15
    lacunarity   = float(cfg.lacunarity) if cfg.lacunarity is not None else 2.0
    base_scale   = cfg.base_scale
    scale_factor = cfg.scale_factor
    base_seed    = int(cfg.seed) if cfg.seed is not None else 0

    ix = np.arange(inner_w_px)
    iy = np.arange(inner_l_px)
    xx, yy = np.meshgrid(ix, iy, indexing="ij")

    # 使用 numpy.vectorize 包装 pnoise2
    pnoise2_vec = np.vectorize(
        lambda xi, yi: noise.pnoise2(
            xi * cfg.horizontal_scale / base_scale * scale_factor,
            yi * cfg.horizontal_scale / base_scale * scale_factor,
            octaves=octaves,
            persistence=persistence,
            lacunarity=lacunarity,
            base=base_seed,
        ),
        otypes=[float],
    )
    inner_height = pnoise2_vec(xx, yy)

    h_min, h_max = cfg.height_range
    if inner_height.max() > inner_height.min():
        inner_height = (inner_height - inner_height.min()) / inner_height.ptp()
    else:
        inner_height = np.zeros_like(inner_height)
    inner_height = inner_height * (h_max - h_min) + h_min

    blend_px = int(cfg.blend_distance / cfg.horizontal_scale)
    if blend_px > 0:
        ramp = np.linspace(0, 1, blend_px)
        mask = np.ones_like(inner_height)
        mask[:blend_px, :] *= ramp[:, None]
        mask[-blend_px:, :] *= ramp[::-1, None]
        mask[:, :blend_px] *= ramp[None, :]
        mask[:, -blend_px:] *= ramp[::-1][None, :]
        inner_height = inner_height * mask + h_min * (1 - mask)

    full_height = np.full((total_w_px, total_l_px), fill_value=h_min, dtype=np.float32)
    bx = (total_w_px - inner_w_px) // 2
    by = (total_l_px - inner_l_px) // 2
    full_height[bx : bx + inner_w_px, by : by + inner_l_px] = inner_height

    return np.rint(full_height / cfg.vertical_scale).astype(np.int16)


@configclass
class HfFractalPerlinTerrainCfg(HfTerrainBaseCfg):
    #perlin noise setting

    function = fractal_perlin_terrain

    # --- size ---
    size: tuple[float, float] = (8.0, 8.0)  # (width_x, length_y) in meters
    horizontal_scale: float = 0.05          # grid resolution on X/Y plane (m per cell)
    vertical_scale:   float = 0.005         # grid resolution in Z direction (m per height step)

    # --- flat border around the map ---
    border_width:   float = 0.1             # flat margin on each side (m)
    blend_distance: float = 0             # smooth transition from border to noisy area (m)

    # --- core Perlin-fBm hyper-parameters ---
    base_scale:   float = 2.0               # base divisor for (x,y) coordinates fed to noise
    scale_factor: float = 10.0              # extra frequency multiplier (controls density)
    octaves:      int   = 6                 # number of Perlin layers to stack
    persistence:  float = 0.5               # amplitude decay per octave (0–1)
    lacunarity:   float  = 2.0              # frequency multiplier per octave (≥1);
    height_range: tuple[float, float] = (0.0, 0.12) # physical height range mapped to the normalised noise (m)
    seed:         int  = 42     