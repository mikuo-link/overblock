# data.py
# 《文字冒险》0.0.3 数据表
# 所有数值、装备、武器、盾牌、技能、敌人、状态

# ==================== 流派修正 ====================
# 风格修正只影响基础数值，优先级第一
STYLES = {
    "狂暴": {
        "hp": 1.1, "atk": 1.6, "def": 0.6, "spd": 1.2,
        "magic": False, "mp_regen": 0, "mastery": 0.0,
    },
    "防御": {
        "hp": 1.4, "atk": 0.6, "def": 1.8, "spd": 0.7,
        "magic": False, "mp_regen": 0, "mastery": 0.0,
    },
    "平衡": {
        "hp": 1.0, "atk": 1.0, "def": 1.0, "spd": 1.0,
        "magic": False, "mp_regen": 0, "mastery": 0.0,
    },
    "魔法": {
        "hp": 0.8, "atk": 0.6, "def": 0.7, "spd": 1.0,
        "magic": True, "mp_regen": 5, "mastery": 0.30,
        "magic_per_level": 2, "melee_per_level": 1, "magic_cap_level": 15,
    },
}

# ==================== 基础值与成长 ====================
BASE = {"hp": 30, "atk": 8, "def": 5, "mp": 10, "magic": 5, "spd": 0}
GROWTH = {"hp": 5, "atk": 2, "def": 2, "mp": 1, "magic": 1, "spd_per_3": 1}
MAX_LEVEL = 30
BAG_MAX = 20

# 主动/被动闪避
DODGE_ACTIVE_BASE = 10       # 主动闪避基础 10%
DODGE_ACTIVE_PER_SPD = 5     # 每点速度 +5%
DODGE_ACTIVE_CAP = 95        # 主动闪避封顶 95%
DODGE_PASSIVE_BASE = 5       # 被动闪避基础 5%
DODGE_PASSIVE_PER_5LV = 1    # 每 5 级 +1%
DODGE_PASSIVE_CAP = 15       # 被动闪避基础封顶 15%

# 逃跑
FLEE_RATE = 0.80

# ==================== 装备系列 ====================
# 每系列三档：一星（无套装）、二星（二件套）、三星（二件套+四件套）
# 二星和三星的二件套效果一样
# 属性 key：def/hp/melee/magic/magic_mastery/mp/mp_regen/spd/dodge_passive
EQUIPMENT_SETS = {
    "骑士": {
        "一星": {
            "name": "见习骑士",
            "parts": {
                "头盔": {"def": 4},
                "胸甲": {"def": 6},
                "护腿": {"def": 5, "melee": 0.05},
                "靴子": {"def": 3, "hp": 0.05},
            },
            "set2": None,
            "set4": None,
        },
        "二星": {
            "name": "精英骑士",
            "parts": {
                "头盔": {"def": 6, "hp": 0.05},
                "胸甲": {"def": 12},
                "护腿": {"def": 8, "melee": 0.10},
                "靴子": {"def": 4, "hp": 0.10},
            },
            "set2": {"melee": 0.20},
            "set4": None,
        },
        "三星": {
            "name": "圣骑士",
            "parts": {
                "头盔": {"def": 10, "hp": 0.10},
                "胸甲": {"def": 20},
                "护腿": {"def": 15, "melee": 0.20},
                "靴子": {"def": 5, "hp": 0.15},
            },
            "set2": {"melee": 0.20},
            "set4": {"adrenaline": 1},
        },
    },
    "游侠": {
        "一星": {
            "name": "窃贼",
            "parts": {
                "头盔": {"def": 3},
                "胸甲": {"def": 5, "spd": 1},
                "护腿": {"def": 4, "melee": 0.05},
                "靴子": {"def": 2, "spd": 2},
            },
            "set2": None,
            "set4": None,
        },
        "二星": {
            "name": "刺客",
            "parts": {
                "头盔": {"def": 5, "melee": 0.05},
                "胸甲": {"def": 10, "spd": 2, "melee": 0.05},
                "护腿": {"def": 7, "spd": 2, "melee": 0.10},
                "靴子": {"def": 4, "spd": 3},
            },
            "set2": {"spd": 4, "melee": 0.10},
            "set4": None,
        },
        "三星": {
            "name": "侠盗",
            "parts": {
                "头盔": {"def": 7, "melee": 0.10},
                "胸甲": {"def": 12, "spd": 3, "melee": 0.10},
                "护腿": {"def": 10, "spd": 3, "melee": 0.15},
                "靴子": {"def": 6, "spd": 5},
            },
            "set2": {"spd": 4, "melee": 0.10},
            "set4": {"dodge_passive": 0.10},
        },
    },
    "巫师": {
        "一星": {
            "name": "学徒",
            "parts": {
                "头盔": {"def": 1, "mp": 5},
                "胸甲": {"def": 2, "mp": 7, "mp_regen": 5},
                "护腿": {"def": 2, "mp": 6},
                "靴子": {"def": 1, "mp": 5},
            },
            "set2": None,
            "set4": None,
        },
        "二星": {
            "name": "魔导师",
            "parts": {
                "头盔": {"def": 2, "magic": 0.10, "mp": 7},
                "胸甲": {"def": 4, "mp": 15, "mp_regen": 10},
                "护腿": {"def": 3, "magic_mastery": 0.10, "mp": 10},
                "靴子": {"def": 2, "magic_mastery": 0.07, "mp": 10},
            },
            "set2": {"magic": 0.20},
            "set4": None,
        },
        "三星": {
            "name": "大法师",
            "parts": {
                "头盔": {"def": 4, "magic": 0.15, "mp": 10},
                "胸甲": {"def": 6, "mp": 20, "mp_regen": 20},
                "护腿": {"def": 5, "magic_mastery": 0.20, "mp": 15},
                "靴子": {"def": 4, "magic_mastery": 0.15, "mp": 15},
            },
            "set2": {"magic": 0.20},
            "set4": {"magic_mastery": 0.15, "mp_regen": 20, "mp_cost_reduce": 0.10},
        },
    },
    "狂暴": {
        "一星": {
            "name": "野蛮人",
            "parts": {
                "头盔": {"def": 4, "hp": 0.05},
                "胸甲": {"def": 6, "hp": 0.10},
                "护腿": {"def": 5, "hp": 0.05},
                "靴子": {"def": 3, "melee": 0.05},
            },
            "set2": None,
            "set4": None,
        },
        "二星": {
            "name": "角斗士",
            "parts": {
                "头盔": {"def": 7, "hp": 0.05, "melee": 0.05},
                "胸甲": {"def": 10, "hp": 0.10, "melee": 0.05},
                "护腿": {"def": 7, "hp": 0.05, "melee": 0.10},
                "靴子": {"def": 6, "melee": 0.10},
            },
            "set2": {"frenzy": 1.8},
            "set4": None,
        },
        "三星": {
            "name": "圣斗士",
            "parts": {
                "头盔": {"def": 10, "hp": 0.05, "melee": 0.10},
                "胸甲": {"def": 13, "hp": 0.15, "melee": 0.05},
                "护腿": {"def": 9, "hp": 0.10, "melee": 0.15},
                "靴子": {"def": 8, "melee": 0.15},
            },
            "set2": {"frenzy": 1.8},
            "set4": {"buff_duration": 1, "buff_cooldown": 1},
        },
    },
    "平衡": {
        "一星": {
            "name": "流浪者",
            "parts": {
                "头盔": {"def": 3, "magic": 0.05, "melee": 0.05, "mp": 5},
                "胸甲": {"def": 4, "melee": 0.05, "mp_regen": 5, "hp": 0.05},
                "护腿": {"def": 3, "magic": 0.05, "mp": 5},
                "靴子": {"def": 2, "spd": 2, "dodge_passive": 0.02},
            },
            "set2": None,
            "set4": None,
        },
        "二星": {
            "name": "巡游者",
            "parts": {
                "头盔": {"def": 5, "magic": 0.10, "melee": 0.10, "mp": 10},
                "胸甲": {"def": 7, "melee": 0.10, "mp_regen": 10, "hp": 0.10},
                "护腿": {"def": 6, "magic": 0.10, "magic_mastery": 0.10, "mp": 10},
                "靴子": {"def": 5, "spd": 3, "dodge_passive": 0.03},
            },
            "set2": {"patrol_token": 1},
            "set4": None,
        },
        "三星": {
            "name": "巡礼者",
            "parts": {
                "头盔": {"def": 8, "magic": 0.15, "melee": 0.15, "mp": 20},
                "胸甲": {"def": 10, "melee": 0.15, "mp_regen": 20, "hp": 0.15},
                "护腿": {"def": 9, "magic": 0.15, "magic_mastery": 0.15, "mp": 20},
                "靴子": {"def": 8, "spd": 5, "dodge_passive": 0.05},
            },
            "set2": {"patrol_token": 1},
            "set4": {"damage_switch": 1.2},
        },
    },
}

# ==================== 武器 ====================
# 属性 key：melee/magic/spd/range/skill
WEAPONS = {
    "单手剑": {
        "一星": {"name": "训练木剑", "melee": 7, "spd": 2, "range": 1, "skill": None},
        "二星": {"name": "铁剑", "melee": 14, "spd": 2, "range": 1, "skill": "坚韧不拔"},
        "三星": {"name": "圣剑", "melee": 25, "spd": 2, "range": 1, "skill": ["圣光裁决", "战神的加护"]},
    },
    "大剑": {
        "一星": {"name": "佣兵大剑", "melee": 15, "spd": 0, "range": 2, "skill": None},
        "二星": {"name": "勇者大剑", "melee": 28, "spd": 0, "range": 2, "skill": "越战越勇"},
        "三星": {"name": "裂天巨剑", "melee": 50, "spd": 0, "range": 2, "skill": ["破军", "裂天"]},
    },
    "长矛": {
        "一星": {"name": "卫兵长矛", "melee": 7, "spd": 1, "range": 3, "skill": None},
        "二星": {"name": "斯巴达长矛", "melee": 14, "spd": 1, "range": 3, "skill": "破釜沉舟"},
        "三星": {"name": "炽天使长矛", "melee": 25, "spd": 1, "range": 3, "skill": ["怒火", "审判业火"]},
    },
    "法杖": {
        "一星": {"name": "学徒法杖", "magic": 7, "spd": 0, "range": 5, "skill": None},
        "二星": {"name": "魔导灵杖", "magic": 14, "spd": 1, "range": 5, "skill": "学无止境"},
        "三星": {"name": "古神圣杖", "magic": 25, "spd": 1, "range": 5, "skill": ["冥河", "唤灵"]},
    },
}

# 手持法杖时普攻按魔法伤害算
STAFF_PRIMARY_MAGIC = True

# ==================== 盾牌 ====================
SHIELDS = {
    "木盾": {"block": 10, "spd": 0, "dmg": 1.0, "tier": 1},
    "铁盾": {"block": 20, "spd": 0, "dmg": 1.0, "tier": 2},
    "圣盾": {"block": 30, "spd": 0, "dmg": 1.0, "tier": 3},
    "塔盾": {"block": 40, "spd": -2, "dmg": 0.8, "no_dodge": True, "thrust_mult": 1.2, "tier": 4},
    "轻型盾": {"block": 15, "spd": 2, "post_block": True, "no_thrust": True, "tier": 4},
}

# ==================== 玩家技能 ====================
# cost: 魔力消耗；cd: 冷却回合；mult: 倍率；dtype: 伤害类型
# targets: 目标数；hits: 段数；ignore_def: 无视防御
# scale: 伤害基准（atk/magic/def）；effect: (状态名, 持续回合)
# heal: 治疗倍率；shield: 护盾倍率；buff: 增益名；once: 每场一次
PLAYER_SKILLS = {
    "火焰冲击": {"cost": 10, "cd": 2, "mult": 2.0, "dtype": "magic", "targets": 2, "effect": ("燃烧", 3)},
    "寒冰箭":   {"cost": 10, "cd": 2, "mult": 2.25, "dtype": "magic", "targets": 2, "effect": ("冰冻", 1)},
    "雷电球":   {"cost": 12, "cd": 2, "mult": 1.75, "dtype": "magic", "targets": 3, "effect": ("麻痹", 2), "ignore_def": True},
    "治疗术":   {"cost": 10, "cd": 1, "heal": 2.0, "dtype": "heal", "targets": 0, "effect": ("治愈", 2)},
    "毒液射击": {"cost": 15, "cd": 3, "mult": 1.2, "dtype": "physical", "targets": 3, "hits": 3, "effect": ("中毒", 3)},
    "圣光护盾": {"cost": 12, "cd": 4, "shield": 2.0, "dtype": "shield", "targets": 0, "effect": ("生命之光", 2)},
    "盾牌猛击": {"cost": 0, "cd": 2, "mult": 0.8, "dtype": "physical", "targets": 1, "ignore_def": True, "scale": "def"},
    "狂暴":     {"cost": 0, "cd": 5, "dtype": "buff", "targets": 0, "buff": "狂化", "duration": 3},
    "回旋斩":   {"cost": 0, "cd": 2, "mult": 1.5, "dtype": "physical", "targets": 2},
    "十字斩":   {"cost": 0, "cd": 2, "mult": 1.0, "dtype": "physical", "targets": 1, "hits": 2},
    "突刺":     {"cost": 0, "cd": 2, "mult": 1.75, "dtype": "physical", "targets": 1, "ignore_def": True},
    "防御姿态": {"cost": 0, "cd": 4, "dtype": "buff", "targets": 0, "buff": "防御姿态", "duration": 2},
    "防御反击": {"cost": 0, "cd": 0, "dtype": "buff", "targets": 0, "buff": "防御反击", "duration": 2},
    "舍身攻击": {"cost": 0, "cd": 3, "dtype": "buff", "targets": 0, "buff": "舍身", "duration": 2},
    "战吼":     {"cost": 0, "cd": 0, "dtype": "buff", "targets": 0, "buff": "震慑", "duration": 1, "once": True},
}

# ==================== 武器技能 ====================
WEAPON_SKILLS = {
    # 二星武器技能
    "坚韧不拔": {"desc": "攻击后，下回合防御 +10"},
    "越战越勇": {"desc": "血量低于一半时，敌人攻击只造成 90% 伤害（四舍五入），减益不受影响"},
    "破釜沉舟": {"desc": "攻击力 > 防御力时，攻击 ×1.2（乘算），减益不受影响"},
    "学无止境": {"desc": "使用普攻后，下回合 +1 层渊博，每层 +10% 魔法精通，最多 5 层，持续整场"},
    # 三星武器技能
    "圣光裁决": {"desc": "敌方生命 < 10% 时攻击 ×1.2；本回合打出 > 400 伤害时，无视一切直接斩杀"},
    "战神的加护": {"desc": "第 10 个己方回合结束，防御 +10，攻击 +15%（加算），获得 1 层肾上腺素"},
    "破军":     {"desc": "敌人 > 1 时，单体攻击额外以 0.3 倍打随机 2 个其他目标，自身 80% 减伤"},
    "裂天":     {"desc": "敌人 = 1 时，攻击后额外造成 0.3 倍无视防御伤害；敌人 < 20% 血时每次攻击 10% 概率震慑"},
    "怒火":     {"desc": "伤害 ×（总生命 / 当前生命），封顶 1.5 倍，四舍五入一位小数"},
    "审判业火": {"desc": "敌人上回合造成 ≥ 你最大生命 5% 的伤害时，额外附加（该伤害/2）数值，并附加 3 回合燃烧"},
    "冥河":     {"desc": "本场每击杀一个敌人 +10% 魔法精通，封顶 40%"},
    "唤灵":     {"desc": "每用 3 次魔法技能，创造 1 只使魔，最多 2 只；使魔跟随攻击 0.2 倍；致命时消耗 1 只抵御，上限 -1"},
}

# ==================== 状态效果 ====================
# 减益
DEBUFFS = {
    "燃烧":   {"type": "dot", "value": 0.10, "stat": "max_hp", "desc": "每回合扣最大生命 1/10"},
    "中毒":   {"type": "dot", "value": 0.10, "stat": "max_hp", "desc": "每回合扣最大生命 1/10，降低 30% 近战伤害，不可叠加"},
    "寒冷":   {"type": "speed", "value": 0.5, "desc": "当前速度减半，主动闪避也减半，最多 3 回合，再叠转冰冻"},
    "冰冻":   {"type": "control", "desc": "无法行动"},
    "麻痹":   {"type": "control", "value": 0.5, "desc": "无法行动，防御减半"},
    "震慑":   {"type": "control", "desc": "无法行动，等同冰冻"},
    "网缚":   {"type": "speed", "value": 0.7, "desc": "攻击力与速度 ×0.7，禁用闪避"},
}

# 增益
BUFFS = {
    "治愈":     {"type": "hot", "value": 0.10, "stat": "max_hp", "desc": "每回合回最大生命 1/10"},
    "生命之光": {"type": "revive", "desc": "满血被一击清空时复活，按魔法伤害 10% 回血，每回合自动消耗 1 层"},
    "肾上腺素": {"type": "revive", "desc": "满血或 ≥75% 生命被致死时复活，按攻击力 10% 回血，触发时消耗"},
    "狂化":     {"type": "buff", "atk": 1.5, "def": 1.2, "no_magic": True, "desc": "非魔法攻击 ×1.5，防御 ×1.2，禁魔法"},
    "防御姿态": {"type": "buff", "dmg_taken": 0.5, "def": 2.0, "desc": "受到伤害减半，防御翻倍"},
    "防御反击": {"type": "buff", "desc": "敌人攻击后反伤 = 攻击伤害/2 + 防御×0.8 + 攻击力"},
    "舍身":     {"type": "buff", "atk": 1.8, "dmg_taken": 1.2, "ignore_def": True, "desc": "攻击 ×1.8，下回合敌人伤害无视防御 ×1.2"},
}

# 元素 → 所属减益
ELEMENT_DEBUFF = {"火": "燃烧", "冰": "寒冷", "雷": "麻痹", "毒": "中毒", "岩": None}
# 火焰系免疫冰冻和寒冷
FIRE_IMMUNE = ["冰冻", "寒冷"]

# ==================== 敌人公式 ====================
# 分段成长：1~10 基础增量，11~20 +0.5，21~30 +1.0
ENEMY_FORMULAS = {
    "史莱姆": {"hp": (15, 4), "atk": (3, 2), "def": (2, 1), "spd": (5, 0.5), "resist": "physical"},
    "蜘蛛":   {"hp": (10, 3), "atk": (5, 2.5), "def": (3, 1.2), "spd": (8, 0.8)},
    "藤蔓":   {"hp": (25, 6), "atk": (5, 2.2), "def": (3, 1.3), "spd": (2, 0.3)},
    "巨人":   {"hp": (30, 7), "atk": (6, 2.8), "def": (4, 1.8), "spd": (2, 0.2), "resist": "magic"},
}

# 敌人攻击分段增量（覆盖原公式的 atk 增量）
ENEMY_ATK_SEGMENTS = {"1_10": 2.5, "11_20": 3.0, "21_30": 4.0}

# ==================== 敌人列表 ====================
ENEMIES = {
    "火焰史莱姆": {"type": "史莱姆", "element": "火"},
    "寒冰史莱姆": {"type": "史莱姆", "element": "冰"},
    "雷电史莱姆": {"type": "史莱姆", "element": "雷"},
    "毒史莱姆":   {"type": "史莱姆", "element": "毒"},
    "岩史莱姆":   {"type": "史莱姆", "element": "岩"},
    "火焰蜘蛛":   {"type": "蜘蛛", "element": "火"},
    "雷电蜘蛛":   {"type": "蜘蛛", "element": "雷"},
    "黑寡妇":     {"type": "蜘蛛", "element": "毒", "hp_mult": 0.6},
    "岩蜘蛛":     {"type": "蜘蛛", "element": "岩"},
    "火焰藤蔓":   {"type": "藤蔓", "element": "火"},
    "寒霜藤蔓":   {"type": "藤蔓", "element": "冰"},
    "电击藤蔓":   {"type": "藤蔓", "element": "雷"},
    "熔岩巨人":   {"type": "巨人", "element": "火"},
    "冰雪巨人":   {"type": "巨人", "element": "冰"},
    "雷电巨人":   {"type": "巨人", "element": "雷"},
    "毒泥巨人":   {"type": "巨人", "element": "毒"},
}

# 通用元素修正
ELEMENT_MODS = {
    "火": {"atk": 1.4, "hp": 0.8},
    "岩": {"atk": 1.3, "def": 1.3, "hp": 1.3, "spd": 0.8, "magic_resist": 0.8},
}

# ==================== 敌人技能 ====================
ENEMY_SKILLS = {
    "史莱姆": ["跳跃砸击", "冲撞", "包裹"],
    "蜘蛛":   ["扑咬", "蛛网", "产卵"],
    "藤蔓":   ["缠绕", "寄生", "藤蔓囚笼"],
    "巨人":   ["震地", "重拳", "战争践踏"],
}

ENEMY_SKILL_DATA = {
    # 史莱姆
    "跳跃砸击": {"mult": 1.5, "charge": True, "effect": ("element", "1-2")},
    "冲撞":     {"mult": 1.2, "effect": ("element", 1), "chance": 0.75},
    "包裹":     {"mult": 0, "effect": ("element", 2), "disable_dodge": 1},
    # 蜘蛛
    "扑咬":     {"mult": 1.2, "effect": ("element", 1), "chance": 0.5},
    "蛛网":     {"mult": 0, "effect": ("网缚", 1)},
    "产卵":     {"mult": 0, "summon": "蜘蛛卵", "max": 3},
    # 藤蔓
    "缠绕":     {"mult": 1.2, "disable_dodge": 1, "effect": ("element", 1), "chance": 0.5},
    "寄生":     {"mult": 0.6, "seed": True, "once": True},
    "藤蔓囚笼": {"mult": 0, "random": ["disable_dodge_2", "def_up_30"]},
    # 巨人
    "震地":     {"mult": 0, "effect": ("震慑", 1)},
    "重拳":     {"mult": 2.0, "charge": True, "effect": ("element", "1-2")},
    "战争践踏": {"mult": 1.25, "hits": 2, "effect": ("震慑", 1), "chance": 0.5},
}

# 普通攻击附加元素减益概率
ENEMY_BASIC_DEBUFF_CHANCE = 0.15

# 敌人技能触发概率
ENEMY_SKILL_CHANCE = 0.30

# ==================== 武器分级掉落 ====================
# 按玩家等级决定掉落星级
def get_tier_by_level(level):
    if level <= 10:
        return "一星"
    elif level <= 20:
        return "二星"
    else:
        return "三星"

