import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

gym.register(
    id="DDTRobotLab-Velocity-Flat-Tita-LSTM-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.flat_env_cfg:DDTRobotTitaLstmFlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:DDTRobotTitaLstmFlatPPORunnerCfg",
    },
)

gym.register(
    id="DDTRobotLab-Velocity-Rough-Tita-LSTM-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:DDTRobotTitaLstmRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:DDTRobotTitaLstmRoughPPORunnerCfg",
    },
)
