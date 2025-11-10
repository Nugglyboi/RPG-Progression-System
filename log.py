import structs

output_file = "data/output.csv"


def record_turn(turn: int, player: structs.Player):
    # TODO make some of these columns debug, this is an excessive amount of information

    if turn == 0:
        with open(output_file, mode="w") as file:
            file.write(
                "Step,PlayerLevel,ActiveBeat#,ActiveBeatName,ZoneLevel,PowerRatio,BeatType,RandCat,OutcomeCategory,SkillDifficulty,Success?,RepDelta,XP_Earned,Gold_Earned,RandQuality,Quality,DropRand,DropSlot,ItemPower,SellValue,SuccessChanceCombat,DeathChance,Death?,RepairCost,Respec?,RespecCost,VendorTaxPct,Gold_Spent,NetGoldChange,CumulativeGold,CumulativeXP,CumulativeRep,GearScoreAvg_UNUSED,PrevCombatCount_UNUSED,Eq_Weapon,Eq_Chest,Eq_Helm,Eq_Legs,Eq_Accessory,GearScore,GearScoreNote,CatStatKey,CategoryDC,BeatDC_lookup,BaseStat,PerLevel,StatScore,TN,SuccessChance_UNI,SuccessChance_NonCombat\n"
            )

    with open(output_file, mode="a") as file:
        file.write(
            f"{turn + 1},{player.level},ActiveBeat#,ActiveBeatName,ZoneLevel,PowerRatio,BeatType,RandCat,OutcomeCategory,SkillDifficulty,Success?,RepDelta,XP_Earned,Gold_Earned,RandQuality,Quality,DropRand,DropSlot,ItemPower,SellValue,SuccessChanceCombat,DeathChance,Death?,RepairCost,Respec?,RespecCost,VendorTaxPct,Gold_Spent,NetGoldChange,CumulativeGold,CumulativeXP,CumulativeRep,GearScoreAvg_UNUSED,PrevCombatCount_UNUSED,Eq_Weapon,Eq_Chest,Eq_Helm,Eq_Legs,Eq_Accessory,GearScore,GearScoreNote,CatStatKey,CategoryDC,BeatDC_lookup,BaseStat,PerLevel,StatScore,TN,SuccessChance_UNI,SuccessChance_NonCombat\n"
        )
