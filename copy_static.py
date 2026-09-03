import os
import shutil
import json
import re
import glob

def main():
    static_dir = 'src/helpdesk/static/helpdesk/vendor'
    os.makedirs(static_dir, exist_ok=True)

    with open('package.json', 'r') as f:
        data = json.load(f)
        vendors = list(data.get('dependencies', {}).keys())

    for vendor_name in vendors:
        src_dir = os.path.join('node_modules', vendor_name)
        dest_dir = os.path.join(static_dir, vendor_name)
        datatables_dir = os.path.join(static_dir, 'datatables')
        
        print(f"Processing vendor: {vendor_name}")
        if not os.path.isdir(src_dir):
            print(f"  -> ERROR: {src_dir} not found. Run yarn install first.")
            continue
        
        # Remove existing dest_dir if it exists
        if os.path.exists(dest_dir):
            if os.path.isdir(dest_dir):
                shutil.rmtree(dest_dir)
            else:
                os.remove(dest_dir)
        
        if vendor_name == "datatables":
            os.makedirs(dest_dir, exist_ok=True)
            media_dir = os.path.join(src_dir, 'media')
            if os.path.isdir(media_dir):
                for item in os.listdir(media_dir):
                    s = os.path.join(media_dir, item)
                    d = os.path.join(dest_dir, item)
                    if os.path.isdir(s):
                        shutil.copytree(s, d)
                    else:
                        shutil.copy2(s, d)
                        
        elif "datatables" in vendor_name:
            print("  -> [CASE: datatables] Matched! Copying JS/CSS...")
            js_dest = os.path.join(datatables_dir, 'js')
            css_dest = os.path.join(datatables_dir, 'css')
            images_dest = os.path.join(datatables_dir, 'images')
            os.makedirs(js_dest, exist_ok=True)
            os.makedirs(css_dest, exist_ok=True)
            os.makedirs(images_dest, exist_ok=True)
            
            js_src = os.path.join(src_dir, 'js')
            if os.path.isdir(js_src):
                for f_name in os.listdir(js_src):
                    if f_name.endswith('.js'):
                        shutil.copy2(os.path.join(js_src, f_name), js_dest)
                        
            css_src = os.path.join(src_dir, 'css')
            if os.path.isdir(css_src):
                for f_name in os.listdir(css_src):
                    if f_name.endswith('.css'):
                        shutil.copy2(os.path.join(css_src, f_name), css_dest)
                        
            images_src = os.path.join(src_dir, 'images')
            if os.path.isdir(images_src):
                for f_name in os.listdir(images_src):
                    shutil.copy2(os.path.join(images_src, f_name), images_dest)
                    
            if os.path.exists(dest_dir):
                if os.path.isdir(dest_dir):
                    shutil.rmtree(dest_dir)
                else:
                    os.remove(dest_dir)
                
        elif os.path.isdir(os.path.join(src_dir, 'dist')):
            print("  -> Copying 'dist' folder...")
            if vendor_name == "jquery-ui":
                print("  -> Copying 'themes' folder...")
                os.makedirs(dest_dir, exist_ok=True)
                themes_base = os.path.join(src_dir, 'dist', 'themes', 'base')
                if os.path.isdir(themes_base):
                    for item in os.listdir(themes_base):
                        s = os.path.join(themes_base, item)
                        d = os.path.join(dest_dir, item)
                        if os.path.isdir(s):
                            shutil.copytree(s, d)
                        else:
                            shutil.copy2(s, d)
            elif vendor_name == "metismenu":
                dest_dir = os.path.join(static_dir, 'metisMenu')
                if os.path.exists(dest_dir):
                    if os.path.isdir(dest_dir):
                        shutil.rmtree(dest_dir)
                    else:
                        os.remove(dest_dir)
                os.makedirs(dest_dir, exist_ok=True)
                
            shutil.copytree(os.path.join(src_dir, 'dist'), dest_dir, dirs_exist_ok=True)
            
            if vendor_name == "jquery-easing":
                for f_name in os.listdir(dest_dir):
                    f_path = os.path.join(dest_dir, f_name)
                    if os.path.isfile(f_path) and (f_name.endswith('.js') or f_name.endswith('.map')):
                        new_name = re.sub(r'\.([0-9]+\.[0-9]+)\.umd', '.umd', f_name)
                        new_name = new_name.replace('.umd', '')
                        if new_name != f_name:
                            shutil.move(f_path, os.path.join(dest_dir, new_name))
                            
        elif os.path.isdir(os.path.join(src_dir, 'umd')):
            print("  -> Copying 'umd' folder...")
            shutil.copytree(os.path.join(src_dir, 'umd'), dest_dir)
            
        elif glob.glob(os.path.join(src_dir, '*.min.js')):
            print("  -> Copying root-level files (*.min.js only)...")
            os.makedirs(dest_dir, exist_ok=True)
            for f_path in glob.glob(os.path.join(src_dir, '*.min.js')):
                shutil.copy2(f_path, dest_dir)
                
        elif os.path.isdir(os.path.join(src_dir, 'js')):
            print("  -> Copying js/* and css/* ...")
            os.makedirs(dest_dir, exist_ok=True)
            shutil.copytree(os.path.join(src_dir, 'js'), os.path.join(dest_dir, 'js'), dirs_exist_ok=True)
            
            css_src = os.path.join(src_dir, 'css')
            if os.path.isdir(css_src):
                shutil.copytree(css_src, os.path.join(dest_dir, 'css'), dirs_exist_ok=True)
                
            fonts_src = os.path.join(src_dir, 'webfonts')
            if os.path.isdir(fonts_src):
                shutil.copytree(fonts_src, os.path.join(dest_dir, 'webfonts'), dirs_exist_ok=True)
                
        else:
            print("  -> WARNING: No standard dist folder found.")
            os.makedirs(dest_dir, exist_ok=True)
            for f_path in glob.glob(os.path.join(src_dir, '*')):
                if os.path.isfile(f_path) and f_path.endswith(('.js', '.css', '.map')):
                    shutil.copy2(f_path, dest_dir)

    print("Static vendor copy completed successfully!")

if __name__ == '__main__':
    main()
