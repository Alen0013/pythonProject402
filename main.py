
from command import LightOnCommand, LightOffCommand
from light import Light
from remote_control import RemoteControl

if __name__ == "__main__":
    # Create the receiver
    light = Light()

    # Create the commands
    light_on = LightOnCommand(light)
    light_off = LightOffCommand(light)

    # Create the invoker
    remote = RemoteControl()

    # Turn the light on
    remote.set_command(light_on)
    remote.press_button()  # Output: Light is ON

    # Turn the light off
    remote.set_command(light_off)
    remote.press_button()  # Output: Light is OFF