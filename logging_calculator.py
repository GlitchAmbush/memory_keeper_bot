tiers = [3, 5, 8, 13, 17, 20]
gold = [30, 80, 150, 250, 400, 500]
xp = [300, 500, 700, 800, 1000]
wph: int = 600 # 18 WPM * 60 minutes

def get_tier_and_scaled_rewards(player_levels: list, words: list):
    rp_wph = round(len(words) / wph)
    
    # debug
    print("\nWords: ", len(words))
    print("WPH: ",rp_wph)

    for i in range(len(tiers)):
        tier: int = tiers[i]
        if isinstance(player_levels, list):
            p_level_value: int = player_levels[0]  # Assuming it's a single value list
        else:
            p_level_value: int = player_levels
            
        if p_level_value >= tier:
            if i == len(tiers) - 1 or p_level_value < tiers[i + 1]:
                scaled_gold: int = gold[min(i, len(gold) - 1)] * rp_wph
                scaled_xp: int = xp[min(i, len(xp) - 1)] * rp_wph
                return tier, scaled_gold, scaled_xp, rp_wph
    return None, None, None, None

def print_rewards_info(player_levels: list, words: list):
    desc_list: list[str] = []
    desc_str: str = ''
    
    for level in player_levels:
        tier, scaled_gold, scaled_xp, rp_wph = get_tier_and_scaled_rewards(level, words)
        desc_list.append(f'''\n**Hours of RP:** {rp_wph}
**Level:** {level}
**Gold:** {scaled_gold}gp
**XP:** {scaled_xp}''')
    
    for desc in desc_list:
        desc_str += f'\n{desc}'
    return desc_str


# TESTING
def test_rewards_calc(player_levels: list, words: list, rp_duration: int):
    alpha = 1.07
    pwr = 4

    rp_wph = len(words) / wph
    effective_hrs = alpha * rp_duration * (1 - 1 / (1 + rp_wph/rp_duration) ** pwr) / 3600
    for i in range(len(tiers)):
        tier: int = tiers[i]
        if isinstance(player_levels, list):
            p_level_value: int = player_levels[0]  # Assuming it's a single value list
        else:
            p_level_value: int = player_levels

        if p_level_value >= tier:
            if i == len(tiers) - 1 or p_level_value < tiers[i + 1]:
                scaled_gold: int = round(gold[min(i, len(gold) - 1)] * effective_hrs)
                scaled_xp: int = round(xp[min(i, len(xp) - 1)] * effective_hrs)
                return tier, scaled_gold, scaled_xp, rp_wph
        return None, None, None, None
    
def test_rewards_print(player_levels: list, words: list, rp_duration: int):
    desc_list: list[str] = []
    desc_str: str = ''
    
    for level in player_levels:
        tier, scaled_gold, scaled_xp, rp_wph = test_rewards_calc(level, words, rp_duration)
        desc_list.append(f'''\n**Hours of RP:** {rp_wph}
**Level:** {level}
**Gold:** {scaled_gold}gp
**XP:** {scaled_xp}''')
    
    for desc in desc_list:
        desc_str += f'\n{desc}'
    return desc_str