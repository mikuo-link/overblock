# mechanics.py
# 《文字冒险》0.0.3 核心机制
# 角色、敌人、装备、背包、伤害、状态、技能、战斗

import random
from data import *


# ==================== 角色 ====================
class Character:
    def __init__(self, name, style="平衡"):
        self.name = name
        self.style = style
        self.level = 1
        self.exp = 0
        self.exp_to_level = 10
        self.hp = 30
        self.max_hp = 30
        self.mp = 10
        self.max_mp = 10
        self.atk = 8
        self.defense = 5
        self.magic = 5
        self.spd = 0
        self.crit = 5
        self.dodge_active = DODGE_ACTIVE_BASE
        self.dodge_passive = DODGE_PASSIVE_BASE
        self.shield = 0
        self.max_shield = 0
        self.gold = 0
        self.equipment = {"武器": "无", "头盔": "无", "胸甲": "无", "护腿": "无", "靴子": "无", "盾牌": "无"}
        self.bag = []
        self.bag_max = BAG_MAX
        self.effects = []
        self.skills = ["火焰冲击", "寒冰箭", "雷电球", "治疗术", "毒液射击", "圣光护盾", "盾牌猛击", "狂暴",
                       "回旋斩", "十字斩", "突刺", "防御姿态", "防御反击", "舍身攻击", "战吼"]
        self.cooldowns = {}
        self.melee_bonus = 0.0
        self.magic_bonus = 0.0
        self.mastery = 0.0
        self.mp_regen = 2
        self.buff_duration_bonus = 0
        self.buff_cooldown_penalty = 0
        self.used_once_skills = set()
        self.adrenaline = 0
        self.life_light = 0
        self.patrol_token = 0
        self.patrol_counter = 0
        self.last_damage_type = None
        self.recalc()

    # ---------- 属性重算 ----------
    def recalc(self):
        """按流派和等级重算基础面板，再叠加装备"""
        s = STYLES[self.style]
        lv = self.level

        # 基础值 × 风格修正
        self.max_hp = int(BASE["hp"] * s["hp"] + (lv - 1) * GROWTH["hp"] * s["hp"])
        self.atk = int(BASE["atk"] * s["atk"] + (lv - 1) * GROWTH["atk"] * s["atk"])
        self.defense = int(BASE["def"] * s["def"] + (lv - 1) * GROWTH["def"] * s["def"])

        # 魔力与魔法伤害
        if s.get("magic"):
            self.max_mp = int(BASE["mp"] * s.get("mp", 1.0) + (lv - 1) * s.get("magic_per_level", 1))
            self.magic = int(BASE["magic"] * s.get("magic_per_level", 1) + (lv - 1) * s.get("magic_per_level", 1))
        else:
            # 其他流派：魔力/魔法伤害每级 +1，15 级后停
            mp_level = min(lv - 1, 15)
            self.max_mp = BASE["mp"] + mp_level * GROWTH["mp"]
            self.magic = BASE["magic"] + mp_level * GROWTH["magic"]

        # 速度：每 3 级 +1
        self.spd = (lv - 1) // 3

        # 回魔
        self.mp_regen = 2 + s.get("mp_regen", 0)

        # 重置加成
        self.melee_bonus = 0.0
        self.magic_bonus = 0.0
        self.mastery = s.get("mastery", 0.0)
        self.buff_duration_bonus = 0
        self.buff_cooldown_penalty = 0
        self.dodge_passive = DODGE_PASSIVE_BASE + min((lv - 1) // 5, 10)  # 每 5 级 +1%，封顶 15%

        # 叠加装备
        self._apply_equipment_stats()

        # 恢复时不超过上限
        self.hp = min(self.hp, self.max_hp)
        self.mp = min(self.mp, self.max_mp)

    def _apply_equipment_stats(self):
        """遍历装备，加属性"""
        for slot, item in self.equipment.items():
            if item == "无":
                continue
            # 查防具
            found = False
            for series, tiers in EQUIPMENT_SETS.items():
                for tier, data in tiers.items():
                    if item.startswith(data["name"]):
                        part = item[len(data["name"]):]
                        if part in data["parts"]:
                            self._apply_stats(data["parts"][part])
                            found = True
                            break
                if found:
                    break
            if found:
                continue
            # 查武器
            for wtype, tiers in WEAPONS.items():
                for tier, data in tiers.items():
                    if item == data["name"]:
                        stats = {}
                        if "melee" in data:
                            stats["melee"] = data["melee"] / 100.0  # 武器是数值，这里单独处理
                        if "magic" in data:
                            stats["magic"] = data["magic"] / 100.0
                        if "spd" in data:
                            stats["spd"] = data["spd"]
                        self._apply_weapon_stats(data)
                        break

    def _apply_stats(self, stats):
        """应用装备属性"""
        for k, v in stats.items():
            if k == "def":
                self.defense += v
            elif k == "hp":
                self.max_hp += int(self.max_hp * v)
            elif k == "melee":
                self.melee_bonus += v
            elif k == "magic":
                self.magic_bonus += v
            elif k == "magic_mastery":
                self.mastery += v
            elif k == "mp":
                self.max_mp += v
            elif k == "mp_regen":
                self.mp_regen += v
            elif k == "spd":
                self.spd += v
            elif k == "dodge_passive":
                self.dodge_passive += int(v * 100)

    def _apply_weapon_stats(self, data):
        """应用武器属性"""
        if "melee" in data:
            self.atk += data["melee"]
        if "magic" in data:
            self.magic += data["magic"]
        if "spd" in data:
            self.spd += data["spd"]

    # ---------- 背包 ----------
    def add_to_bag(self, item):
        if len(self.bag) < self.bag_max:
            self.bag.append(item)
            return True
        return False

    def remove_from_bag(self, index):
        if 0 <= index < len(self.bag):
            return self.bag.pop(index)
        return None

    # ---------- 经验与升级 ----------
    def gain_exp(self, amount):
        self.exp += amount
        while self.exp >= self.exp_to_level and self.level < MAX_LEVEL:
            self.exp -= self.exp_to_level
            self.level += 1
            self.exp_to_level = self.level * 15
            self.recalc()
            self.hp = self.max_hp
            self.mp = self.max_mp
            print(f"恭喜！{self.name} 升级到 {self.level} 级!")

    # ---------- 状态效果 ----------
    def add_effect(self, name, duration):
        """添加状态，同类刷新持续时间"""
        for e in self.effects:
            if e["name"] == name:
                e["duration"] = max(e["duration"], duration)
                return
        self.effects.append({"name": name, "duration": duration})

    def has_effect(self, name):
        return any(e["name"] == name for e in self.effects)

    def remove_effect(self, name):
        self.effects = [e for e in self.effects if e["name"] != name]

    def process_effects(self):
        """回合结束处理状态效果"""
        messages = []
        for e in self.effects[:]:
            name = e["name"]
            # 每回合结算
            if name in DEBUFFS:
                info = DEBUFFS[name]
                if info["type"] == "dot":
                    dmg = max(1, int(self.max_hp * info["value"]))
                    self.hp -= dmg
                    messages.append(f"{name} 造成了 {dmg} 点伤害!")
                elif info["type"] == "speed":
                    pass  # 速度减半在计算时处理
                elif info["type"] == "control":
                    pass  # 跳过行动在战斗循环处理

            if name in BUFFS:
                info = BUFFS[name]
                if info["type"] == "hot":
                    heal = max(1, int(self.max_hp * info["value"]))
                    self.hp = min(self.max_hp, self.hp + heal)
                    messages.append(f"{name} 治疗了 {heal} 点生命!")

            # 减回合
            e["duration"] -= 1
            if e["duration"] <= 0:
                self.effects.remove(e)
                messages.append(f"{name} 效果消失了!")

        return messages

    # ---------- 闪避 ----------
    def get_active_dodge(self, enemy_spd=0):
        """主动闪避率 = 基础 + 速度×5% + 相对敏捷差×10%，再乘被动加成，封顶 95%"""
        base = DODGE_ACTIVE_BASE
        base += self.spd * DODGE_ACTIVE_PER_SPD
        # 被动闪避加成（乘算）
        base = base * (1 + self.dodge_passive / 100.0)
        # 敏捷差（暂用速度差代替）
        cap = DODGE_ACTIVE_CAP
        return min(int(base), cap)

    def try_active_dodge(self, enemy_spd=0):
        rate = self.get_active_dodge(enemy_spd)
        return random.randint(1, 100) <= rate

    def try_passive_dodge(self):
        return random.randint(1, 100) <= self.dodge_passive

    # ---------- 受伤 ----------
    def take_damage(self, damage, dtype="physical", ignore_def=False, ignore_shield=False):
        """受到伤害，返回 (实际伤害, 闪避提示)"""
        # 被动闪避
        if self.try_passive_dodge():
            return 0, "被动闪避"

        actual = damage

        # 护盾吸收
        if not ignore_shield and self.shield > 0:
            absorb = min(self.shield, actual)
            self.shield -= absorb
            actual -= absorb

        # 防御抵消
        if not ignore_def:
            actual = max(1, actual - self.defense)

        actual = int(actual)
        self.hp -= actual

        # 肾上腺素/生命之光 复活判定
        if self.hp <= 0:
            revived = self._try_revive()
            if revived:
                return actual, revived

        return actual, None

    def _try_revive(self):
        """尝试复活"""
        # 肾上腺素
        if self.adrenaline > 0:
            heal = max(1, int(self.atk / 10))
            self.hp = heal
            self.adrenaline -= 1
            return f"肾上腺素触发！复活并恢复 {heal} 点生命!"
        # 生命之光
        if self.life_light > 0:
            heal = max(1, int(self.magic * 0.1))
            self.hp = heal
            self.life_light -= 1
            return f"生命之光触发！复活并恢复 {heal} 点生命!"
        return None

    def is_alive(self):
        return self.hp > 0

    # ---------- 回魔 ----------
    def regen_mp(self):
        self.mp = min(self.max_mp, self.mp + self.mp_regen)

    # ---------- 冷却 ----------
    def tick_cooldowns(self):
        for k in list(self.cooldowns.keys()):
            self.cooldowns[k] -= 1
            if self.cooldowns[k] <= 0:
                del self.cooldowns[k]

    def is_on_cooldown(self, skill):
        return skill in self.cooldowns


# ==================== 敌人 ====================
class Enemy:
    def __init__(self, name, level):
        info = ENEMIES[name]
        f = ENEMY_FORMULAS[info["type"]]
        self.name = name
        self.type = info["type"]
        self.element = info["element"]
        self.level = level
        self.hp = self._calc_stat(f["hp"])
        self.max_hp = self.hp
        self.atk = self._calc_atk()
        self.defense = self._calc_stat(f["def"])
        self.spd = self._calc_stat(f["spd"])
        self.exp = 10 + level * 5
        self.gold = 5 + level * 3
        self.skills = ENEMY_SKILLS[self.type]
        self.charging = None       # 蓄力技能名
        self.charging_timer = 0
        self.status = []           # 敌人身上的状态
        self.dodge_passive = 0     # 精英怪可设
        self.used_once = set()
        self.dead = False

        # 元素修正
        if self.element in ELEMENT_MODS:
            mod = ELEMENT_MODS[self.element]
            if "atk" in mod:
                self.atk = int(self.atk * mod["atk"])
            if "def" in mod:
                self.defense = int(self.defense * mod["def"])
            if "hp" in mod:
                self.hp = int(self.hp * mod["hp"])
                self.max_hp = self.hp
            if "spd" in mod:
                self.spd = int(self.spd * mod["spd"])

        # 独有修正
        if "hp_mult" in info:
            self.hp = int(self.hp * info["hp_mult"])
            self.max_hp = self.hp

    def _calc_stat(self, formula):
        """通用属性公式（分段成长）"""
        base, inc = formula
        lv = self.level
        if lv <= 10:
            val = base + (lv - 1) * inc
        elif lv <= 20:
            val = base + 9 * inc + (lv - 10) * (inc + 0.5)
        else:
            val = base + 9 * inc + 10 * (inc + 0.5) + (lv - 20) * (inc + 1.0)
        return int(val)

    def _calc_atk(self):
        """攻击使用分段增量"""
        base = ENEMY_FORMULAS[self.type]["atk"][0]
        lv = self.level
        seg = ENEMY_ATK_SEGMENTS
        if lv <= 10:
            val = base + (lv - 1) * seg["1_10"]
        elif lv <= 20:
            val = base + 9 * seg["1_10"] + (lv - 10) * seg["11_20"]
        else:
            val = base + 9 * seg["1_10"] + 10 * seg["11_20"] + (lv - 20) * seg["21_30"]
        return int(val)

    def is_alive(self):
        return self.hp > 0 and not self.dead

    # ---------- 敌人受伤 ----------
    def take_damage(self, damage, dtype="physical", ignore_def=False):
        # 被动闪避
        if self.dodge_passive > 0 and random.randint(1, 100) <= self.dodge_passive:
            return 0, "敌人闪避"

        # 魔法抗性（巨人）
        if dtype == "magic" and ENEMY_FORMULAS[self.type].get("resist") == "magic":
            damage = int(damage * 0.8)
        # 物理抗性（史莱姆）
        if dtype == "physical" and ENEMY_FORMULAS[self.type].get("resist") == "physical":
            damage = int(damage * 0.8)

        if not ignore_def:
            actual = max(1, damage - self.defense)
        else:
            actual = max(1, damage)

        self.hp -= int(actual)
        if self.hp <= 0:
            self.dead = True
        return int(actual), None

    # ---------- 敌人行动 ----------
    def choose_action(self, player):
        """返回 (消息列表, 是否被控制)"""
        messages = []

        # 处理控制状态
        if self.has_status("冰冻") or self.has_status("麻痹") or self.has_status("震慑"):
            messages.append(f"{self.name} 被控制，无法行动!")
            return messages

        # 蓄力中：释放
        if self.charging:
            msg = self._release_charge(player)
            messages.append(msg)
            return messages

        # 技能概率
        if random.random() < ENEMY_SKILL_CHANCE:
            skill = random.choice(self.skills)
            # 每场一次限制
            data = ENEMY_SKILL_DATA.get(skill, {})
            if data.get("once") and skill in self.used_once:
                skill = "普攻"
        else:
            skill = "普攻"

        if skill == "普攻":
            msg = self._basic_attack(player)
            messages.append(msg)
        else:
            self.used_once.add(skill)
            msg = self._use_skill(skill, player)
            messages.append(msg)

        return messages

    def _basic_attack(self, player):
        # 普通攻击 15% 概率附加元素减益
        dmg, dodge = player.take_damage(self.atk, "physical")
        if dodge:
            return f"{self.name} 攻击被 {dodge}!"
        msg = f"{self.name} 攻击了你，造成 {dmg} 点伤害!"
        if random.random() < ENEMY_BASIC_DEBUFF_CHANCE and self.element in ELEMENT_DEBUFF:
            debuff = ELEMENT_DEBUFF[self.element]
            if debuff:
                player.add_effect(debuff, 1)
                msg += f" 你受到了 {debuff}!"
        return msg

    def _use_skill(self, skill, player):
        data = ENEMY_SKILL_DATA.get(skill, {})
        # 蓄力技能
        if data.get("charge"):
            self.charging = skill
            return f"{self.name} 正在准备 {skill}！"

        return self._resolve_skill(skill, player, data)

    def _release_charge(self, player):
        skill = self.charging
        self.charging = None
        data = ENEMY_SKILL_DATA.get(skill, {})
        return self._resolve_skill(skill, player, data)

    def _resolve_skill(self, skill, player, data):
        mult = data.get("mult", 1.0)
        hits = data.get("hits", 1)
        messages = []

        # 伤害
        if mult > 0:
            total = 0
            for _ in range(hits):
                dmg = int(self.atk * mult)
                # 闪避判定（对每个目标独立，这里只玩家）
                if data.get("charge"):
                    # 蓄力技能，闪避必过
                    if player.try_active_dodge(self.spd):
                        messages.append(f"你闪开了 {skill}!")
                        continue
                actual, dodge = player.take_damage(dmg, "physical")
                if dodge:
                    messages.append(f"{skill} 被 {dodge}!")
                else:
                    total += actual
            if total > 0:
                messages.append(f"{self.name} 使用 {skill}，造成 {total} 点伤害!")

        # 附加减益
        if "effect" in data:
            eff = data["effect"]
            if eff[0] == "element":
                debuff = ELEMENT_DEBUFF.get(self.element)
                if debuff:
                    # 火焰免疫冰冻/寒冷
                    if self.element == "火" and debuff in FIRE_IMMUNE:
                        pass
                    else:
                        duration = eff[1] if isinstance(eff[1], int) else random.randint(1, 2)
                        player.add_effect(debuff, duration)
                        messages.append(f"你受到了 {debuff} {duration} 回合!")
            else:
                player.add_effect(eff[0], eff[1])
                messages.append(f"你受到了 {eff[0]}!")

        # 禁用闪避
        if data.get("disable_dodge"):
            player.add_effect("网缚", data["disable_dodge"])
            messages.append("你被禁用了闪避!")

        # 寄生种子
        if data.get("seed"):
            player.add_effect("寄生种子", 99)
            messages.append("你被种下了寄生种子!")

        # 随机效果（藤蔓囚笼）
        if "random" in data:
            r = random.choice(data["random"])
            if r == "disable_dodge_2":
                player.add_effect("网缚", 2)
                messages.append("你被禁用闪避 2 回合!")
            elif r == "def_up_30":
                self.defense = int(self.defense * 1.3)
                messages.append(f"{self.name} 防御提升 30%!")

        return " ".join(messages) if messages else f"{self.name} 使用了 {skill}!"

    # ---------- 敌人状态 ----------
    def add_status(self, name, duration):
        for e in self.status:
            if e["name"] == name:
                e["duration"] = max(e["duration"], duration)
                return
        self.status.append({"name": name, "duration": duration})

    def has_status(self, name):
        return any(e["name"] == name for e in self.status)

    def process_status(self):
        for e in self.status[:]:
            e["duration"] -= 1
            if e["duration"] <= 0:
                self.status.remove(e)


# ==================== 伤害计算 ====================
def calc_damage(attacker, defender, mult=1.0, dtype="physical", ignore_def=False, scale=None):
    """
    计算伤害，规则：
    1. 基础值（攻击或魔法）
    2. × 技能倍率
    3. × (1 + 加算增伤)
    4. × (1 + 乘算精通)
    5. - 防御
    6. 四舍五入
    """
    # 基础
    if scale == "def":
        base = attacker.defense
    elif dtype == "magic":
        base = attacker.magic
    else:
        base = attacker.atk

    dmg = base * mult

    # 加算增伤
    if dtype == "physical":
        dmg *= (1 + getattr(attacker, "melee_bonus", 0.0))
    elif dtype == "magic":
        dmg *= (1 + getattr(attacker, "magic_bonus", 0.0))

    # 乘算精通
    if dtype == "magic":
        dmg *= (1 + getattr(attacker, "mastery", 0.0))

    # 防御抵消
    if not ignore_def:
        dmg = max(1, dmg - defender.defense)

    # 四舍五入
    return int(round(dmg))


# ==================== 装备应用 ====================
def apply_equipment(player):
    """外部调用的装备重算"""
    player.recalc()
    # 套装效果
    _check_set_bonus(player)


def _check_set_bonus(player):
    """检查套装效果（2 件套 / 4 件套）"""
    # 统计每个系列的件数和星级
    series_count = {}   # {系列: [(部位, 星级)]}
    for slot, item in player.equipment.items():
        if item == "无" or slot == "武器" or slot == "盾牌":
            continue
        for series, tiers in EQUIPMENT_SETS.items():
            for tier, data in tiers.items():
                if item.startswith(data["name"]):
                    if series not in series_count:
                        series_count[series] = []
                    series_count[series].append((tier, slot))

    for series, items in series_count.items():
        # 2 件套：同系列二星及以上
        high_items = [x for x in items if x[0] in ("二星", "三星")]
        if len(high_items) >= 2:
            set2 = None
            for tier in ("二星", "三星"):
                for tier_key, data in EQUIPMENT_SETS[series].items():
                    if tier_key == tier and data.get("set2"):
                        set2 = data["set2"]
                        break
                if set2:
                    break
            if set2:
                _apply_set_stats(player, set2)

        # 4 件套：全套三星
        if len(items) == 4 and all(x[0] == "三星" for x in items):
            set4 = EQUIPMENT_SETS[series]["三星"].get("set4")
            if set4:
                _apply_set_stats(player, set4)


def _apply_set_stats(player, stats):
    """应用套装效果"""
    for k, v in stats.items():
        if k == "melee":
            player.melee_bonus += v
        elif k == "magic":
            player.magic_bonus += v
        elif k == "magic_mastery":
            player.mastery += v
        elif k == "spd":
            player.spd += v
        elif k == "mp_regen":
            player.mp_regen += v
        elif k == "dodge_passive":
            player.dodge_passive += int(v * 100)
        elif k == "adrenaline":
            player.adrenaline += v
        elif k == "frenzy":
            pass  # 狂化倍率在释放时检查
        elif k == "patrol_token":
            player.patrol_token += v
        elif k == "damage_switch":
            pass  # 在伤害计算时检查
        elif k == "buff_duration":
            player.buff_duration_bonus += v
        elif k == "buff_cooldown":
            player.buff_cooldown_penalty += v
