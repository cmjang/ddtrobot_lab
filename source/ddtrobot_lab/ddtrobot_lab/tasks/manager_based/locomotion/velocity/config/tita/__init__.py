import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

gym.register(
    id="DDTRobotLab-Velocity-Flat-Tita-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.flat_env_cfg:DDTRobotTitaFlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:DDTRobotTitaFlatPPORunnerCfg",
    },
)

gym.register(
    id="DDTRobotLab-Velocity-Rough-Tita-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:DDTRobotTitaRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:DDTRobotTitaRoughPPORunnerCfg",
    },
)
