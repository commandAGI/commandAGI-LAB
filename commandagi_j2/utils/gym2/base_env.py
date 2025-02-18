from abc import ABC, abstractmethod
from typing import Dict, Tuple, List, NewType

# Define common type aliases for the environment and related modules
Observation = NewType("Observation", str)
Action = NewType("Action", str)
Step = Tuple[Observation, Action]
Trajectory = List[Step]
Mandate = NewType("Mandate", str)


class Env(ABC):
    """Abstract base class for environments."""

    def reset(self) -> Observation:
        """Reset the environment and return initial observation."""
        observation = self.get_observation()
        return observation

    @abstractmethod
    def close(self):
        """Clean up environment resources.
        
        This method should be implemented by subclasses to properly clean up any resources
        like network connections, file handles, or external processes that need to be
        explicitly closed or terminated.
        """
        pass

    def step(self, action: Action) -> Tuple[Observation, float, bool, Dict]:
        """Execute action and return (observation, reward, done, info).

        Args:
            action (Action): Action to execute

        Returns:
            observation (Observation): Environment observation
            reward (float): Reward from the action
            done (bool): Whether episode has ended
            info (Dict): Additional information
        """
        """Execute an action and return the next observation, reward, done, and info."""
        success = self.execute_action(action)
        if not success:
            raise ValueError(f"Action {action} failed to execute")
        observation = self.get_observation()
        reward = self.get_reward(action)
        done = self.get_done(action)
        info = self.get_info()
        return observation, reward, done, info

    @abstractmethod
    def get_observation(self) -> Observation:
        """Get the current observation from the environment.

        This method should be implemented by subclasses to return the current state observation.
        """

    @abstractmethod
    def execute_action(self, action: Action) -> Observation:
        """Execute an action and return the observation.

        Args:
            action (Action): The action to execute

        """

    @abstractmethod
    def get_reward(self, action: Action) -> float:
        """Get the reward for an action.

        Args:
            action (Action): The action that was executed

        Returns:
            float: The reward for the action
        """

    @abstractmethod
    def get_done(self, action: Action) -> bool:
        """Get the done flag for an action.

        Returns:
            bool: Whether the episode is done
        """

    def get_info(self) -> Dict:
        """Get the info for an action.

        Returns:
            Dict: Additional information
        """
        return {}
