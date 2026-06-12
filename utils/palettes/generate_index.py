import yaml

yaml_path = '/Users/dgd/Files/Code/Python/Academic-Plotting-Vault-Private/utils/palettes/palettes.yaml'
output_path = '/Users/dgd/Files/Code/Python/Academic-Plotting-Vault-Private/utils/palettes/macro_categories_index.md'

with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)

category_index = {}

for group_key, group_data in data.items():
    if not isinstance(group_data, dict):
        continue
        
    categories = group_data.get('macro_categories', [])
    if not categories:
        continue
        
    for category in categories:
        if category not in category_index:
            category_index[category] = []
        category_index[category].append({
            'group': group_key,
            'name': group_data.get('name', '')
        })

with open(output_path, 'w', encoding='utf-8') as f:
    f.write('# Palettes Index by Macro Categories\n\n')
    f.write('此索引文件根据 `palettes.yaml` 中的 `macro_categories` 自动生成，用于快速查找对应图表类型的配色方案。\n\n')
    
    for category in sorted(category_index.keys()):
        f.write(f'## {category}\n\n')
        
        groups = category_index[category]
        for group in groups:
            f.write(f'- **{group["group"]}**: {group["name"]}\n')
        f.write('\n')

print(f"Successfully created {output_path}")
