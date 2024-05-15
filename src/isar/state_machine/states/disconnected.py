import logging
import time
from typing import Optional, TYPE_CHECKING

from transitions import State

from isar.models.communication.message import StartMissionMessage

if TYPE_CHECKING:
    from isar.state_machine.state_machine import StateMachine


class Disconnected(State):
    def __init__(self, state_machine: "StateMachine") -> None:
        super().__init__(name="disconnected", on_enter=self.start, on_exit=self.stop)
        self.state_machine: "StateMachine" = state_machine
        self.logger = logging.getLogger("state_machine")

    def start(self) -> None:
        self.state_machine.update_state()
        self._run()

    def stop(self) -> None:
        pass

    def _run(self) -> None:
        while True:
            if self.state_machine.is_robot_connected():
                transition = self.state_machine.reconnected  # type: ignore
                break
            time.sleep(self.state_machine.sleep_time)

        transition()
