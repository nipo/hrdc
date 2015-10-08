from usage import *

ThreeDGameController = Usage("game.ThreeDGameController", 0x50001, CA)
PinballDevice = Usage("game.PinballDevice", 0x50002, CA)
GunDevice = Usage("game.GunDevice", 0x50003, CA)
PointofView = Usage("game.PointofView", 0x50020, CP)
TurnRightLeft = Usage("game.TurnRightLeft", 0x50021, DV)
PitchForwardBackward = Usage("game.PitchForwardBackward", 0x50022, DV)
RollRightLeft = Usage("game.RollRightLeft", 0x50023, DV)
MoveRightLeft = Usage("game.MoveRightLeft", 0x50024, DV)
MoveForwardBackward = Usage("game.MoveForwardBackward", 0x50025, DV)
MoveUpDown = Usage("game.MoveUpDown", 0x50026, DV)
LeanRightLeft = Usage("game.LeanRightLeft", 0x50027, DV)
LeanForwardBackward = Usage("game.LeanForwardBackward", 0x50028, DV)
HeightofPOV = Usage("game.HeightofPOV", 0x50029, DV)
Flipper = Usage("game.Flipper", 0x5002A, MC)
SecondaryFlipper = Usage("game.SecondaryFlipper", 0x5002B, MC)
Bump = Usage("game.Bump", 0x5002C, MC)
NewGame = Usage("game.NewGame", 0x5002D, OSC)
ShootBall = Usage("game.ShootBall", 0x5002E, OSC)
Player = Usage("game.Player", 0x5002F, OSC)
GunBolt = Usage("game.GunBolt", 0x50030, OOC)
GunClip = Usage("game.GunClip", 0x50031, OOC)
GunSelector = Usage("game.GunSelector", 0x50032, NAry)
GunSingleShot = Usage("game.GunSingleShot", 0x50033, Sel)
GunBurst = Usage("game.GunBurst", 0x50034, Sel)
GunAutomatic = Usage("game.GunAutomatic", 0x50035, Sel)
GunSafety = Usage("game.GunSafety", 0x50036, OOC)
GamepadFireJump = Usage("game.GamepadFireJump", 0x50037, CL)
GamepadTrigger = Usage("game.GamepadTrigger", 0x50039, CL)
