from data.data_enums import ItemType, Material, Condition

# Default description strings
default_descr = {
    'poor': ('It is in poor condition',
             'You expect it to break any second.'),
    'normal': ('It is in a fairly ordinary condition.',
               'It should hold... for a while.',
                'There is nothing remarkable about its condition.'),
    'good': ('It is in a good condition.',
             'You are suprised at its better than average condition',
             ),
    'legend': ('It is in a fantastic condition condition',
               'It is in a beyond pristine condition.'
               )
}


cond_name_data = {
    Condition.POOR: '(-)',
    Condition.GOOD: '(+)',
    Condition.LEGENDARY: '(++)'
}


cond_descr_data = {
    ItemType.MELEE_WEAPON: {
        Material.OAK: {
            Condition.POOR: (
                'The wood is brittle and might just snap any second.',
                "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
            ),
            Condition.NORMAL: (
                "The oak has mostly withstood the test of time.",
                "Unremarkable but it does have a basic finish at least."
            ),
            Condition.GOOD: (
                'The oak wood seems sturdy and in good condition.',
                'The oak frame has been spared by worms and is in nearly mint condition.'
            ),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.CHITIN: {
            Condition.POOR: (
                "Whatever insect had to die to make it, must not have been hard to kill at all",
                "Bits of meat and goo of the former owner are a testament to how little work this item has seen."
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: default_descr['good'],
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.IRON: {
            Condition.POOR:(
                'If you are lucky, all that rust might poison the enemy.',
                'It is so rusted, you are not sure if using wood would be sturdier.',
                'It appears to be more rust than actual metal.'
            ),
            Condition.NORMAL: (
                'There is some rust here and there, but it is in a generally okay condition.',
                'The metal has some kinks but overall it is in a solid state.'
            ),
            Condition.GOOD: (
                'It is well honed and the edges are still sharp.',
                'You reckon it will fell your foes easily.'
            ),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.STEEL: {
            Condition.POOR:(
                'If you are lucky, all that rust might poison the enemy.',
                'It is so rusted, you are not sure if using wood would be sturdier.'
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (
                'It is well honed and the edges are still sharp.',
                'You reckon it will fell your foes easily.'
            ),
            Condition.LEGENDARY: default_descr['legend']
        }
    },
    ItemType.RANGED_WEAPON: {
        Material.OAK: {
            Condition.POOR: default_descr['poor'],
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: default_descr['good'],
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.CHITIN: {
            Condition.POOR: default_descr['poor'],
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: default_descr['good'],
            Condition.LEGENDARY: default_descr['legend']
        },
    },
    ItemType.ARMOR: {
        Material.OAK: {
            Condition.POOR: (
                'You are worried it might snap at any second.',
                "It is terribly splintered, but at least the enemy might loose an eye when it breaks."
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.LEATHER: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.LINEN: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.IRON: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.STEEL: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        }},
    ItemType.SHIELD: {
        Material.OAK: {
            Condition.POOR: (
                'However, calling this worm-riddled plank a "shield" is rather generous.',
                "You wonder if the splinters in your hand are worth the dubious protection it offers."
            ),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.LEATHER: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.IRON: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        },
        Material.STEEL: {
            Condition.POOR:(),
            Condition.NORMAL: default_descr['normal'],
            Condition.GOOD: (),
            Condition.LEGENDARY: default_descr['legend']
        }}
}

# Old name list #
# 'names': {
        #     Material.OAK: 'splintered',
        #     Material.LINEN: 'frayed',
        #     Material.WOOL: 'frayed',
        #     Material.LEATHER: 'brittle',
        #     Material.IRON: 'rusty',
        #     Material.STEEL: 'rusty'
        # },
# 'names': {
        #     Material.OAK: 'sturdy',
        #     Material.LINEN: 'well fitting',
        #     Material.WOOL: 'well fitting',
        #     Material.LEATHER: 'hardened',
        #     Material.IRON: 'well honed',
        #     Material.STEEL: 'well honed'
        # },
