# ui.py
# 《文字冒险》0.0.3 输入输出

def print_out(text=""):
    print(text)

def ask(prompt):
    return input(prompt)

def ask_choice(prompt, options):
    """显示选项，返回用户选择的索引（0 起）"""
    print(prompt)
    for i, opt in enumerate(options):
        print(f"{i + 1}. {opt}")
    while True:
        try:
            idx = int(input("请选择: ")) - 1
            if 0 <= idx < len(options):
                return idx
            print("无效选择，请重新输入。")
        except ValueError:
            print("无效输入，请输入数字。")

def ask_yes_no(prompt):
    while True:
        ans = input(f"{prompt} (是/否): ").strip().lower()
        if ans in ("是", "y", "yes"):
            return True
        if ans in ("否", "n", "no"):
            return False
        print("无效的命令，请在‘是’或‘否’中做出选择。")

def show_enemy_list(enemies):
    """显示敌人列表，格式：序号. 名称 生命值：xx/xx"""
    for i, e in enumerate(enemies):
        if e.is_alive():
            print(f"{i + 1}. {e.name}  生命值：{e.hp}/{e.max_hp}")

def show_player_status(player):
    print(f"\n===== {player.name} 的状态 =====")
    print(f"等级: {player.level}  经验: {player.exp}/{player.exp_to_level}")
    print(f"生命: {player.hp}/{player.max_hp}")
    print(f"魔力: {player.mp}/{player.max_mp}")
    print(f"护盾: {player.shield}")
    print(f"攻击: {player.atk}  防御: {player.defense}  魔法: {player.magic}")
    print(f"速度: {player.spd}  回魔: {player.mp_regen}")
    print(f"近战增伤: {int(player.melee_bonus * 100)}%  魔法增伤: {int(player.magic_bonus * 100)}%  精通: {int(player.mastery * 100)}%")
    print(f"被动闪避: {player.dodge_passive}%  主动闪避: {player.get_active_dodge()}%")
    print(f"金币: {player.gold}  战斗风格: {player.style}")
    print("装备:")
    for slot, item in player.equipment.items():
        print(f"  {slot}: {item}")
    if player.effects:
        print("状态效果:")
        for e in player.effects:
            print(f"  - {e['name']} ({e['duration']} 回合)")
    print("========================")

def show_bag(player):
    if not player.bag:
        print("背包是空的。")
        return
    print(f"\n背包 ({len(player.bag)}/{player.bag_max}):")
    for i, item in enumerate(player.bag):
        print(f"{i + 1}. {item}")

