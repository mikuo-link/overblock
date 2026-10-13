# main.py
# 《文字冒险》0.0.3 主循环

import random
from mechanics import Character, Enemy, apply_equipment, calc_damage
from data import *
from ui import print_out, ask, ask_choice, ask_yes_no, show_enemy_list, show_player_status, show_bag


# ==================== 主入口 ====================
def main():
    print_out("欢迎来到《文字冒险》0.0.3!")
    print_out()
    name = ask("请为你的角色取一个名字: ").strip()
    if not name:
        name = "无名氏"
    player = Character(name)
    print_out(f"\n你好，{player.name}！开始你的冒险吧！")
    show_player_status(player)

    while True:
        choice = ask_choice("\n===== 主菜单 =====", ["探索", "查看状态", "更换战斗风格", "打开背包", "休息", "退出"])
        if choice == 0:
            explore(player)
        elif choice == 1:
            show_player_status(player)
        elif choice == 2:
            change_style(player)
        elif choice == 3:
            open_bag(player)
        elif choice == 4:
            rest(player)
        elif choice == 5:
            print_out("感谢游玩！")
            break
        if not player.is_alive():
            print_out("你倒下了……游戏结束。")
            break


# ==================== 探索 ====================
def explore(player):
    print_out("\n你开始探索……")
    encounter = random.randint(1, 10)
    if encounter <= 4:
        find_item(player)
    elif encounter <= 7:
        find_gold(player)
    else:
        battle(player)


# ==================== 捡装备 ====================
def find_item(player):
    tier = get_tier_by_level(player.level)
    if random.random() < 0.5:
        # 防具
        series = random.choice(list(EQUIPMENT_SETS.keys()))
        data = EQUIPMENT_SETS[series][tier]
        part = random.choice(list(data["parts"].keys()))
        item = data["name"] + part
    else:
        # 武器
        wtype = random.choice(list(WEAPONS.keys()))
        data = WEAPONS[wtype][tier]
        item = data["name"]
    print_out(f"\n你发现了一个 {item}！")

    if player.add_to_bag(item):
        print_out("已放入背包。")
    else:
        print_out("背包已满！")
        show_bag(player)
        idx = ask_choice("你想替换掉哪个装备？", player.bag)
        player.bag[idx] = item
        print_out(f"已用 {item} 替换掉旧装备。")


# ==================== 捡金币 ====================
def find_gold(player):
    g = random.randint(10, 30)
    player.gold += g
    print_out(f"\n你找到了 {g} 枚金币！")


# ==================== 背包 ====================
def open_bag(player):
    show_bag(player)
    if not player.bag:
        return
    choice = ask_choice("\n要做什么？", ["装备", "丢弃", "返回"])
    if choice == 0:
        idx = ask_choice("选择要装备的物品", player.bag)
        item = player.bag.pop(idx)
        equip_item(player, item)
    elif choice == 1:
        idx = ask_choice("选择要丢弃的物品", player.bag)
        item = player.bag.pop(idx)
        print_out(f"你丢弃了 {item}。")


def equip_item(player, item):
    """装备物品，自动判断部位"""
    # 防具
    for series, tiers in EQUIPMENT_SETS.items():
        for tier, data in tiers.items():
            if item.startswith(data["name"]):
                part = item[len(data["name"]):]
                if part in ("头盔", "胸甲", "护腿", "靴子"):
                    player.equipment[part] = item
                    apply_equipment(player)
                    print_out(f"你装备了 {item}！")
                    return
    # 武器
    for wtype, tiers in WEAPONS.items():
        for tier, data in tiers.items():
            if item == data["name"]:
                player.equipment["武器"] = item
                apply_equipment(player)
                print_out(f"你装备了 {item}！")
                return
    # 盾牌
    if item in SHIELDS:
        player.equipment["盾牌"] = item
        apply_equipment(player)
        print_out(f"你装备了 {item}！")
        return
    print_out("这个物品无法装备。")


# ==================== 更换战斗风格 ====================
def change_style(player):
    styles = ["狂暴", "防御", "平衡", "魔法"]
    idx = ask_choice("选择战斗风格", styles)
    player.style = styles[idx]
    apply_equipment(player)
    print_out(f"战斗风格已更改为：{player.style}")
    show_player_status(player)


# ==================== 休息 ====================
def rest(player):
    heal = random.randint(10, 20)
    player.hp = min(player.max_hp, player.hp + heal)
    player.mp = player.max_mp
    player.shield = 0
    player.effects = []
    print_out(f"\n你恢复了 {heal} 点生命值，魔力和护盾也恢复了。")


# ==================== 战斗 ====================
def battle(player):
    # 生成敌人
    enemy_count = random.randint(1, min(3, max(1, player.level // 5 + 1)))
    enemies = []
    names = list(ENEMIES.keys())
    for _ in range(enemy_count):
        name = random.choice(names)
        enemies.append(Enemy(name, player.level))

    print_out(f"\n遭遇 {len(enemies)} 个敌人！")
    for i, e in enumerate(enemies):
        print_out(f"{i + 1}. {e.name} (LV{e.level})")

    # 战斗循环
    turn = 1
    while any(e.is_alive() for e in enemies) and player.is_alive():
        print_out(f"\n=== 第 {turn} 回合 ===")
        show_player_status(player)
        print_out("\n敌人:")
        show_enemy_list(enemies)

        # 玩家回合
        action = ask_choice("\n选择行动", ["攻击", "技能", "闪避", "逃跑", "查看敌人状态"])
        if action == 0:
            player_basic_attack(player, enemies)
        elif action == 1:
            player_use_skill(player, enemies)
        elif action == 2:
            print_out("你采取了闪避姿态。")
        elif action == 3:
            if random.random() < FLEE_RATE:
                print_out("你成功逃脱了！")
                return
            else:
                print_out("逃跑失败！")
        elif action == 4:
            # 查看敌人状态
            print_out("\n敌人详细状态:")
            for i, e in enumerate(enemies):
                if e.is_alive():
                    print_out(f"{i + 1}. {e.name} 生命:{e.hp}/{e.max_hp} 攻击:{e.atk} 防御:{e.defense} 速度:{e.spd}")

        # 玩家回合结束：状态结算、冷却、回魔
        msgs = player.process_effects()
        for m in msgs:
            print_out(m)
        player.tick_cooldowns()
        player.regen_mp()

        # 敌人回合
        if not player.is_alive():
            break
        print_out("\n=== 敌人回合 ===")
        for e in enemies:
            if not e.is_alive():
                continue
            msgs = e.choose_action(player)
            for m in msgs:
                print_out(m)
            e.process_status()
            if not player.is_alive():
                break

        turn += 1

    # 战斗结束
    if player.is_alive():
        total_exp = sum(e.exp for e in enemies if not e.is_alive())
        total_gold = sum(e.gold for e in enemies if not e.is_alive())
        print_out(f"\n战斗胜利！获得 {total_exp} 经验，{total_gold} 金币。")
        player.gain_exp(total_exp)
        player.gold += total_gold
    else:
        print_out("\n你被击败了……")


def player_basic_attack(player, enemies):
    """普通攻击"""
    alive = [e for e in enemies if e.is_alive()]
    if not alive:
        return
    # 选目标
    if len(alive) == 1:
        target = alive[0]
        print_out(f"自动选择目标：{target.name}")
    else:
        show_enemy_list(enemies)
        idx = ask_choice("选择目标", [e.name for e in enemies if e.is_alive()])
        target = [e for e in enemies if e.is_alive()][idx]

    # 判断手持武器
    weapon = player.equipment.get("武器", "无")
    is_staff = any(weapon == d["name"] for wtype, tiers in WEAPONS.items() if wtype == "法杖" for d in tiers.values())
    dtype = "magic" if is_staff else "physical"

    dmg = calc_damage(player, target, 1.0, dtype)
    actual, dodge = target.take_damage(dmg, dtype)
    if dodge:
        print_out(f"{target.name} {dodge}了你的攻击！")
    else:
        print_out(f"你对 {target.name} 造成了 {actual} 点伤害！")


def player_use_skill(player, enemies):
    """使用技能"""
    alive_skills = [s for s in player.skills if s in PLAYER_SKILLS]
    idx = ask_choice("选择技能", alive_skills + ["取消"])
    if idx == len(alive_skills):
        return
    skill = alive_skills[idx]
    info = PLAYER_SKILLS[skill]

    # 检查冷却
    if player.is_on_cooldown(skill):
        print_out(f"{skill} 还在冷却中！")
        return
    # 检查魔力
    if player.mp < info.get("cost", 0):
        print_out("魔力不足！")
        return
    # 每场一次
    if info.get("once") and skill in player.used_once_skills:
        print_out(f"{skill} 本场已经用过了！")
        return

    # 扣魔
    player.mp -= info.get("cost", 0)
    # 设置冷却
    cd = info.get("cd", 0) + player.buff_cooldown_penalty
    if cd > 0:
        player.cooldowns[skill] = cd
    if info.get("once"):
        player.used_once_skills.add(skill)

    dtype = info.get("dtype", "physical")

    # 治疗
    if dtype == "heal":
        heal = int(player.magic * info.get("heal", 1.0))
        player.hp = min(player.max_hp, player.hp + heal)
        print_out(f"你使用 {skill}，恢复了 {heal} 点生命！")
        if "effect" in info:
            player.add_effect(info["effect"][0], info["effect"][1] + player.buff_duration_bonus)
            print_out(f"获得 {info['effect'][0]} 效果！")
        return

    # 护盾
    if dtype == "shield":
        shield = int(player.magic * info.get("shield", 1.0))
        player.shield += shield
        print_out(f"你使用 {skill}，获得 {shield} 点护盾！")
        if "effect" in info:
            player.add_effect(info["effect"][0], info["effect"][1] + player.buff_duration_bonus)
            print_out(f"获得 {info['effect'][0]} 效果！")
        return

    # 增益
    if dtype == "buff":
        buff = info.get("buff", "")
        dur = info.get("duration", 2) + player.buff_duration_bonus
        player.add_effect(buff, dur)
        print_out(f"你使用 {skill}，获得 {buff} 效果！")
        if buff == "狂化":
            pass
        return

    # 伤害技能
    targets_count = info.get("targets", 1)
    hits = info.get("hits", 1)
    ignore_def = info.get("ignore_def", False)
    scale = info.get("scale", None)

    alive = [e for e in enemies if e.is_alive()]
    if not alive:
        return

    # 选目标
    if targets_count == 1:
        if len(alive) == 1:
            targets = [alive[0]]
        else:
            show_enemy_list(enemies)
            idx = ask_choice("选择目标", [e.name for e in enemies if e.is_alive()])
            targets = [[e for e in enemies if e.is_alive()][idx]]
    else:
        targets = alive[:targets_count]

    total = 0
    for target in targets:
        for _ in range(hits):
            dmg = calc_damage(player, target, info.get("mult", 1.0), dtype, ignore_def, scale)
            actual, dodge = target.take_damage(dmg, dtype, ignore_def)
            if dodge:
                print_out(f"{target.name} {dodge}了！")
            else:
                total += actual
    print_out(f"你使用 {skill}，共造成 {total} 点伤害！")

    # 附加效果
    if "effect" in info:
        eff_name, eff_dur = info["effect"]
        for target in targets:
            if target.is_alive():
                target.add_status(eff_name, eff_dur)
        print_out(f"附加了 {eff_name} 效果！")


# ==================== 启动 ====================
if __name__ == "__main__":
    main()

