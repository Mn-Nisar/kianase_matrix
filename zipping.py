

import os
import zipfile

def zip_and_delete_output(kinase):
    folder_path = "output/"
    if not os.path.exists(folder_path):
        print(f"Error: The folder '{folder_path}' does not exist.")
        return
    output_zip = f"zip_output/{kinase}.zip"
    with zipfile.ZipFile(output_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)  # Maintain folder structure in ZIP
                zipf.write(file_path, arcname)
    print(f"All files in '{folder_path}' have been compressed into '{output_zip}'.")

    # Delete all the files in output/ folder
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for file in files:
            file_path = os.path.join(root, file)
            os.remove(file_path)
    print(f"All files in '{folder_path}' have been deleted.")

