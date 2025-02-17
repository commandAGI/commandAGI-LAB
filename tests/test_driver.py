import pytest
from commandagi_j2.envs.local_pynput_computer_env import LocalPynputComputeEnv
from commandagi_j2.agents.simple_computer_agent import SimpleComputerAgent
from unittest.mock import MagicMock, patch

from commandagi_j2.utils.gym2.basic_driver import BasicDriver
from commandagi_j2.utils.gym2.in_memory_collector import InMemoryDataCollector


class TestDriver:
    @pytest.fixture
    def mock_env(self):
        env = MagicMock(spec=LocalPynputComputeEnv)
        env.reset.return_value = "test_screenshot.png"
        env.step.return_value = (
            "test_screenshot.png",
            1.0,
            False,
            {"action_success": True},
        )
        return env

    @pytest.fixture
    def mock_agent(self):
        agent = MagicMock()
        agent.reset = MagicMock()
        agent.act = MagicMock(return_value="click 100,100")
        agent.update = MagicMock()
        return agent

    @pytest.fixture
    def driver(self, mock_env, mock_agent):
        collector = InMemoryDataCollector(save_dir="test_data")
        return BasicDriver(env=mock_env, agent=mock_agent, collector=collector)

    def test_run_episode(self, driver, mock_env, mock_agent):
        with patch("time.sleep"):  # Skip sleep delays
            reward = driver.run_episode(max_steps=3, episode_num=0)

            assert isinstance(reward, float)
            assert mock_env.reset.called
            assert mock_agent.reset.called
            assert mock_env.step.call_count == 3
            assert mock_agent.act.call_count == 3
