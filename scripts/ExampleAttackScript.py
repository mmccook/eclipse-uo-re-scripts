if Target.HasTarget():
    Target.Cancel()
    Misc.Pause(500)
Spells.Cast("Wildfire")
Target.WaitForTarget(10000, False)
Target.TargetExecute(Player.Serial)
Misc.Pause(1000)
