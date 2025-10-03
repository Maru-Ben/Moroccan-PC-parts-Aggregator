from ..normalizers.gpu import GPUNormalizer

import os

normalizer = GPUNormalizer(os.path.join(os.path.dirname(__file__), "../rules/gpu.json"))

test_cases = [
    'msi geforce rtx 5060 ti 16g ventus 2x plus',
    'msi geforce rtx 5080 ventus 3x oc 16gb gddr7',
    'arktek amd radeon rx 580 8gb',
    'palit geforce rtx 4070 dual 12g',
    'msi geforce rtx 5070 12g inspire 3x oc',
    'asus rog geforce rtx nvlink bridge 4 slot avec aura sync rgb',
    'asrock radeon rx 9060 xt challenger oc 8gb gddr6',
    'xfx amd radeon rx 6700 speedster swift 309 10gb gddr6',
    'msi geforce rtx 3050 ventus 2x xs 8g oc',
    'gigabyte geforce rtx 5060 ti windforce oc 16g',
    'msi geforce rtx 5080 shadow 3x oc 16gb gddr7',
    'zotac gaming geforce rtx 5060 ti 8gb twin edge',
    'msi geforce rtx 5090 32g gaming trio oc',
    'xfx amd radeon rx 9070xt mercury oc gaming edition 16gb gddr6',
    'zotac gaming geforce rtx 5060 ti 8gb twin edge',
    'msi geforce rtx 5080 16g ventus 3x oc plus',
    'msi geforce rtx 5090 gaming trio oc 32gb gddr7',
    'maxsun geforce rtx 3060 terminator 12 go gddr6 (bulk)',
    'gigabyte geforce rtx 5080 aero oc sff 16g',
    'msi geforce rtx 5060 8g shadow 2x oc bulk',
    'msi rtx 3060 ti ventus 2x 8g',
    'msi geforce rtx 5060 8g inspire 2x oc',
    'asrock amd radeon rx 9070 xt steel legend 16gb',
    'gigabyte geforce rtx 5070 eagle oc sff 12g',
    'gainward geforce rtx 5080 phoenix v1 16gb gddr7',
    'palit geforce rtx 4070 dual 12gb gddr6',
    'msi geforce rtx 5090 32g ventus 3x oc',
    'asrock amd radeon rx 9070 xt steel legend 16gb',
    'gigabyte geforce rtx 3060 windforce oc 12gb gddr6',
    'gigabyte radeon rx 9070 gaming oc 16g',
    'arktek gtx 1050 ti 4gb',
    'msi geforce rtx 5070 ti 16g shadow 3x oc bulk',
    'gigabyte geforce rtx 3050 windforce oc v2 6g',
    'msi rtx 4060 ti ventus 2x 16g oc',
    'gigabyte geforce rtx 5070 aero oc 12g',
    'msi geforce rtx 5070 ti 16g shadow 3x oc',
    'zotac gaming geforce rtx 5070 amp edition blanc',
    'gigabyte geforce rtx 5060 ti windforce 8g',
    'gigabyte radeon rx 9070 gaming oc 16g',
    'msi geforce rtx 5050 8g shadow 2x oc',
    'gigabyte geforce rtx 5060 ti windforce oc 8g',
    'msi geforce rtx 5070 ventus 2x oc white 12gb gddr7',
    'msi geforce rtx 5060 8g ventus 2x oc blanc',
    'gigabyte geforce rtx 4060 eagle oc 8gb gddr6',
    'gigabyte geforce rtx 5080 windforce oc sff 16g',
    'asus prime geforce rtx 5080 16gb gddr7 oc edition',
    'msi geforce rtx 5060 ti 8g ventus 2x oc plus',
    'msi geforce rtx 5060 8g shadow 2x oc bulk',
    'msi geforce rtx 5090 gaming trio oc 32gb gddr7',
    'msi geforce rtx 5070 ti 16g inspire 3x oc',
    'msi geforce rtx 3050 ventus 2x xs oc 8gb gddr6',
    'inno3d geforce rtx 5070 12gb twin x2 gddr7',
    'arktek rtx 3070 dual fan',
    'zotac gaming geforce rtx 5070 solid oc 12gb gddr7',
    'msi geforce rtx 5070 ti 16g shadow 3x bulk',
    'asus dual geforce rtx 4070 ti super oc edition 16gb gddr6x',
    'zotac gaming geforce rtx 5070 amp edition blanc',
    'xfx amd radeon rx 9060 xt swift oc triple fan gaming edition 16gb gddr6',
    'asrock radeon rx 9060 xt challenger oc 8gb gddr6',
    'gigabyte geforce rtx 5060 ti eagle ice oc 8g',
    'gigabyte geforce rtx 5060 windforce oc 8g',
    'gigabyte geforce rtx 3050 eagle oc 8gb',
    'msi geforce rtx 5060 8g ventus 2x oc',
    'asrock amd radeon rx 9070 xt steel legend 16gb  (sans emballage)',
    'msi geforce rtx 5070 12g ventus 3x oc',
    'asus geforce rtx 3060 ti dual mini v2 oc 8gb',
    'arktek gtx 1660 super',
    'sapphire pure radeon rx 7900 xt 20gb gddr6',
    'asus geforce gtx 1660 super',
    'msi geforce rtx 5060 ti 8g shadow 2x oc plus bulk',
    'msi geforce rtx 5080 16g ventus 3x oc plus',
    'msi geforce rtx 5090 32g vanguard soc',
    'msi geforce rtx 5070 12g ventus 3x oc',
    'msi geforce rtx 5080 gaming trio oc 16gb gddr7',
    'msi geforce rtx 5070 12g inspire 3x oc',
    'msi geforce rtx 5050 8g gaming oc',
    'msi geforce rtx 4060 ti ventus 2x oc black 16gb gddr6',
    'msi geforce rtx 4060 ventus 2x white 8g oc',
    'gigabyte radeon rx 9070 xt gaming oc 16g',
    'msi geforce rtx 5080 vanguard soc 16gb gddr7',
    'gigabyte geforce rtx 5060 ti windforce oc 8g',
    'gigabyte radeon rx 9060 xt gaming oc 8g',
    'msi geforce rtx 5060 ti 16g shadow 2x plus',
    'zotac gaming geforce rtx 5070 ti solid sff oc 16gb gddr7',
    'msi geforce rtx 3050 ventus 2x e oc 6gb gddr6',
    'powercolor red devil amd radeon rx 9070 xt 16 go special edition',
    'gigabyte radeon rx 9070 gaming oc 16g',
    'gigabyte geforce rtx 5060 ti windforce oc 16g (exclusivite web)',
    'gigabyte geforce rtx 5060 ti windforce 8g',
    'gigabyte geforce rtx 5080 windforce oc sff 16g',
    'msi geforce rtx 5070 ventus 2x oc 12gb gddr7',
    'msi geforce rtx 5060 8g ventus 2x oc white',
    'xfx swift amd radeon rx 9070 oc gaming edition 16gb blanc',
    'maxsun geforce rtx 3060 terminator 12 go gddr6  (bulk)',
    'msi geforce rtx 5070 12g shadow 2x oc',
    'zotac gaming geforce rtx 5060 8gb twin edge',
    'msi geforce rtx 4060 gaming x nv edition 8gb gddr6',
    'msi geforce rtx 5070 ti 16g shadow 3x oc (bulk)',
    'msi geforce rtx 5070 shadow 3x oc 12gb gddr7',
    'msi geforce rtx 5070 gaming trio oc 12g gddr7'
]


def test_coloncical_grouping():
    
    # Group by canonical name
    groups = {}
    
    for title in test_cases:
        specs = normalizer.normalize(title)
        canonical = specs.model  # "RTX 4090 - ASUS"
        
        if canonical not in groups:
            groups[canonical] = []
        groups[canonical].append({
            'title': title
        })
        
        print(f"Title: {title}")
        print(f"Canonical: {canonical}")
        print("---")
    
    print("\nGROUPED PRODUCTS:")
    for canonical, products in groups.items():
        print(f"\n{canonical}:")
        for product in products:
            print(f"  - {product['title']}")


def test_grouping_decisions():
    groups = []
    
    for product_title in test_cases:
        specs = normalizer.normalize(product_title)
        print(f"🔍 Processing: {product_title}")
        print(f"   Canonical: {specs.model}")
        
        # Try to find a group this product should join
        found_group = False
        
        for group in groups:
            # Get a representative product from the group to compare against
            group_specs = group['products'][0]['specs']
            decision = normalizer.should_group(specs, group_specs)
            
            print(f"   Comparing with Group {group['id']}: {decision}")
            
            if decision['decision'] == 'group':
                # Add to this group
                group['products'].append({
                    'title': product_title,
                    'specs': specs,
                    'sub_brand': specs.key_specs['sub_brand_text']
                })
                print(f"   ✅ ADDED to Group {group['id']} (confidence: {decision['confidence']:.2f})")
                found_group = True
                break
        
        if not found_group:
            # Create new group
            new_group = {
                'id': len(groups) + 1,
                'canonical': specs.model,
                'products': [{
                    'title': product_title,
                    'specs': specs,
                    'sub_brand': specs.key_specs['sub_brand_text']
                }]
            }
            groups.append(new_group)
            print(f"   🆕 NEW Group {new_group['id']} created")
        
        print()
    
    # Show final results
    print("=" * 60)
    print("=== FINAL GROUPS ===\n")
    
    for group in groups:
        print(f"📦 Group {group['id']}: {group['canonical']}")
        print(f"   Products: {len(group['products'])}")
        
        for i, product in enumerate(group['products'], 1):
            print(f"   {i}. {product['title']}")
            print(f"      └─ Sub-brand: '{product['sub_brand']}'")
        
        # Show internal similarities if multiple products
        if len(group['products']) > 1:
            print(f"   🔍 Internal similarities:")
            for i in range(len(group['products']) - 1):
                specs1 = group['products'][i]['specs']
                specs2 = group['products'][i+1]['specs']
                similarity = normalizer.calculate_similarity(specs1, specs2)
                decision = normalizer.should_group(specs1, specs2)
                print(f"      Product {i+1} ↔ {i+2}: {similarity:.2f} ({decision['decision']})")
        
        print()



test_grouping_decisions()



