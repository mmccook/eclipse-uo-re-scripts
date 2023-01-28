from common import AttunementSelf, AfterCastPause, BlessTarget, ArcaneEmpowermentSelf, GiftOfRenewalTarget, GiftOfLifeTarget

def Buff():
    if(not Player.BuffsExist("Attunement")):
        AttunementSelf()
        AfterCastPause()
    if(not Player.BuffsExist("Gift Of Life")):
        GiftOfLifeTarget(Player.Serial)
        AfterCastPause()
    if(not Player.BuffsExist("Bless")):
        BlessTarget(Player.Serial)
        AfterCastPause()
    if(not Player.BuffsExist("Gift Of Renewal")):
        GiftOfRenewalTarget(Player.Serial)
        AfterCastPause()
    if(not Player.BuffsExist("Arcane Empowerment")):
        ArcaneEmpowermentSelf()
        AfterCastPause()


Buff()
